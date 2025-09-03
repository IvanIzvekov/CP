from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_session
from app.services.auth_service import (
    register_user, authenticate_user,
    create_access_token, create_refresh_token, verify_token
)
from app.schemas.user_schema import UserCreate, UserRead, UserLogin

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", response_model=UserRead)
async def api_register(user_data: UserCreate, session: AsyncSession = Depends(get_session)):
    try:
        user = await register_user(session, user_data)
        return user
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/login")
async def api_login(user_data: UserLogin, session: AsyncSession = Depends(get_session)):
    user = await authenticate_user(session, user_data.username, user_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    access_token = create_access_token(user.id)
    refresh_token = create_refresh_token(user.id)
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }

@router.post("/refresh")
async def refresh_token_endpoint(refresh_token: str):
    user_id = verify_token(refresh_token, token_type="refresh")
    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid refresh token")
    new_access_token = create_access_token(user_id)
    return {"access_token": new_access_token, "token_type": "bearer"}
