from sqlalchemy import TIMESTAMP, Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.models.base_model import Base
from app.models.schedule_vigil_model import ScheduleVigil


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), nullable=False, unique=True)

    name = Column(String(100), nullable=False)
    surname = Column(String(100), nullable=False)
    second_name = Column(String(100), nullable=True)
    short_name = Column(String(100), nullable=False)

    hashed_password = Column(String(255), nullable=False)
    is_superuser = Column(Boolean, default=False)
    is_deleted = Column(Boolean, default=False)
    register_at = Column(TIMESTAMP, default=func.now())

    post_id = Column(Integer, ForeignKey("posts.id"), nullable=True)
    rank_id = Column(
        Integer, ForeignKey("ranks.id"), nullable=False, default=1
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
