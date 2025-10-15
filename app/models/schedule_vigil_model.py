from sqlalchemy import TIMESTAMP, Column, ForeignKey, Index, UUID
from sqlalchemy.orm import relationship
import uuid

from app.models.base_model import Base


class ScheduleVigil(Base):
    __tablename__ = "schedule_vigil"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
    )
    date = Column(TIMESTAMP, nullable=False)

    vigil_id = Column(UUID, ForeignKey("vigil_enum.id"), nullable=False)
    user_id = Column(UUID, ForeignKey("users.id"), nullable=False)

    vigil_enum = relationship("VigilEnum", back_populates="schedule_vigils")
    user = relationship("User", back_populates="schedule_vigils")

    __table_args__ = (
        Index("schedule_vigil_date_idx", "date"),
        Index("schedule_vigil_user_id_idx", "user_id"),
        Index("schedule_vigil_user_id_date_idx", "user_id", "date"),
    )
