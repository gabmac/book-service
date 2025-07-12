from fastapi.testclient import TestClient
from sqlalchemy import text
from tests.conftest import BaseConfTest

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
from src.infrastructure.adapters.entrypoints.consumer import Consumer
from src.infrastructure.settings.config import (
    DatabaseConfig,
    ElasticsearchConfig,
    ElasticsearchIndexConfig,
    LogstashConfig,
    ProducerConfig,
    SlaveDatabaseConfig,
    SystemConfig,
)
from src.infrastructure.settings.web_application import app


class BaseViewConfTest(BaseConfTest):
    fastapi_app = app
    test_client = None

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        db_config = DatabaseConfig()
        slave_db_config = SlaveDatabaseConfig()
        cls.db = DatabaseSettings(
            host=db_config.host,
            password=db_config.password,
            port=db_config.port,
            user=db_config.user,
            slave_host=slave_db_config.host,
            slave_port=slave_db_config.port,
        )
        cls.db._pg_trgm_install()
        cls.elasticsearch_config = ElasticsearchConfig()
        cls.elasticsearch_index_config = ElasticsearchIndexConfig()

        # Create real Elasticsearch client for tests
        cls.elasticsearch_client = ElasticsearchClient(cls.elasticsearch_config)
        cls.author_read_repository = AuthorReadRepository(db=cls.db)  # type: ignore
        cls.author_write_repository = AuthorWriteRepository(db=cls.db)  # type: ignore
        cls.book_read_repository = BookReadRepository(db=cls.db, elasticsearch_client=cls.elasticsearch_client)  # type: ignore
        cls.book_write_repository = BookWriteRepository(db=cls.db, elasticsearch_client=cls.elasticsearch_client)  # type: ignore
        cls.branch_read_repository = BranchReadRepository(db=cls.db)  # type: ignore
        cls.branch_write_repository = BranchWriteRepository(db=cls.db)  # type: ignore
        cls.book_category_read_repository = BookCategoryReadRepository(db=cls.db)  # type: ignore
        cls.book_category_write_repository = BookCategoryWriteRepository(db=cls.db)  # type: ignore
        cls.physical_exemplar_read_repository = PhysicalExemplarReadRepository(db=cls.db)  # type: ignore
        cls.physical_exemplar_write_repository = PhysicalExemplarWriteRepository(db=cls.db)  # type: ignore

        cls.producer_config = ProducerConfig()
        cls.logstash_config = LogstashConfig()
        cls.system_config = SystemConfig()
        cls.consumer = Consumer(
            cls.producer_config,
            cls.logstash_config,
            cls.system_config,
        )

        # Create real Elasticsearch client for tests

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        cls.consumer.stop_consuming()

    def setUp(self):
        super().setUp()
        if self.consumer.channel.is_closed:
            self.consumer.reload = True
            self.consumer = Consumer(
                self.producer_config,
                self.logstash_config,
                self.system_config,
            )

    def tearDown(self):
        super().tearDown()
        # Clean up Elasticsearch test data
        # Delete test index if it exists
        with self.db.get_session() as session:
            session.exec(text("DELETE FROM author_book_link"))  # type: ignore
            session.exec(text("DELETE FROM author"))  # type: ignore
            session.exec(text("DELETE FROM physical_exemplar"))  # type: ignore
            session.exec(text("DELETE FROM branch"))  # type: ignore
            session.exec(text("DELETE FROM book_book_category_link"))  # type: ignore
            session.exec(text("DELETE FROM book_category"))  # type: ignore
            session.exec(text("DELETE FROM book_data"))  # type: ignore
            session.exec(text("DELETE FROM book"))  # type: ignore
            session.commit()

        test_index = self.elasticsearch_index_config.books_index
        if self.elasticsearch_client.client.indices.exists(index=test_index):
            self.elasticsearch_client.client.indices.delete(index=test_index)

    @property
    def client(self) -> TestClient:
        """
        Fixture that creates client for requesting server.

        :param fastapi_app: the application.
        :yield: client for the app.
        """

        if self.test_client is None:
            self.test_client = TestClient(
                app=self.fastapi_app,
                base_url="http://localhost:9857",
            )

            self.test_client.headers.update(
                {
                    "Content-Type": "application/json",
                },
            )

        return self.test_client
