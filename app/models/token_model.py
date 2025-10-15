from sqlalchemy import TIMESTAMP, Column, ForeignKey, Integer, String, UUID
from sqlalchemy.sql import func
import uuid

from app.models.base_model import Base


class RefreshToken(Base):
    __tablename__ = "refresh_tokens"

    id = Column(UUID(as_uuid=True), primary_key=True, autoincrement=True, default=uuid.uuid4, unique=True, nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"))
    token = Column(String(255), nullable=False, unique=True)
    created_at = Column(TIMESTAMP, default=func.now())
