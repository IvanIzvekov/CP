from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.user_model import User
from app.models.company_duty_model import CompanyDuty
from app.schemas.user_schema import UserCreate
from sqlalchemy.orm import selectinload

async def get_user_by_id(session: AsyncSession, user_id: int) -> User | None:
    stmt = (
        select(User)
        .where(User.id == user_id, User.is_deleted == False)  # проверка bool поля
        .options(
            selectinload(User.post),
            selectinload(User.rank),
            selectinload(User.duties),
        )
    )
    result = await session.execute(stmt)
    return result.scalar_one_or_none()

async def get_user_by_username(session: AsyncSession, username: str) -> User | None:
    # Используем подгрузку связанных объектов для асинхронного запроса
    stmt = (
        select(User)
        .options(
            selectinload(User.post),  # подгружаем пост
            selectinload(User.rank),  # подгружаем звание
            selectinload(User.duties),  # подгружаем обязанности
        )
        .where(User.username == username)
    )
    result = await session.execute(stmt)
    return result.scalar_one_or_none()

async def create_user(session: AsyncSession, user_data: UserCreate, hash: str) -> User:
    duties = []
    if user_data.duties_ids:
        stmt = select(CompanyDuty).where(CompanyDuty.id.in_(user_data.duties_ids))
        duties = (await session.execute(stmt)).scalars().all()

    user = User(
        username=user_data.username,
        name=user_data.name,
        surname=user_data.surname,
        second_name=user_data.second_name,
        hashed_password=hash,
        rank_id=user_data.rank_id,
        post_id=user_data.post_id,
        duties=duties
    )
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return await get_user_by_username(session, user.username)
