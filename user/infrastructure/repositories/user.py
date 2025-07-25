import logging
import uuid
from typing import Any

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
        logger.info("Creating user %s", user.telegram_id)
        registered = User(**user.model_dump())
        self.session.add(
            BDUser(
                id=registered.id,
                telegram_id=registered.telegram_id,
                username=registered.username,
                name=registered.name,
            ),
        )
        await self.session.commit()
        return registered

    async def update(self, user: User) -> User:
        return user

    async def get(self, uid: uuid.UUID) -> User:
        logger.info("Microservice authorizing - %s", uid)
        stmt = select(BDUser).where(BDUser.id == uid)
        user = (await self.session.execute(stmt)).first()
        if user:
            return self.parse(user[0])
        raise NotFoundError

    async def get_by_tg_id(self, uid: int) -> User | None:
        logger.info("Authorizing user - %s", uid)
        stmt = select(BDUser).where(BDUser.telegram_id == uid)
        user = (await self.session.execute(stmt)).first()
        if user:
            return self.parse(user[0])
        raise NotFoundError

    def parse(self, user: Any) -> User:
        return User(
            username=user.username,
            telegram_id=user.telegram_id,
            id=user.id,
            name=user.name,
            is_admin=user.is_admin,
            is_banned=user.is_banned,
        )
