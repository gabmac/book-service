import logging
from datetime import datetime

from pika import BlockingConnection, ConnectionParameters
from pika.adapters.blocking_connection import BlockingChannel
from pika.credentials import PlainCredentials
from pika.exchange_type import ExchangeType

from src.infrastructure.settings.config import LogstashConfig, ProducerConfig


class Consumer:
    _instance = None
    connection: BlockingConnection
    channel: BlockingChannel
    reload: bool = False

    def __new__(cls, config: ProducerConfig, logstash_config: LogstashConfig):  # type: ignore
        cls.logger = logging.getLogger(logstash_config.loggername)

        # pylint: disable=unused-argument
        def callback(ch, method, properties, body) -> None:  # type: ignore
            cls.logger.info(
                {
                    "consumer_in": True,
                    "@timestamp": datetime.utcnow().isoformat(),
                    "routing_key": method.routing_key,
                    "properties": properties,
                    "exchange": "book-service-exchange",
                    "body": body,
                },
            )

        # pylint: enable=unused-argument

        if cls._instance is None or cls.reload:
            cls.connection = BlockingConnection(
                ConnectionParameters(
                    host=config.localhost,
                    credentials=PlainCredentials(config.user, config.password),
                ),
            )
            cls.channel = cls.connection.channel()
            cls.channel.exchange_declare(
                exchange="book-service-exchange",
                exchange_type=ExchangeType.direct,
            )
            result = cls.channel.queue_declare(
                queue="book-service-queue",
                auto_delete=True,
            )
            queue_name = result.method.queue

            for queue in config.queues:
                cls.channel.queue_bind(
                    exchange="book-service-exchange",
                    queue=queue_name,
                    routing_key=queue,
                )

            cls.channel.basic_consume(
                queue=queue_name,
                on_message_callback=callback,
                auto_ack=True,
            )
            cls.reload = False
            cls._instance = cls
        return cls._instance

    @classmethod
    def start_consuming(cls) -> None:
        cls.channel.start_consuming()
