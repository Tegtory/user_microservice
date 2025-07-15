from aio_pika import ExchangeType, connect
from aio_pika.abc import AbstractExchange


class RabbitMQService:
    @staticmethod
    async def get_exchange(host: str, name: str) -> AbstractExchange:
        connection = await connect(host)

        async with connection:
            channel = await connection.channel()
            return await channel.declare_exchange(name, ExchangeType.FANOUT)
