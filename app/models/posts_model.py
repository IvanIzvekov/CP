from sqlalchemy.orm import DeclarativeBase, relationship
from sqlalchemy import Integer, String, Column, TIMESTAMP, Boolean
from sqlalchemy.sql import func
from app.models.base_model import Base

class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    name = Column(String(255), nullable=False)

    users = relationship("User", back_populates="post")

