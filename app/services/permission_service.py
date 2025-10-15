from uuid import UUID

from app.entities.user import UserEntity
from app.interfaces.interfaces import IUserRepository


class PermissionService:
    def __init__(self, user_repo: IUserRepository):
        self.user_repo = user_repo

    async def can_upload_vigils(self, user: UserEntity, duty_id: UUID) -> bool:
        user = await self.user_repo.get_duties(user)

        if not user.duties:
            return False

        return True if duty_id in [duty.id for duty in user.duties] else False
