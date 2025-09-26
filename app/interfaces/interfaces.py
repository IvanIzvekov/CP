from abc import ABC, abstractmethod


class IScheduleRepository(ABC):
    @abstractmethod
    async def save_vigils_schedule(self, vigils_schedule: dict):
        raise NotImplementedError


class IUserRepository(ABC):
    @abstractmethod
    async def get_by_id(self, user_id: int):
        raise NotImplementedError

    @abstractmethod
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
        raise NotImplementedError

    @abstractmethod
    async def save_refresh_token(
        self, user_id: int, refresh_token: str
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    async def get_refresh_token(self, user_id: int) -> str | None:
        raise NotImplementedError

    @abstractmethod
    async def get_by_username(self, username: str) -> dict | None:
        raise NotImplementedError
