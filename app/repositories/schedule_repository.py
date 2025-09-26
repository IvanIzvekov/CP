from sqlalchemy.ext.asyncio import AsyncSession

from app.interfaces.interfaces import IScheduleRepository


class ScheduleRepository(IScheduleRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def save_vigils_schedule(self, vigils_schedule: dict):
        pass
