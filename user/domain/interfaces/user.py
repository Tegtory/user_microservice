import uuid
from typing import Protocol

from user.domain.models import AuthUser, User


class UserRepository(Protocol):
    async def create(self, user: AuthUser) -> User:
        pass

    async def update(self, user: User) -> User:
        pass

    async def get(self, uid: uuid.UUID) -> User:
        pass

    async def get_by_tg_id(self, uid: int) -> User:
        pass
