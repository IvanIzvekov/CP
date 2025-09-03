from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.user_repository import get_user_by_id, create_user
from app.schemas.user_schema import UserCreate
from app.services.auth_service import verify_token
from fastapi import HTTPException, status
from app.models.user_model import User


async def check_token(token: str) -> int:
    user_id = verify_token(token, token_type="access")
    if not user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    return user_id