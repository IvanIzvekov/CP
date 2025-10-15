from typing import List
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.entities.task import TaskEntity
from app.interfaces.interfaces import ITaskRepository


class TaskRepository(ITaskRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, task: TaskEntity) -> TaskEntity:
        pass

    async def update(self, task: TaskEntity) -> TaskEntity:
        pass

    async def delete(self, task: TaskEntity) -> TaskEntity:
        pass

    async def get_by_id(self, task_id: UUID) -> TaskEntity:
        pass

    async def get(
        self,
        task_ids: List[UUID] = None,
        owner_id: UUID = None,
        responsible_id: UUID = None,
    ) -> List[TaskEntity]:
        pass
