from sqlalchemy.orm import relationship
from sqlalchemy import Integer, String, Column, TIMESTAMP, Boolean, ForeignKey
from sqlalchemy.sql import func
from app.models.base_model import Base
from app.models.association_tables import duties_mtm, user_projects

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)

    username = Column(String(50), nullable=False, unique=True)

    nickname = Column(String(50), nullable=True)

    name = Column(String(255), nullable=False)
    surname = Column(String(255), nullable=False)
    second_name = Column(String(255), nullable=False)

    hashed_password = Column(String(255), nullable=False)
    register_at = Column(TIMESTAMP, nullable=False, default=func.now())
    last_activity_at = Column(TIMESTAMP, nullable=False, default=func.now(), onupdate=func.now())

    is_superuser = Column(Boolean, nullable=False, default=False)
    is_deleted = Column(Boolean, nullable=False, default=False)

    post_id = Column(Integer, ForeignKey("posts.id"), nullable=True)
    rank_id = Column(Integer, ForeignKey("ranks.id"), nullable=False, default=1)

    photo = Column(String, nullable=True)

    phone = Column(String, nullable=True)

    personnel_number = Column(Integer, nullable=True)

    # связи
    post = relationship(
        "Post",
                back_populates="users"
    )  # одна должность — много пользователей

    duties = relationship(
        "CompanyDuty",
        secondary=duties_mtm,
        back_populates="users"
    )
    rank = relationship(
        "Rank",
        back_populates="users"
    )

    projects = relationship(
        "Project",
        secondary=user_projects,
        back_populates="users"
    )
