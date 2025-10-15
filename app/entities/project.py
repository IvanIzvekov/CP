from app.entities.base_entity import BaseEntity
from uuid import UUID

from dataclasses import dataclass


@dataclass
class ProjectEntity(BaseEntity):
    id: UUID | None = None
    name: str | None = None
    annotation: str | None = None
    description: str | None = None
    is_active: bool | None = None
    photo: bytes | None = None