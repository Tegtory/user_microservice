import dataclasses

from user.common.exceptions import AppError, NotFoundError
from user.domain.interfaces.notification import UserNotificationRepository
from user.domain.interfaces.user import UserRepository
from user.domain.models import AuthUser, User
from user.domain.notifications import UserRegisteredNotification


@dataclasses.dataclass()
class UserUseCase:
    repository: UserRepository
    notif: UserNotificationRepository

    async def register_by_telegram(self, register_user: AuthUser) -> None:
        try:
            await self.repository.get_by_tg_id(register_user.telegram_id)
        except NotFoundError:
            user = await self.repository.create(register_user)
            return await self.notif.about__user_registered(
                UserRegisteredNotification(id=user.id),
            )
        raise AppError

    async def get_by_telegram(self, uid: int) -> User:
        return await self.repository.get_by_tg_id(uid)
