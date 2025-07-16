import logging

from aio_pika.abc import AbstractExchange
from dishka import Provider, Scope, make_async_container, provide
from sqlalchemy.ext.asyncio import AsyncSession

from user.common.config import config
from user.domain.interfaces.notification import UserNotificationRepository
from user.domain.interfaces.user import UserRepository
from user.domain.use_cases.user import UserUseCase
from user.infrastructure.rabbit.notif import NotificationRepositoryImpl
from user.infrastructure.rabbit.service import RabbitMQ
from user.infrastructure.repositories.slqalchemy import Database
from user.infrastructure.repositories.user import SQLUserRepositoryImpl

logger = logging.getLogger(__name__)

provider = Provider(scope=Scope.APP)

provider.provide(
    NotificationRepositoryImpl, provides=UserNotificationRepository
)
provider.provide(SQLUserRepositoryImpl, provides=UserRepository)
provider.provide(UserUseCase)


class ConnectionProvider(Provider):
    @provide(scope=Scope.APP)
    async def provide_engine(self) -> AsyncSession:
        return await Database(config.get_db_url()).get_session()

    @provide(scope=Scope.APP)
    async def provide_exchange(self) -> AbstractExchange:
        return await RabbitMQ(config.rabbit_url).get_exchange("logs")


container = make_async_container(provider, ConnectionProvider())
