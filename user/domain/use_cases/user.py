from user.common.exceptions import AppError
from user.domain.interfaces.user import UserRepository
from user.domain.models import AuthUser, User


class UserUseCase:
    def __init__(self, repository: UserRepository) -> None:
        self.repository = repository

    async def register_by_telegram(self, uid: int, username: str) -> None:
        if await self.repository.get_by_telegram_id(uid):
            raise AppError
        await self.repository.create(
            AuthUser(telegram_id=uid, username=username)
        )

    async def login_by_telegram(self, uid: int) -> User:
        return await self.repository.get_by_telegram_id(uid)
