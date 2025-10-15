from sqlalchemy import Boolean, Column, String, UUID
from sqlalchemy.orm import relationship
import uuid

from app.models.base_model import Base


class VigilEnum(Base):
    __tablename__ = "vigil_enum"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)

    name = Column(String(100), nullable=False)
    is_deleted = Column(Boolean, default=False)

    name_in_csv = Column(String(100), nullable=False)
    post_in_csv = Column(String(100), nullable=True)

    schedule_vigils = relationship(
        "ScheduleVigil", back_populates="vigil_enum"
    )
