from app.entities.base_entity import BaseEntity
from uuid import UUID
from datetime import datetime

from dataclasses import dataclass

from app.entities.vigil_enum import VigilEnumEntity
from app.entities.user import UserEntity


@dataclass
class ScheduleVigilEntity(BaseEntity):
    id: UUID | None = None
    date: datetime | None = None

    vigil_id: int | None = None
    vigil: VigilEnumEntity | None = None

    user_id: UUID | None = None
    user: UserEntity | None = None
