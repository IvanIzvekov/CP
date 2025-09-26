from fastapi import APIRouter, Depends, File, HTTPException, UploadFile

from app.core.database import get_session
from app.dependencies.auth_depend import check_auth_dep
from app.dependencies.premission_depend import check_upload_permission
from app.repositories.schedule_repository import ScheduleRepository
from app.services.schedule_service import ScheduleService

router = APIRouter(prefix="/schedule", tags=["schedule"])


@router.post("/vigils")
async def upload_vigils(
    file: UploadFile = File(..., description="Excel файл с расписанием"),
    session=Depends(get_session),
    user_id: int = Depends(check_auth_dep),
):
    await check_upload_permission(duty_id=3, user_id=user_id, session=session)
    if not file.filename.endswith(".xlsx"):
        raise HTTPException(
            status_code=400,
            detail="Нужно отправить именно файл .xlsx, тот в котором вы создаете "
            "графики нарядов.",
        )
    if file.content_type not in [
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        "application/octet-stream",
    ]:
        raise HTTPException(status_code=400, detail="Неверный формат файла")

    shedule_repo = ScheduleRepository(session)
    service = ScheduleService(shedule_repo)
    try:
        # TODO НАЙТИ ГДЕ УЖЕ ОТКРЫВАЕТСЯ ТРАНЗАКЦИЯ
        async with session.begin():
            pass

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
