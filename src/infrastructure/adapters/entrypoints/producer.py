import json
import logging
from contextvars import ContextVar
from datetime import datetime, timezone

from pika import BlockingConnection, ConnectionParameters
from pika.adapters.blocking_connection import BlockingChannel
from pika.credentials import PlainCredentials
from pika.exchange_type import ExchangeType
from uuid6 import uuid7

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
                exchange_type=ExchangeType.topic,
            )
            cls._instance = cls
        return cls._instance

    @classmethod
    def publish(cls, message: Message) -> None:
        cid = ContextVar(
            "CID",
            default="",
        )
        cidvalue = f"{cid.get()}-{str(uuid7())}"
        cid.set(cidvalue)
        document = {
            "@timestamp": datetime.now(timezone.utc).isoformat(),
            "queue_name": message.queue_name,
            "message": message.message,
            "exchange": "book-service-exchange",
            "routing_key": message.queue_name,
            "producer_out": True,
            "CID": cidvalue,
        }
        cid.set(cidvalue)
        cls.logger.info(json.dumps(document))
        cls.channel.basic_publish(
            exchange="book-service-exchange",
            routing_key=message.queue_name,
            body=json.dumps(message.model_dump()),
        )
        cls.logger.info(
            json.dumps(
                {
                    "@producer_in": True,
                    "@timestamp": datetime.now(timezone.utc).isoformat(),
                    "CID": cidvalue,
                },
            ),
        )

    @classmethod
    def stop(cls) -> None:
        cls.connection.close()
