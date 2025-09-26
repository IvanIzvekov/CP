import asyncio
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timedelta
from typing import Tuple

import jwt
from passlib.context import CryptContext

from app.core.config import settings
from app.exceptions.exceptions import InvalidCredentialsError, InvalidRefreshTokenError
from app.repositories.user_repository import IUserRepository


class AuthService:
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    ALGORITHM = "HS256"

    _executor = ThreadPoolExecutor()

    def __init__(self, user_repo: IUserRepository):
        self.repo = user_repo

    async def verify_password(self, plain: str, hashed: str) -> bool:
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(
            self._executor, self.pwd_context.verify, plain, hashed
        )

    async def _create_token(
        self, user_id: int, expires_delta: timedelta, token_type: str
    ) -> str:
        loop = asyncio.get_running_loop()
        expire = datetime.utcnow() + expires_delta
        payload = {"sub": str(user_id), "exp": expire, "type": token_type}
        return await loop.run_in_executor(
            self._executor,
            jwt.encode,
            payload,
            settings.JWT_SECRET,
            self.ALGORITHM,
        )

    async def create_access_token(self, user_id: int) -> str:
        return await self._create_token(
            user_id,
            timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
            "access",
        )

    async def create_refresh_token(self, user_id: int) -> str:
        return await self._create_token(
            user_id,
            timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS),
            "refresh",
        )

    async def verify_token(
        self, token: str, token_type: str = "access"
    ) -> int:
        loop = asyncio.get_running_loop()
        try:
            payload = await loop.run_in_executor(
                self._executor,
                jwt.decode,
                token,
                settings.JWT_SECRET,
                [self.ALGORITHM],
            )
            if payload.get("type") != token_type:
                raise InvalidRefreshTokenError("Invalid token type")
            user = int(payload.get("sub"))
            return user
        except jwt.PyJWTError:
            raise InvalidRefreshTokenError("Invalid or expired token")

    async def login(self, username: str, password: str) -> Tuple[str, str]:
        user = await self.repo.get_by_username(username)
        if not user or not await self.verify_password(
            password, user["hashed_password"]
        ):
            raise InvalidCredentialsError("Incorrect username or password")

        access, refresh = await asyncio.gather(
            self.create_access_token(user["id"]),
            self.create_refresh_token(user["id"]),
        )

        await self.repo.save_refresh_token(user["id"], refresh)
        return access, refresh

    async def refresh_tokens(self, refresh_token: str) -> Tuple[str, str]:
        user_id = await self.verify_token(refresh_token, "refresh")
        saved_token = await self.repo.get_refresh_token(user_id)
        if not saved_token:
            raise InvalidRefreshTokenError("Refresh token not found")
        if saved_token != refresh_token:
            raise InvalidRefreshTokenError("Refresh token revoked")

        new_access, new_refresh = await asyncio.gather(
            self.create_access_token(user_id),
            self.create_refresh_token(user_id),
        )

        await self.repo.save_refresh_token(user_id, new_refresh)
        return new_access, new_refresh
