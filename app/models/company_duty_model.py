from sqlalchemy import TIMESTAMP, Boolean, Column, ForeignKey, Integer, String, Table
from sqlalchemy.orm import DeclarativeBase, relationship
from sqlalchemy.sql import func

from app.models.association_tables import associate_users_duties
from app.models.base_model import Base


class CompanyDuty(Base):
    __tablename__ = "company_duties"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)

    users = relationship(
        "User", secondary=associate_users_duties, back_populates="duties"
    )
