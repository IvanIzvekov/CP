from app.entities.base_entity import BaseEntity
from uuid import UUID
from datetime import datetime

from dataclasses import dataclass


@dataclass
class VigilEnumEntity(BaseEntity):
    id: UUID | None = None
    name: str | None = None
    is_deleted: bool | None = None
    name_in_csv: str | None = None
    post_in_csv: str | None = None
