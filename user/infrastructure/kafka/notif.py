import json
import logging

from aio_pika import DeliveryMode, Message
from aio_pika.abc import AbstractExchange

from user.domain.notifications import UserRegisteredNotification

logger = logging.getLogger(__name__)


class NotifRepositoryImpl:
    def __init__(self, exchange: AbstractExchange):
        self.exchange = exchange

    async def about__user_registered(
        self, notification: UserRegisteredNotification
    ) -> None:
        body = json.dumps(notification.model_dump()).encode()
        message = Message(body, delivery_mode=DeliveryMode.PERSISTENT)

        await self.exchange.publish(message, routing_key="info")

        logger.info("user registered notification")
