from sqlalchemy import Boolean, Column, String, UUID
from sqlalchemy.orm import relationship
import uuid

from app.models.association_tables import associate_users_projects
from app.models.base_model import Base


class Project(Base):
    __tablename__ = "projects"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
    )
    name = Column(String(255), nullable=False)
    annotation = Column(String(255), nullable=False)
    description = Column(String, nullable=False)
    is_active = Column(Boolean, nullable=False)
    photo_path = Column(String, nullable=True)

    users = relationship(
        "User", secondary=associate_users_projects, back_populates="projects"
    )
