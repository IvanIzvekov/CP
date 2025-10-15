from app.entities.base_entity import BaseEntity
from uuid import UUID
from datetime import datetime

from dataclasses import dataclass


@dataclass
class RefreshTokenEntity(BaseEntity):
    id: UUID | None = None
    user_id: UUID | None = None
    token: str | None = None
    created_at: datetime | None = None
