import dataclasses
import uuid

from user.common.exceptions import AppError, NotFoundError
from user.domain.interfaces.notification import UserNotificationRepository
from user.domain.interfaces.user import UserRepository
from user.domain.models import AuthUser, User
from user.domain.notifications import UserRegisteredNotification


@dataclasses.dataclass(frozen=True, slots=True)
class UserUseCase:
    repository: UserRepository
    notif: UserNotificationRepository

    async def register_by_telegram(self, register_user: AuthUser) -> User:
        try:
            await self.repository.get_by_tg_id(register_user.telegram_id)
        except NotFoundError:
            user = await self.repository.create(register_user)
            await self.notif.about__user_registered(
                UserRegisteredNotification(id=str(user.id)),
            )
            return user
        raise AppError

    async def get_by_telegram(self, uid: int) -> User:
        return await self.repository.get_by_tg_id(uid)

    async def get_by_id(self, uid: uuid.UUID) -> User:
        return await self.repository.get(uid)
