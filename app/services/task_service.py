from app.interfaces.interfaces import ITaskRepository, IUserRepository
from app.entities.task import TaskEntity
from uuid import UUID
from app.exceptions.exceptions import ResponsibleTypeError, UserNotFoundError


class TaskService:
    def __init__(self, repository: ITaskRepository, user_repository: IUserRepository):
        self.repo = repository
        self.user_repo = user_repository

    async def create(self, responsible_id: UUID, text: str, owner_id: UUID, responsible_type: str = "user", can_be_completed: bool = True, can_be_deleted: bool = True):
        if responsible_type == "user":
            responsible = [await self.user_repo.get_by_id(responsible_id)]
        elif responsible_type == "duty":
            responsible = await self.user_repo.get_duty_users(responsible_id)
        else:
            raise ResponsibleTypeError("Неверный тип ответственного за задачу: 'user' or 'duty'")

        if not responsible:
            raise UserNotFoundError("Ответственный не найден")

        owner = await self.user_repo.get_by_id(owner_id)


        task = TaskEntity(
            text=text,
            owner=owner,
            responsible=responsible,
            can_be_completed=can_be_completed,
            can_be_deleted=can_be_deleted,
        )

        task = await self.repo.create(task)
        return task