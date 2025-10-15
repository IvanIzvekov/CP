from sqlalchemy import TIMESTAMP, Boolean, Column, ForeignKey, String, UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid

from app.models.base_model import Base
from app.models.association_tables import associate_task_responsibles


class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    username = Column(String(50), nullable=False, unique=True)

    name = Column(String(100), nullable=False)
    surname = Column(String(100), nullable=False)
    second_name = Column(String(100), nullable=True)
    short_name = Column(String(100), nullable=False)
    short_name_2 = Column(String(100), nullable=False)

    hashed_password = Column(String(255), nullable=False)
    is_superuser = Column(Boolean, default=False)
    is_deleted = Column(Boolean, default=False)
    register_at = Column(TIMESTAMP, default=func.now())

    post_id = Column(UUID, ForeignKey("posts.id"), nullable=True)
    rank_id = Column(
        UUID, ForeignKey("ranks.id"), nullable=False, default=1
    )
    invocation = Column(String(50), nullable=False)

    duties = relationship(
        "CompanyDuty",
        secondary="associate_users_duties",
        back_populates="users",
    )
    projects = relationship(
        "Project", secondary="associate_users_projects", back_populates="users"
    )

    post = relationship("Post", back_populates="users")
    rank = relationship("Rank", back_populates="users")
    schedule_vigils = relationship("ScheduleVigil", back_populates="user")

    responsible_tasks = relationship(
        "Task",
        secondary=associate_task_responsibles,
        back_populates="responsible",
        lazy="selectin"
    )

    owned_tasks = relationship(
        "Task",
        back_populates="owner_user",
        foreign_keys="Task.owner_id",
        lazy="selectin"
    )
