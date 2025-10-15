from app.entities.base_entity import BaseEntity
from uuid import UUID
from datetime import datetime

from dataclasses import dataclass

from app.entities.company_duty import CompanyDutyEntity
from app.entities.post import PostEntity
from app.entities.project import ProjectEntity
from app.entities.rank import RankEntity
from app.entities.task import TaskEntity


@dataclass
class OnlyUserEntity(BaseEntity):
    id: UUID | None = None
    username: str | None = None

    name: str | None = None
    surname: str | None = None
    second_name: str | None = None

    short_name: str | None = None
    short_name_2: str | None = None

    invocation: str | None = None

    hashed_password: str | None = None

    is_superuser: bool | None = None
    is_deleted: bool | None = None
    register_at: datetime | None = None

    post_id: UUID | None = None
    post: PostEntity | None = None

    rank_id: UUID | None = None
    rank: RankEntity | None = None


@dataclass
class UserEntity(OnlyUserEntity):
    duties: list[CompanyDutyEntity] | None = None

    projects: list[ProjectEntity] | None = None

    responsible_tasks: list[TaskEntity] | None = None