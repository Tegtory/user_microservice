import logging

from dishka import Provider, Scope, make_async_container

from user.domain.interfaces.notification import UserNotificationRepository
from user.infrastructure.kafka.notif import NotifRepositoryImpl

logger = logging.getLogger(__name__)

provider = Provider(scope=Scope.APP)

provider.provide(NotifRepositoryImpl, provides=UserNotificationRepository)

container = make_async_container(provider)
