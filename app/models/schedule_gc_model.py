import uuid

from sqlalchemy import TIMESTAMP, UUID, Column

from app.models.base_model import Base


class ScheduleGC(Base):
    __tablename__ = "schedule_group_control"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
    )
    date = Column(TIMESTAMP, nullable=False)
