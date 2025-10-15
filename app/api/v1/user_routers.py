from fastapi import APIRouter, Depends, HTTPException

from app.core.database import get_session
from app.entities.user import UserEntity
from app.exceptions.exceptions import UserAlreadyExistsError
from app.repositories.user_repository import UserRepository
from app.schemas.user_schema import UserCreate
from app.services.user_service import UserService

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/register")
async def register(user_data: UserCreate, session=Depends(get_session)):
    service = UserService(UserRepository(session))
    try:
        user_ent = UserEntity.from_schema(user_data)
        user = await service.create(user_ent)
        user_map = user.to_dict()
        user_map = user_map.pop("hashed_password")
        return {"user": user_map, "detail": "User created successfully"}
    except UserAlreadyExistsError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
