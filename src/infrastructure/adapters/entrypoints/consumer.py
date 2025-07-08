import json
import logging
from datetime import datetime

from pika import BlockingConnection, ConnectionParameters
from pika.adapters.blocking_connection import BlockingChannel
from pika.credentials import PlainCredentials
from pika.exchange_type import ExchangeType

from src.application.dto.producer import Message
from src.application.usecase.author.delete_author import DeleteAuthor
from src.application.usecase.author.upsert_author import UpsertAuthor
from src.application.usecase.book.delete_book import DeleteBook
from src.application.usecase.book.upsert_book import UpsertBook
from src.application.usecase.book_category.upsert_book_category import (
    UpsertBookCategory,
)
from src.application.usecase.branch.upsert_branch import UpsertBranch
from src.domain.entities.author import Author
from src.domain.entities.base import DeletionEntity
from src.domain.entities.book import Book
from src.domain.entities.book_category import BookCategory
from src.domain.entities.branch import Branch
from src.infrastructure.adapters.database.db.session import DatabaseSettings
from src.infrastructure.adapters.database.repository.author import AuthorRepository
from src.infrastructure.adapters.database.repository.book import BookRepository
from src.infrastructure.adapters.database.repository.book_category import (
    BookCategoryRepository,
)
from src.infrastructure.adapters.database.repository.branch import BranchRepository
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
book_category_repository = BookCategoryRepository(db=db)
branch_repository = BranchRepository(db=db)

callables = {
    "book.upsert": {
        "usecase": UpsertBook(book_repository),
        "entity": Book,
    },
    "author.upsert": {
        "usecase": UpsertAuthor(author_repository),
        "entity": Author,
    },
    "book.deletion": {
        "usecase": DeleteBook(book_repository),
        "entity": DeletionEntity,
    },
    "author.deletion": {
        "usecase": DeleteAuthor(author_repository),
        "entity": DeletionEntity,
    },
    "book_category.upsert": {
        "usecase": UpsertBookCategory(book_category_repository),
        "entity": BookCategory,
    },
    "branch.upsert": {
        "usecase": UpsertBranch(branch_repository),
        "entity": Branch,
    },
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
                        "exchange": "book-service-exchange",
                        "body": dict_json,
                    },
                ),
            )
            body = Message.model_validate(dict_json)
            try:
                entity = callables[method.routing_key]["entity"].model_validate(  # type: ignore
                    json.loads(body.message),
                )
                callables[method.routing_key]["usecase"].execute(entity)  # type: ignore
                ch.basic_ack(delivery_tag=method.delivery_tag)
            except Exception as e:
                cls.logger.error(f"Error processing message: {e}")
                raise e

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
                exchange_type=ExchangeType.topic,
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
                auto_ack=False,
            )
            cls.reload = False
            cls._instance = cls
        return cls._instance

    @classmethod
    def start_consuming(cls) -> None:
        cls.channel.start_consuming()
