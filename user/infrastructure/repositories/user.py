import uuid

from user.domain.models import AuthUser, User


class MemoryUserRepositoryImpl:
    def __init__(self) -> None:
        self.users: list[User] = []

    async def create(self, user: AuthUser) -> User:
        registered = User(**user.model_dump())
        self.users.append(registered)
        return registered

    async def update(self, user: User) -> User:
        return user

    async def get(self, uid: uuid.UUID) -> User | None:
        return User()

    async def get_by_telegram_id(self, uid: int) -> User | None:
        for i in filter(lambda x: x.telegram_id == uid, self.users):
            return i if isinstance(i, User) else None
        return None
