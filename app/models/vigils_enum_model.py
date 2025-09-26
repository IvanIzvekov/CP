from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.orm import relationship

from app.models.base_model import Base


class VigilEnum(Base):
    __tablename__ = "vigil_enum"

    id = Column(Integer, primary_key=True, autoincrement=True)

    name = Column(String(100), nullable=False)
    is_deleted = Column(Boolean, default=False)

    name_in_csv = Column(String(100), nullable=False)
    post_in_csv = Column(String(100), nullable=False)

    schedule_vigils = relationship(
        "ScheduleVigil", back_populates="vigil_enum"
    )
