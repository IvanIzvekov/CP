from app.entities.base_entity import BaseEntity
from uuid import UUID

from dataclasses import dataclass


@dataclass
class CompanyDutyEntity(BaseEntity):
    id: UUID | None = None
    name: str | None = None