from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID

from app.entities.user import UserEntity

async def check_upload_permission(
    duty_id: UUID, user: UserEntity, session: AsyncSession
):
    if user.is_superuser:
        return True

    if not duty_id in [duty.id for duty in user.duties]:
        raise HTTPException(
            status_code=403, detail="You don't have permissions"
        )
    return True
