from typing import List

from app.entities.base_entity import BaseEntity
from uuid import UUID
from dataclasses import dataclass
from datetime import datetime

from app.entities.user import OnlyUserEntity


@dataclass
class TaskEntity(BaseEntity):
    id: UUID | None = None
    text: str | None = None
    owner: OnlyUserEntity | None = None
    responsible: List[OnlyUserEntity] | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None
    is_deleted: bool | None = None
    is_active: bool | None = None
    expired_at: datetime | None = None
    can_be_completed: bool | None = None
    can_be_deleted: bool | None = None