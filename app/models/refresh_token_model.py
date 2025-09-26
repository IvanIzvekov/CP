from sqlalchemy import TIMESTAMP, Column, ForeignKey, Integer, String, func
from sqlalchemy.orm import relationship

from app.models.base_model import Base


class RefreshToken(Base):
    __tablename__ = "refresh_tokens"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        unique=True,
    )
    token = Column(String(512), nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now(), nullable=False)

    user = relationship("User", backref="refresh_token")
