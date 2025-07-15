import logging

from aio_pika.abc import AbstractExchange
from dishka import Provider, Scope, make_async_container, provide
from sqlalchemy.ext.asyncio import AsyncSession

from user.domain.interfaces.notification import UserNotificationRepository
from user.domain.interfaces.user import UserRepository
from user.domain.use_cases.user import UserUseCase
from user.infrastructure.rabit.notif import NotifRepositoryImpl
from user.infrastructure.rabit.service import RabbitMQService
from user.infrastructure.repositories.slqalchemy import DatabaseService
from user.infrastructure.repositories.user import SQLUserRepositoryImpl

logger = logging.getLogger(__name__)

provider = Provider(scope=Scope.APP)

provider.provide(NotifRepositoryImpl, provides=UserNotificationRepository)
provider.provide(SQLUserRepositoryImpl, provides=UserRepository)
provider.provide(UserUseCase)


class ConnectionProvider(Provider):
    @provide(scope=Scope.APP)
    async def provide_engine(self) -> AsyncSession:
        return await DatabaseService().get_session()

    @provide(scope=Scope.APP)
    async def provide_exchange(self) -> AbstractExchange:
        return await RabbitMQService.get_exchange(
            "amqp://guest:guest@localhost/", "logs"
        )


container = make_async_container(provider, ConnectionProvider())
