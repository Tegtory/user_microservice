from aio_pika import ExchangeType, connect
from aio_pika.abc import AbstractExchange

from user.common.config import config


class RabbitMQ:
    def __init__(self, url: str) -> None:
        self.url = url

    async def get_exchange(self, name: str) -> AbstractExchange | None:
        if not config.ENABLE_NOTIFICATIONS:
            return None
        connection = await connect(self.url)
        channel = await connection.channel()
        return await channel.declare_exchange(name, ExchangeType.FANOUT)
