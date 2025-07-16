import json

from aio_pika import DeliveryMode, Message
from aio_pika.abc import AbstractExchange

from user.domain.notifications import UserRegisteredNotification


class NotificationRepositoryImpl:
    def __init__(self, exchange: AbstractExchange) -> None:
        self.exchange = exchange

    async def about__user_registered(
        self, notification: UserRegisteredNotification
    ) -> None:
        body = json.dumps(notification.model_dump()).encode()
        await self._send_notification(body)

    async def _send_notification(self, body: bytes) -> None:
        message = Message(body, delivery_mode=DeliveryMode.PERSISTENT)
        await self.exchange.publish(message, routing_key="info")
