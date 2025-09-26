from sqlalchemy import TIMESTAMP, Column, ForeignKey, Integer, String
from sqlalchemy.sql import func

from app.models.base_model import Base


class RefreshToken(Base):
    __tablename__ = "refresh_tokens"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    token = Column(String(255), nullable=False, unique=True)
    created_at = Column(TIMESTAMP, default=func.now())
