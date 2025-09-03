from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Optional
from app.services.user_service import check_token

# создаём схему авторизации один раз
http_bearer = HTTPBearer(auto_error=True)  # auto_error=True — автоматически выдаёт 401 если нет токена

async def check_auth_dep(
    credentials: HTTPAuthorizationCredentials = Depends(http_bearer)
):

    token = credentials.credentials

    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authorization token missing"
        )

    return await check_token(token)