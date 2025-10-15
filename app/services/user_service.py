from typing import List
from uuid import UUID

from passlib.context import CryptContext

from app.entities.user import UserEntity
from app.interfaces.interfaces import IUserRepository
from app.exceptions.exceptions import UserNotFoundError


class UserService:

    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def __init__(self, user_repo: IUserRepository):
        self.user_repo = user_repo

    async def get_user_duties(self, user: UserEntity) -> UserEntity:
        return await self.user_repo.get_user_duties(user)

    async def create(
        self,
        user_entity: UserEntity,
    ) -> UserEntity:

        hashed_password = await self.hash_password(user_entity.hashed_password)
        user_entity.hashed_password = hashed_password

        user_entity.short_name = (
            f"{user_entity.name[0]}. {user_entity.surname}"
        )
        user_entity.short_name_2 = f"{user_entity.surname} {user_entity.name[0]}.{user_entity.second_name[0] if user_entity.second_name else ''}{'.' if user_entity.second_name else ''}"
        user = await self.user_repo.create(user=user_entity)
        return user

    async def hash_password(self, password: str) -> str:
        return self.pwd_context.hash(password)

    async def verify_password(
        self, plain_password: str, hashed_password: str
    ) -> bool:
        return self.pwd_context.verify(plain_password, hashed_password)

    async def get_users_from_ids(
        self, user_id: List[UUID] = None
    ) -> List[UserEntity]:
        users = await self.user_repo.get_users_from_ids(user_id)
        if not users:
            raise UserNotFoundError("Users not found")
        return users
