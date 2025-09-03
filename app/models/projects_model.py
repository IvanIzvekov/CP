from sqlalchemy.orm import relationship
from sqlalchemy import Integer, String, Column, Boolean
from sqlalchemy.sql import func
from app.models.base_model import Base
from app.models.association_tables import user_projects

class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    name = Column(String(255), nullable=False)
    description = Column(String, nullable=False)
    is_active = Column(Boolean, nullable=False)
    photo = Column(String, nullable=True)

    users = relationship("User", secondary=user_projects, back_populates="projects")


