from sqlalchemy import Column, ForeignKey, Table, UUID
import uuid

from app.models.base_model import Base

associate_task_responsibles = Table(
    "associate_task_responsibles",
    Base.metadata,
    Column("task_id", UUID(as_uuid=True), ForeignKey("tasks.id"), primary_key=True),
    Column("user_id", UUID(as_uuid=True), ForeignKey("users.id"), primary_key=True),
)

associate_users_duties = Table(
    "associate_users_duties",
    Base.metadata,
    Column("id", UUID, primary_key=True, default=uuid.uuid4, unique=True, nullable=False),
    Column(
        "user_id",
        UUID,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    ),
    Column(
        "duty_id",
        UUID,
        ForeignKey("company_duties.id", ondelete="CASCADE"),
        nullable=False,
    ),
)

associate_users_projects = Table(
    "associate_users_projects",
    Base.metadata,
    Column("user_id", ForeignKey("users.id"), primary_key=True),
    Column("project_id", ForeignKey("projects.id"), primary_key=True),
)
