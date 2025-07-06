import json
import logging
from datetime import datetime

from pika import BlockingConnection, ConnectionParameters
from pika.adapters.blocking_connection import BlockingChannel
from pika.credentials import PlainCredentials
from pika.exchange_type import ExchangeType

from src.application.dto.producer import Message
from src.application.usecase.author.upsert_author import UpsertAuthor
from src.application.usecase.book.upsert_book import UpsertBook
from src.infrastructure.adapters.database.db.session import DatabaseSettings
from src.infrastructure.adapters.database.repository.author import AuthorRepository
from src.infrastructure.adapters.database.repository.book import BookRepository
from src.infrastructure.settings.config import (
    DatabaseConfig,
    LogstashConfig,
    ProducerConfig,
    SlaveDatabaseConfig,
)

db_config = DatabaseConfig()
slave_db_config = SlaveDatabaseConfig()
db = DatabaseSettings(
    host=db_config.host,
    password=db_config.password,
    port=db_config.port,
    user=db_config.user,
    slave_host=slave_db_config.host,
    slave_port=slave_db_config.port,
)
book_repository = BookRepository(db=db)
author_repository = AuthorRepository(db=db)

callables = {
    "book.creation": UpsertBook(book_repository),
    "author.creation": UpsertAuthor(author_repository),
}


class Consumer:
    _instance = None
    connection: BlockingConnection
    channel: BlockingChannel
    reload: bool = False

    def __new__(cls, config: ProducerConfig, logstash_config: LogstashConfig):  # type: ignore
        cls.logger = logging.getLogger(logstash_config.loggername)

        # pylint: disable=unused-argument
        def callback(ch, method, properties, body) -> None:  # type: ignore
            dict_str = body.decode("UTF-8")
            dict_json = json.loads(dict_str)
            cls.logger.info(
                json.dumps(
                    {
                        "consumer_in": True,
                        "@timestamp": datetime.utcnow().isoformat(),
                        "routing_key": method.routing_key,
                        "properties": properties,
                        "exchange": "book-service-exchange",
                        "body": dict_json,
                    },
                ),
            )
            body = Message.model_validate(dict_json)
            callables[method.routing_key].execute(body)  # type: ignore

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
