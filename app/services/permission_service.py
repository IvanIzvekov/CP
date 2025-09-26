from app.interfaces.interfaces import IUserRepository


class PermissionService:
    def __init__(self, user_repo: IUserRepository):
        self.user_repo = user_repo

    async def can_upload_vigils(self, user_id: int, duty_id: int) -> bool:
        duties = await self.user_repo.get_duties(user_id)

        if not duties:
            return False

        # 1 — админ, duty_id — особая обязанность
        if 1 in duties:
            return True
        if duty_id in duties:
            return True

        return False
