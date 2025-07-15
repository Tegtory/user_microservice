from typing import Protocol

from user.domain.notifications import UserRegisteredNotification


class UserNotificationRepository(Protocol):
    async def about__user_registered(
        self, notification: UserRegisteredNotification
    ) -> None:
        pass
