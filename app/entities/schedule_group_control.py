from app.entities.base_entity import BaseEntity
from uuid import UUID
from datetime import datetime

from dataclasses import dataclass


@dataclass
class ScheduleGroupControlEntity(BaseEntity):
    id: UUID | None = None
    date: datetime | None = None
