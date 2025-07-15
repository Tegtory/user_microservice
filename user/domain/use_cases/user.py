from user.common.exceptions import AppError, NotFoundError
from user.domain.interfaces.notification import UserNotificationRepository
from user.domain.interfaces.user import UserRepository
from user.domain.models import AuthUser, User
from user.domain.notifications import UserRegisteredNotification


class UserUseCase:
    def __init__(
        self, repository: UserRepository, notif: UserNotificationRepository
    ) -> None:
        self.repository = repository
        self.notif = notif

    async def register_by_telegram(self, uid: int, username: str) -> None:
        try:
            await self.repository.get_by_tg_id(uid)
        except NotFoundError:
            user = await self.repository.create(
                AuthUser(telegram_id=uid, username=username)
            )
            await self.notif.about__user_registered(
                UserRegisteredNotification(id=user.id)
            )
            return None
        raise AppError

    async def get_by_telegram(self, uid: int) -> User:
        return await self.repository.get_by_tg_id(uid)
