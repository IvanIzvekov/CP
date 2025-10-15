from typing import List
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import selectinload

from app.entities.post import PostEntity
from app.entities.rank import RankEntity
from app.entities.user import UserEntity
from app.entities.company_duty import CompanyDutyEntity
from app.exceptions.exceptions import UserAlreadyExistsError, UserNotFoundError
from app.interfaces.interfaces import IUserRepository
from app.models.posts_model import Post
from app.models.refresh_token_model import RefreshToken
from app.models.user_model import User
from app.models.company_duty_model import CompanyDuty
from app.models.ranks_model import Rank
from app.logger.logger import logger


class UserRepository(IUserRepository):
    def __init__(self, session):
        self.session = session

    async def get_superusers(self) -> list[UserEntity] | None:
        stmt = select(
            User.id,
            User.username,
            User.name,
            User.surname,
            User.second_name,
            User.hashed_password,
            User.is_superuser,
            User.is_deleted,
            User.register_at,
            User.invocation,
            User.short_name,
            User.short_name_2,
        ).where(User.is_superuser == True, User.is_deleted == False)
        result = (await self.session.execute(stmt)).scalars().all()
        return (
            [
                UserEntity.from_model(user, load_relations=False)
                for user in result
            ]
            if result
            else None
        )

    async def create_ranks(self, data: List[RankEntity]) -> List[RankEntity]:
        if not data:
            return []

        ranks_orm = [Rank(**d.to_dict()) for d in data]
        self.session.add_all(ranks_orm)
        await self.session.commit()
        return [RankEntity.from_model(d) for d in ranks_orm]

    async def create_posts(self, data: List[PostEntity]) -> List[PostEntity]:
        if not data:
            return []

        post_orm = [Post(**d.to_dict()) for d in data]
        self.session.add_all(post_orm)
        await self.session.commit()
        return [PostEntity.from_model(d) for d in post_orm]

    async def get_users_from_ids(
        self, user_id: List[UUID] = None
    ) -> list[UserEntity]:
        stmt = select(User).options(
            selectinload(User.rank),
            selectinload(User.post),
            selectinload(User.duties),
            selectinload(User.projects),
            selectinload(User.responsible_tasks),
        )
        if user_id:
            stmt = stmt.where(User.id.in_(user_id))
        result = (await self.session.execute(stmt)).scalars().all()
        return [UserEntity.from_model(user) for user in result]

    async def create_company_duties(
        self, data: List[CompanyDutyEntity]
    ) -> List[CompanyDutyEntity]:
        if not data:
            return []
        company_duties = [CompanyDuty(**d.to_dict()) for d in data]
        self.session.add_all(company_duties)
        await self.session.commit()
        return [CompanyDutyEntity.from_model(d) for d in company_duties]

    async def get_user_duties(self, user: UserEntity) -> UserEntity:
        stmt = (
            select(User)
            .options(selectinload(User.duties))
            .where(User.id == user.id)
        )
        result = (await self.session.execute(stmt)).scalar_one_or_none()

        if not result:
            raise UserNotFoundError(f"User with id '{user.id}' not found")

        duties_entities = [
            CompanyDutyEntity.from_model(duty) for duty in result.duties
        ]

        user.duties = duties_entities
        return user

    async def get_by_id(self, user_id: UUID) -> UserEntity:
        stmt = (
            select(User)
            .where(User.id == user_id)
            .options(
                selectinload(User.rank),
                selectinload(User.post),
                selectinload(User.duties),
                selectinload(User.projects),
                selectinload(User.responsible_tasks),
            )
        )
        result = (await self.session.execute(stmt)).scalar_one_or_none()

        if not result:
            raise UserNotFoundError(f"User with id '{str(user_id)}' not found")

        return UserEntity.from_model(result, load_relations=True)

    async def create(
        self,
        user: UserEntity,
    ) -> UserEntity:
        try:
            user_orm = User(**user.to_dict())
            self.session.add(user_orm)

            await self.session.flush()

            stmt = (
                select(User)
                .options(
                    selectinload(User.post),
                    selectinload(User.rank),
                    selectinload(User.duties),
                    selectinload(User.projects),
                    selectinload(User.responsible_tasks),
                )
                .where(User.id == user_orm.id)
            )
            result = (await self.session.execute(stmt)).scalars().first()

            await self.session.commit()
            user = UserEntity.from_model(user_orm, load_relations=True)
            return user
        except IntegrityError as e:
            await logger.error(e)
            await self.session.rollback()
            raise UserAlreadyExistsError(
                f"User '{user.username}' already exists"
            )

    async def save_refresh_token(self, user_id: UUID, refresh_token: str):
        stmt = select(RefreshToken).where(RefreshToken.user_id == user_id)
        existing = (await self.session.execute(stmt)).scalar_one_or_none()

        if existing:
            existing.token = refresh_token
        else:
            self.session.add(
                RefreshToken(user_id=user_id, token=refresh_token)
            )

        await self.session.commit()

    async def get_refresh_token(self, user_id: UUID) -> str | None:
        stmt = select(RefreshToken).where(RefreshToken.user_id == user_id)
        token_obj = (await self.session.execute(stmt)).scalar_one_or_none()
        return token_obj.token if token_obj else None

    async def get_by_username(self, username: str) -> UserEntity | None:
        stmt = (
            select(User)
            .where(User.username == username)
            .options(
                selectinload(User.rank),
                selectinload(User.post),
                selectinload(User.duties),
                selectinload(User.projects),
                selectinload(User.responsible_tasks),
            )
        )
        user = (await self.session.execute(stmt)).scalar_one_or_none()

        if not user:
            return None

        return UserEntity.from_model(User, load_relations=True)

    async def get_duty_users(self, duty_id: UUID) -> List[UserEntity]:
        stmt = (
            select(User)
            .options(
                selectinload(User.duties),
                selectinload(User.rank),
                selectinload(User.post),
                selectinload(User.projects),
                selectinload(User.responsible_tasks),
            )
            .where(User.duties.any(CompanyDuty.id == duty_id))
        )
        result = (await self.session.execute(stmt)).scalars().all()
        return (
            [
                UserEntity.from_model(user, load_relations=True)
                for user in result
            ]
            if result
            else []
        )
