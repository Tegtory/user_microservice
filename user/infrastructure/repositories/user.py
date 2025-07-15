import logging
import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from user.common.exceptions import NotFoundError
from user.domain.models import AuthUser, User
from user.infrastructure.repositories.models import User as BDUser

logger = logging.getLogger(__name__)


class SQLUserRepositoryImpl:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create(self, user: AuthUser) -> User:
        logger.info(f"Creating user {user.telegram_id}")
        registered = User(**user.model_dump())
        self.session.add(
            BDUser(
                id=registered.id,
                telegram_id=registered.telegram_id,
                username=registered.username,
            )
        )
        await self.session.commit()
        return registered

    async def update(self, user: User) -> User:
        return user

    async def get(self, uid: uuid.UUID) -> User | None:
        return User()

    async def get_by_tg_id(self, uid: int) -> User | None:
        logger.info(f"Authorizing user - {uid}")
        stmt = select(BDUser).where(BDUser.telegram_id == uid)
        user = (await self.session.execute(stmt)).first()
        if user:
            return User(
                username=user[0].username,
                telegram_id=user[0].telegram_id,
                id=user[0].id,
                is_admin=user[0].is_admin,
                is_banned=user[0].is_banned,
            )

        raise NotFoundError
