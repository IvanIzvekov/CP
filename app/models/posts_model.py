import uuid

from sqlalchemy import UUID, Column, String
from sqlalchemy.orm import relationship

from app.models.base_model import Base


class Post(Base):
    __tablename__ = "posts"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
    )
    name = Column(String(255), nullable=False)

    users = relationship("User", back_populates="post")
