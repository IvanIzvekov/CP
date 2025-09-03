from sqlalchemy.orm import relationship
from sqlalchemy import Integer, String, Column
from app.models.base_model import Base

class Rank(Base):
    __tablename__ = "ranks"

    id = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    name = Column(String(255), nullable=False)
    short_name = Column(String(255), nullable=False)

    users = relationship("User", back_populates="rank")

