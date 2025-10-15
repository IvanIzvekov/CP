import uuid

from sqlalchemy import UUID, Column, String
from sqlalchemy.orm import relationship

from app.models.association_tables import associate_users_duties
from app.models.base_model import Base


class CompanyDuty(Base):
    __tablename__ = "company_duties"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
    )
    name = Column(String(255), nullable=False)

    users = relationship(
        "User", secondary=associate_users_duties, back_populates="duties"
    )
