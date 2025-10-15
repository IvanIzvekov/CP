from sqlalchemy import TIMESTAMP, Column, ForeignKey, String, func, UUID
from sqlalchemy.orm import relationship
import uuid

from app.models.base_model import Base


class RefreshToken(Base):
    __tablename__ = "refresh_tokens"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    user_id = Column(
        UUID,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        unique=True,
    )
    token = Column(String(512), nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now(), nullable=False)

    user = relationship("User", backref="refresh_token")
