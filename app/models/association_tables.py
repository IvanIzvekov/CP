from sqlalchemy import Table, Column, Integer, ForeignKey
from app.models.base_model import Base

duties_mtm = Table(
    "duties_mtm",
    Base.metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("user_id", Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
    Column("duty_id", Integer, ForeignKey("company_duties.id", ondelete="CASCADE"), nullable=False),
)

user_projects = Table(
    "user_projects",
    Base.metadata,
    Column("user_id", ForeignKey("users.id"), primary_key=True),
    Column("project_id", ForeignKey("projects.id"), primary_key=True)
)
