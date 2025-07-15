import logging

from dishka import Provider, Scope, make_async_container, provide
from sqlalchemy import Engine

from user.domain.interfaces.notification import UserNotificationRepository
from user.infrastructure.kafka.notif import NotifRepositoryImpl
from user.infrastructure.repositories.slqalchemy import DatabaseService

logger = logging.getLogger(__name__)

provider = Provider(scope=Scope.APP)

provider.provide(NotifRepositoryImpl, provides=UserNotificationRepository)


class ConnectionProvider(Provider):
    @provide
    async def provide_engine(self) -> Engine:
        return await DatabaseService.get_engine()


container = make_async_container(provider, ConnectionProvider())
