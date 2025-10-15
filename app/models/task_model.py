from sqlalchemy import Column, String, UUID, ForeignKey, TIMESTAMP, Boolean
from sqlalchemy.orm import relationship
import uuid
from datetime import datetime
from app.models.association_tables import associate_task_responsibles

from app.models.base_model import Base


class Task(Base):
    __tablename__ = "tasks"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
    )
    text = Column(String, nullable=False)

    owner_id = Column(
        UUID(as_uuid=True), ForeignKey("users.id"), nullable=False
    )

    owner = relationship(
        "User",
        back_populates="owned_tasks",
        foreign_keys=[owner_id],
        lazy="selectin",
    )

    responsible = relationship(
        "User",
        secondary=associate_task_responsibles,
        back_populates="responsible_tasks",
        lazy="selectin",
    )

    created_at = Column(TIMESTAMP, nullable=False, default=datetime.now)
    updated_at = Column(
        TIMESTAMP, nullable=False, default=datetime.now, onupdate=datetime.now
    )
    deleted_at = Column(TIMESTAMP, nullable=True)

    is_deleted = Column(Boolean, nullable=False, default=False)
    is_active = Column(Boolean, nullable=False, default=True)

    expired_at = Column(TIMESTAMP, nullable=True)
    # Параметр для того, чтобы отделять задачи по типу ЗН Р, которые должны закрываться автоматически.
    can_be_completed = Column(Boolean, default=True)
    can_be_deleted = Column(Boolean, default=True)

    attachments = relationship(
        "Attachment", back_populates="task", cascade="all, delete-orphan"
    )
