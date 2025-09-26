from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.models.association_tables import associate_users_projects
from app.models.base_model import Base


class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    name = Column(String(255), nullable=False)
    description = Column(String, nullable=False)
    is_active = Column(Boolean, nullable=False)
    photo = Column(String, nullable=True)

    users = relationship(
        "User", secondary=associate_users_projects, back_populates="projects"
    )
