import json
import logging
from datetime import datetime

from pika import BlockingConnection, ConnectionParameters
from pika.adapters.blocking_connection import BlockingChannel
from pika.credentials import PlainCredentials
from pika.exchange_type import ExchangeType

from src.application.dto.producer import Message
from src.infrastructure.settings.config import LogstashConfig, ProducerConfig


class Producer:
    _instance = None
    connection: BlockingConnection
    channel: BlockingChannel

    def __new__(cls, config: ProducerConfig, logstash_config: LogstashConfig):  # type: ignore
        if cls._instance is None:
            cls.logger = logging.getLogger(logstash_config.loggername)
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
            cls._instance = cls
        return cls._instance

    @classmethod
    def publish(cls, message: Message) -> None:
        document = {
            "@timestamp": datetime.utcnow().isoformat(),
            "queue_name": message.queue_name,
            "message": message.message,
            "exchange": "book-service-exchange",
            "routing_key": message.queue_name,
            "producer_out": True,
        }
        cls.logger.info(document)
        cls.channel.basic_publish(
            exchange="book-service-exchange",
            routing_key=message.queue_name,
            body=json.dumps(message.model_dump()),
        )
        cls.logger.info(
            {"producer_in": True, "@timestamp": datetime.utcnow().isoformat()},
        )

    @classmethod
    def stop(cls) -> None:
        cls.connection.close()
