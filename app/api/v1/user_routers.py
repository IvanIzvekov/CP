from fastapi import APIRouter, Depends, HTTPException

from app.schemas.user_schema import UserRead
from app.models.user_model import User
from app.dependencies.auth_depend import check_auth_dep
from app.core.database import get_session
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/profile")
async def api_profile(current_user = Depends(check_auth_dep),
                      session: AsyncSession = Depends(get_session)):
    result = await session.execute(
        select(User)
        .options(selectinload(User.post),
                 selectinload(User.duties),
                 selectinload(User.rank))
        .where(User.id == current_user)
    )
    user = result.scalars().first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return UserRead.model_validate(user)


# Пример демонстрации того, как получить общие данные всех пользователей
# @router.get("/public-info", response_model=UserRead)
# async def api_profile(current_user = Depends(get_current_user_dep)):
#     return current_user

# Пример демонстрации того, как получить частные данные конкретного пользователя
# from app.core.database import get_session
# from app.dependencies.auth_depend import get_current_user_dep

# @router.get("/custom-info", response_model=UserRead)
# async def api_profile(
#         current_user = Depends(get_current_user_dep),
#         session: AsyncSession = Depends(get_session)):
#     return get_personal_info(session, current_user.id)
