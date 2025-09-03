from sqlalchemy.orm import DeclarativeBase, relationship
from sqlalchemy import Integer, String, Column, TIMESTAMP, Boolean, Table, ForeignKey
from sqlalchemy.sql import func
from app.models.base_model import Base
from app.models.association_tables import duties_mtm

class CompanyDuty(Base):
    __tablename__ = "company_duties"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)

    # связь через mtm
    users = relationship(
        "User",
        secondary=duties_mtm,
        back_populates="duties"
    )