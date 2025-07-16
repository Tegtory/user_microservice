from aio_pika import ExchangeType, connect
from aio_pika.abc import AbstractExchange

from user.common.config import config


class RabbitMQService:
    @staticmethod
    async def get_exchange(name: str) -> AbstractExchange:
        connection = await connect(config.get_rabbit_url())
        channel = await connection.channel()
        return await channel.declare_exchange(name, ExchangeType.FANOUT)
