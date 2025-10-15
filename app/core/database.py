from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.core.config import settings
from app.models.association_tables import (
    associate_users_duties,
    associate_users_projects,
)
from app.models.base_model import Base
from app.models.company_duty_model import CompanyDuty
from app.models.posts_model import Post
from app.models.projects_model import Project
from app.models.ranks_model import Rank
from app.models.user_model import User
from app.models.schedule_vigil_model import ScheduleVigil
from app.models.refresh_token_model import RefreshToken
from app.models.vigils_enum_model import VigilEnum
from app.models.task_model import Task


engine = create_async_engine(settings.DB_URL, echo=True, future=True)
SessionLocal = async_sessionmaker(
    engine, expire_on_commit=False, class_=AsyncSession, autobegin=True
)


async def init_db(engine):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def shutdown_db(engine):
    await engine.dispose()


async def get_session() -> AsyncSession:
    async with SessionLocal() as session:
        yield session