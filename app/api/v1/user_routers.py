from fastapi import APIRouter, Depends, HTTPException

from app.core.database import get_session
from app.exceptions.exceptions import UserAlreadyExistsError
from app.repositories.user_repository import UserRepository
from app.schemas.user_schema import UserCreate
from app.services.user_service import UserService

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/register")
async def register(user_data: UserCreate, session=Depends(get_session)):
    user_repo = UserRepository(session)
    service = UserService(user_repo)

    try:
        async with session.begin():
            user_id = await service.create(**user_data.model_dump())
        return {"user_id": user_id, "detail": "User created successfully"}
    except UserAlreadyExistsError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
