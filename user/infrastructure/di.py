import logging

from aio_pika.abc import AbstractExchange
from dishka import Provider, Scope, make_async_container, provide
from sqlalchemy import Engine

from user.domain.interfaces.notification import UserNotificationRepository
from user.domain.interfaces.user import UserRepository
from user.domain.use_cases.user import UserUseCase
from user.infrastructure.rabit.notif import NotifRepositoryImpl
from user.infrastructure.rabit.service import RabbitMQService
from user.infrastructure.repositories.slqalchemy import DatabaseService
from user.infrastructure.repositories.user import MemoryUserRepositoryImpl

logger = logging.getLogger(__name__)

provider = Provider(scope=Scope.APP)

provider.provide(NotifRepositoryImpl, provides=UserNotificationRepository)
provider.provide(MemoryUserRepositoryImpl, provides=UserRepository)
provider.provide(UserUseCase)


class ConnectionProvider(Provider):
    @provide(scope=Scope.APP)
    async def provide_engine(self) -> Engine:
        return await DatabaseService.get_engine()

    @provide(scope=Scope.APP)
    async def provide_exchange(self) -> AbstractExchange:
        return await RabbitMQService.get_exchange(
            "amqp://guest:guest@localhost/", "logs"
        )


container = make_async_container(provider, ConnectionProvider())
