from sqlalchemy import Column, ForeignKey, Integer, Table

from app.models.base_model import Base

associate_users_duties = Table(
    "associate_users_duties",
    Base.metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column(
        "user_id",
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    ),
    Column(
        "duty_id",
        Integer,
        ForeignKey("company_duties.id", ondelete="CASCADE"),
        nullable=False,
    ),
)

associate_users_projects = Table(
    "associate_users_projects",
    Base.metadata,
    Column("user_id", ForeignKey("users.id"), primary_key=True),
    Column("project_id", ForeignKey("projects.id"), primary_key=True),
)
