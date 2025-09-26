from sqlalchemy import TIMESTAMP, Column, ForeignKey, Integer
from sqlalchemy.orm import relationship

from app.models.base_model import Base


class ScheduleVigil(Base):
    __tablename__ = "schedule_vigil"

    id = Column(Integer, primary_key=True, autoincrement=True)
    date = Column(TIMESTAMP, nullable=False)

    vigil_id = Column(Integer, ForeignKey("vigil_enum.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    vigil_enum = relationship("VigilEnum", back_populates="schedule_vigils")
    user = relationship("User", back_populates="schedule_vigils")
