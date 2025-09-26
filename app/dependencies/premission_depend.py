from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.user_repository import UserRepository
from app.services.permission_service import PermissionService


async def check_upload_permission(
    duty_id: int, user_id: int, session: AsyncSession
):
    user_repo = UserRepository(session)
    permission_service = PermissionService(user_repo)
    if not await permission_service.can_upload_vigils(user_id, duty_id):
        raise HTTPException(
            status_code=403, detail="You don't have permissions"
        )
    return user_id
