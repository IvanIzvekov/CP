from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import selectinload

from app.exceptions.exceptions import UserAlreadyExistsError, UserNotFoundError
from app.interfaces.interfaces import IUserRepository
from app.models.association_tables import associate_users_duties
from app.models.refresh_token_model import RefreshToken
from app.models.user_model import User


class UserRepository(IUserRepository):
    def __init__(self, session):
        self.session = session

    async def get_duties(self, user_id: int) -> list[int]:
        stmt = select(associate_users_duties.c.duty_id).where(
            associate_users_duties.c.user_id == user_id
        )
        result = (await self.session.execute(stmt)).scalars().all()
        await self.session.rollback()
        return result

    async def get_by_id(self, user_id: int):
        stmt = (
            select(User)
            .where(User.id == user_id)
            .options(
                selectinload(User.rank),
                selectinload(User.post),
                selectinload(User.duties),
                selectinload(User.projects),
            )
        )
        result = (await self.session.execute(stmt)).scalar_one_or_none()
        if not result:
            raise UserNotFoundError(f"User with id '{user_id}' not found")

        return {
            "id": result.id,
            "username": result.username,
            "name": result.name,
            "surname": result.surname,
            "second_name": result.second_name,
            "short_name": result.short_name,
            "is_superuser": result.is_superuser,
            "is_deleted": result.is_deleted,
            "register_at": (
                result.register_at.isoformat() if result.register_at else None
            ),
            "post_name": getattr(result.post, "name", None),
            "rank_name": getattr(result.rank, "name", None),
            "duties": [d.name for d in getattr(result, "duties", [])],
            "projects": [p.name for p in getattr(result, "projects", [])],
            "hashed_password": result.hashed_password,
            "invocation": result.invocation,
        }

    async def create(
        self,
        name: str,
        surname: str,
        username: str,
        hashed_password: str,
        second_name: str,
        invocation: str,
        short_name: str,
        rank_id: int,
    ) -> int:
        try:
            user = User(
                username=username,
                hashed_password=hashed_password,
                name=name,
                surname=surname,
                second_name=second_name,
                invocation=invocation,
                short_name=short_name,
                rank_id=rank_id,
            )
            self.session.add(user)
            await self.session.flush()
            return user.id
        except IntegrityError as e:
            print(e)
            raise UserAlreadyExistsError(f"User '{username}' already exists")

    async def save_refresh_token(self, user_id: int, refresh_token: str):
        stmt = select(RefreshToken).where(RefreshToken.user_id == user_id)
        existing = (await self.session.execute(stmt)).scalar_one_or_none()
        if existing:
            existing.token = refresh_token
        else:
            self.session.add(
                RefreshToken(user_id=user_id, token=refresh_token)
            )

    async def get_refresh_token(self, user_id: int) -> str | None:
        stmt = select(RefreshToken).where(RefreshToken.user_id == user_id)
        token_obj = (await self.session.execute(stmt)).scalar_one_or_none()
        if token_obj:
            return token_obj.token
        return None

    async def get_by_username(self, username: str) -> dict | None:
        stmt = (
            select(User)
            .where(User.username == username)
            .options(
                selectinload(User.rank),
                selectinload(User.post),
                selectinload(User.duties),
                selectinload(User.projects),
            )
        )
        user = (await self.session.execute(stmt)).scalar_one_or_none()
        if not user:
            return None

        return {
            "id": user.id,
            "username": user.username,
            "name": user.name,
            "surname": user.surname,
            "second_name": user.second_name,
            "short_name": user.short_name,
            "is_superuser": user.is_superuser,
            "is_deleted": user.is_deleted,
            "register_at": (
                user.register_at.isoformat() if user.register_at else None
            ),
            "post_name": getattr(user.post, "name", None),
            "rank_name": getattr(user.rank, "name", None),
            "duties": [d.name for d in getattr(user, "duties", [])],
            "projects": [p.name for p in getattr(user, "projects", [])],
            "hashed_password": user.hashed_password,
            "invocation": user.invocation,
        }
