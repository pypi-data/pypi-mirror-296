from typing import Callable

from pika import BasicProperties
from pika.exceptions import UnroutableError

from app.lib_service_transport.services.rabbit.base_consumer import BaseConsumerRabbit


class ConsumerRPCRabbit(BaseConsumerRabbit):
    """Базовый класс Consumer для RPC"""

    CALLBACK: Callable = NotImplemented

    def on_request(
            self,
            ch: 'BlockingChannel',  # noqa
            method: 'Basic.Deliver',  # noqa
            properties: 'BasicProperties',
            body: bytes,
    ) -> None:
        """Принимает данные из входящих запросов и отвечает на запросы."""

        response = self.CALLBACK()

        try:
            self._channel.basic_publish(
                exchange='',
                routing_key=properties.reply_to,
                properties=BasicProperties(correlation_id=properties.correlation_id),
                body=response
            )
        except UnroutableError:
            raise

        self.acknowledge_message(delivery_tag=method.delivery_tag)

    def acknowledge_message(self, delivery_tag) -> None:
        """
            Подтверждение получения сообщения от сервера RabbitMQ путем отправки
            ему соответствующего сообщения в ответ.
        """
        self._channel.basic_ack(delivery_tag=delivery_tag)
