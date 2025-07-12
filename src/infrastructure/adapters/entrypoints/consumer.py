import json
import logging
from contextvars import ContextVar
from datetime import datetime, timezone

from pika import BlockingConnection, ConnectionParameters
from pika.adapters.blocking_connection import BlockingChannel
from pika.credentials import PlainCredentials
from pika.exceptions import ChannelClosedByBroker
from pika.exchange_type import ExchangeType
from uuid6 import uuid7

from src.application.dto.producer import Message
from src.application.usecase.author.delete_author import DeleteAuthor
from src.application.usecase.author.upsert_author import UpsertAuthor
from src.application.usecase.book.delete_book import DeleteBook
from src.application.usecase.book.upsert_book import UpsertBook
from src.application.usecase.book_category.upsert_book_category import (
    UpsertBookCategory,
)
from src.application.usecase.branch.upsert_branch import UpsertBranch
from src.application.usecase.physical_exemplar.upsert_physical_exemplar import (
    UpsertPhysicalExemplar,
)
from src.domain.entities.author import Author
from src.domain.entities.base import DeletionEntity
from src.domain.entities.book import Book
from src.domain.entities.book_category import BookCategory
from src.domain.entities.branch import Branch
from src.domain.entities.physical_exemplar import PhysicalExemplar
from src.infrastructure.adapters.database.db.session import DatabaseSettings
from src.infrastructure.adapters.database.elasticsearch.client import (
    ElasticsearchClient,
)
from src.infrastructure.adapters.database.repository.author_read import (
    AuthorReadRepository,
)
from src.infrastructure.adapters.database.repository.author_write import (
    AuthorWriteRepository,
)
from src.infrastructure.adapters.database.repository.book_category_read import (
    BookCategoryReadRepository,
)
from src.infrastructure.adapters.database.repository.book_category_write import (
    BookCategoryWriteRepository,
)
from src.infrastructure.adapters.database.repository.book_read import BookReadRepository
from src.infrastructure.adapters.database.repository.book_write import (
    BookWriteRepository,
)
from src.infrastructure.adapters.database.repository.branch_read import (
    BranchReadRepository,
)
from src.infrastructure.adapters.database.repository.branch_write import (
    BranchWriteRepository,
)
from src.infrastructure.adapters.database.repository.physical_exemplar_read import (
    PhysicalExemplarReadRepository,
)
from src.infrastructure.adapters.database.repository.physical_exemplar_write import (
    PhysicalExemplarWriteRepository,
)
from src.infrastructure.adapters.entrypoints.producer import Producer
from src.infrastructure.adapters.producer.author_producer import AuthorProducerAdapter
from src.infrastructure.adapters.producer.book_producer import BookProducerAdapter
from src.infrastructure.adapters.producer.physical_exemplar_producer import (
    PhysicalExemplarProducerAdapter,
)
from src.infrastructure.settings.config import (
    DatabaseConfig,
    ElasticsearchConfig,
    LogstashConfig,
    ProducerConfig,
    SlaveDatabaseConfig,
    SystemConfig,
)
from src.infrastructure.settings.environments import Environments

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

# Initialize Elasticsearch client
elasticsearch_config = ElasticsearchConfig()
elasticsearch_client = ElasticsearchClient(elasticsearch_config)

# Initialize read and write repositories
book_read_repository = BookReadRepository(
    db=db,
    elasticsearch_client=elasticsearch_client,
)
book_write_repository = BookWriteRepository(
    db=db,
    elasticsearch_client=elasticsearch_client,
)
author_read_repository = AuthorReadRepository(db=db)
author_write_repository = AuthorWriteRepository(db=db)
book_category_read_repository = BookCategoryReadRepository(db=db)
book_category_write_repository = BookCategoryWriteRepository(db=db)
branch_read_repository = BranchReadRepository(db=db)
branch_write_repository = BranchWriteRepository(db=db)
physical_exemplar_read_repository = PhysicalExemplarReadRepository(db=db)
physical_exemplar_write_repository = PhysicalExemplarWriteRepository(db=db)

# Initialize producer for external notifications
producer_config = ProducerConfig()
logstash_config = LogstashConfig()
producer = Producer(config=producer_config, logstash_config=logstash_config)

# Initialize producer adapters
book_producer = BookProducerAdapter(producer=producer)
author_producer = AuthorProducerAdapter(producer=producer)
physical_exemplar_producer = PhysicalExemplarProducerAdapter(producer=producer)

callables = {
    "book.upsert": {
        "usecase": UpsertBook(
            book_read_repository,
            book_write_repository,
            book_producer,
        ),
        "entity": Book,
    },
    "author.upsert": {
        "usecase": UpsertAuthor(
            author_read_repository,
            author_write_repository,
            author_producer,
        ),
        "entity": Author,
    },
    "book.deletion": {
        "usecase": DeleteBook(book_write_repository, book_producer),
        "entity": DeletionEntity,
    },
    "author.deletion": {
        "usecase": DeleteAuthor(author_write_repository, author_producer),
        "entity": DeletionEntity,
    },
    "book_category.upsert": {
        "usecase": UpsertBookCategory(book_category_write_repository),
        "entity": BookCategory,
    },
    "branch.upsert": {
        "usecase": UpsertBranch(branch_write_repository),
        "entity": Branch,
    },
    "physical_exemplar.upsert": {
        "usecase": UpsertPhysicalExemplar(
            physical_exemplar_write_repository,
            physical_exemplar_producer,
        ),
        "entity": PhysicalExemplar,
    },
}


class Consumer:
    _instance = None
    connection: BlockingConnection
    channel: BlockingChannel
    reload: bool = False
    host: str = ""
    config: ProducerConfig
    logstash_config: LogstashConfig
    system_config: SystemConfig

    def __new__(cls, config: ProducerConfig, logstash_config: LogstashConfig, system_config: SystemConfig):  # type: ignore
        cls.logger = logging.getLogger(logstash_config.loggername)
        cls.config = config
        cls.logstash_config = logstash_config
        cls.system_config = system_config

        # pylint: disable=unused-argument
        def callback(ch, method, properties, body) -> None:  # type: ignore
            dict_str = body.decode("UTF-8")
            dict_json = json.loads(dict_str)
            cid = ContextVar(
                "CID",
                default="",
            )
            cidvalue = f"{cid.get()}-{str(uuid7())}"
            cls.logger.info(
                json.dumps(
                    {
                        "consumer_in": True,
                        "@timestamp": datetime.now(timezone.utc).isoformat(),
                        "routing_key": method.routing_key,
                        "exchange": "book-service-exchange",
                        "body": dict_json,
                        "CID": cidvalue,
                    },
                ),
            )
            cid.set(cidvalue)
            body = Message.model_validate(dict_json)
            try:
                entity = callables[method.routing_key]["entity"].model_validate(  # type: ignore
                    json.loads(body.message),
                )
                callables[method.routing_key]["usecase"].execute(entity)  # type: ignore
                ch.basic_ack(delivery_tag=method.delivery_tag)
            except Exception as e:
                cidvalue += f"-{str(uuid7())}"
                cid.set(cidvalue)
                cls.logger.error(
                    {
                        "exception": f"Error processing message: {e}",
                        "CID": cidvalue,
                        "@timestamp": datetime.now(timezone.utc).isoformat(),
                        "routing_key": method.routing_key,
                        "exchange": "book-service-exchange",
                        "body": dict_json,
                    },
                )
                cls.channel.basic_nack(delivery_tag=method.delivery_tag, requeue=True)
                raise e

        # pylint: enable=unused-argument

        if cls._instance is None or cls.reload:
            cls.host = config.localhost
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
            try:
                result = cls.channel.queue_declare(
                    queue="book-service-queue",
                    durable=True,
                    passive=True,
                )
            except ChannelClosedByBroker:
                # Recreate channel if closed
                cls.connection = BlockingConnection(
                    ConnectionParameters(
                        host=cls.host,
                        credentials=PlainCredentials(config.user, config.password),
                    ),
                )
                cls.channel = cls.connection.channel()
                result = cls.channel.queue_declare(
                    queue="book-service-queue",
                    durable=True,
                )
            queue_name = result.method.queue

            for queue in config.queues:
                cls.channel.queue_bind(
                    exchange="book-service-exchange",
                    queue=queue_name,
                    routing_key=queue,
                )
            if system_config.environment != Environments.TEST:
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

    @classmethod
    def stop_consuming(cls) -> None:
        cls.channel.stop_consuming()

    @classmethod
    def consume(cls, routing_key: str) -> None:
        """
        Consume messages with a specific routing key from the main queue for testing.
        """
        queue_name = "book-service-queue"
        # Try to get one message from the queue
        for method, properties, body in cls.channel.consume(  # type: ignore
            queue=queue_name,
            auto_ack=True,
            inactivity_timeout=1,
        ):
            if method is None:
                cls.channel.queue_purge(queue=queue_name)
                cls.channel.cancel()
                return

            # Check if this message has the routing key we're looking for
            if method.routing_key == routing_key:
                dict_str = body.decode("UTF-8")
                dict_json = json.loads(dict_str)
                message_body = Message.model_validate(dict_json)

                try:
                    entity = callables[routing_key]["entity"].model_validate(  # type: ignore
                        json.loads(message_body.message),
                    )
                    callables[routing_key]["usecase"].execute(entity)  # type: ignore
                except Exception as e:
                    cls.logger.error(f"Error processing message: {e}")
                    raise e
