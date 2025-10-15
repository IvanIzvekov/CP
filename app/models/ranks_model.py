from sqlalchemy import Column, String, UUID
from sqlalchemy.orm import relationship
import uuid

from app.models.base_model import Base


class Rank(Base):
    __tablename__ = "ranks"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True)
    name = Column(String(255), nullable=False)
    short_name = Column(String(255), nullable=False)

    users = relationship("User", back_populates="rank")
