from passlib.context import CryptContext

from app.interfaces.interfaces import IUserRepository


class UserService:

    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def __init__(self, user_repo: IUserRepository):
        self.user_repo = user_repo

    async def get_duties(self, user_id: int) -> list:
        return await self.user_repo.get_duties(user_id)

    async def create(
        self,
        name: str,
        surname: str,
        password: str,
        username: str,
        second_name: str,
        invocation: str,
        rank_id: int,
    ) -> int:

        hashed_password = await self.hash_password(password)

        short_name = f"{name[0]}. {surname}"
        user_id = await self.user_repo.create(
            username=username,
            hashed_password=hashed_password,
            name=name,
            surname=surname,
            second_name=second_name,
            invocation=invocation,
            short_name=short_name,
            rank_id=rank_id,
        )
        return user_id

    async def hash_password(self, password: str) -> str:
        return self.pwd_context.hash(password)

    async def verify_password(
        self, plain_password: str, hashed_password: str
    ) -> bool:
        return self.pwd_context.verify(plain_password, hashed_password)
