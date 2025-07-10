from fastapi.testclient import TestClient
from sqlalchemy import text
from tests.conftest import BaseConfTest

from src.infrastructure.adapters.database.db.session import DatabaseSettings
from src.infrastructure.adapters.database.repository.author import AuthorRepository
from src.infrastructure.adapters.database.repository.book import BookRepository
from src.infrastructure.adapters.database.repository.book_category import (
    BookCategoryRepository,
)
from src.infrastructure.adapters.database.repository.branch import BranchRepository
from src.infrastructure.adapters.database.repository.physical_exemplar import (
    PhysicalExemplarRepository,
)
from src.infrastructure.adapters.entrypoints.consumer import Consumer
from src.infrastructure.settings.config import (
    LogstashConfig,
    ProducerConfig,
    SystemConfig,
)
from src.infrastructure.settings.web_application import app


class BaseViewConfTest(BaseConfTest):
    fastapi_app = app
    test_client = None

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # cls.db = DatabaseSettings(
        #     host=DatabaseConfig.host,
        #     password=DatabaseConfig.password,
        #     port=DatabaseConfig.port,
        #     user=DatabaseConfig.user,
        #     slave_host=SlaveDatabaseConfig.host,
        #     slave_port=SlaveDatabaseConfig.port,
        # )
        cls.db = DatabaseSettings(
            host="localhost",
            password="123456",
            port=5432,
            user="postgres",
            slave_host="localhost",
            slave_port=5433,
        )
        cls.db._pg_trgm_install()
        cls.author_repository = AuthorRepository(db=cls.db)  # type: ignore
        cls.book_repository = BookRepository(db=cls.db)  # type: ignore
        cls.branch_repository = BranchRepository(db=cls.db)  # type: ignore
        cls.book_category_repository = BookCategoryRepository(db=cls.db)  # type: ignore
        cls.physical_exemplar_repository = PhysicalExemplarRepository(db=cls.db)  # type: ignore

        cls.producer_config = ProducerConfig()
        cls.logstash_config = LogstashConfig()
        cls.system_config = SystemConfig()
        cls.consumer = Consumer(
            cls.producer_config,
            cls.logstash_config,
            cls.system_config,
        )

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
