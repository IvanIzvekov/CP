from app.entities.company_duty import CompanyDutyEntity
from app.entities.post import PostEntity
from app.entities.rank import RankEntity
from app.entities.vigil_enum import VigilEnumEntity
from app.interfaces.interfaces import IUserRepository, IScheduleRepository
from typing import List


class UtilsService:
    def __init__(self, user_repo: IUserRepository, schedule_repo: IScheduleRepository):
        self.user_repo = user_repo
        self.schedule_repo = schedule_repo

    async def get_superusers(self):
        return await self.user_repo.get_superusers()

    async def set_standard_vigils(self, data: List[VigilEnumEntity]) -> List[VigilEnumEntity]:
        return await self.schedule_repo.create_vigils_type(data=data)

    async def set_standard_duties(self, data: List[CompanyDutyEntity]) -> List[CompanyDutyEntity]:
        return await self.user_repo.create_company_duties(data=data)

    async def set_standard_ranks(self, data: List[RankEntity]):
        return await self.user_repo.create_ranks(data=data)

    async def set_standard_posts(self, data: List[PostEntity]) -> List[PostEntity]:
        return await self.user_repo.create_posts(data=data)