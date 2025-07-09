from fastapi.testclient import TestClient
from tests.conftest import BaseConfTest

from src.infrastructure.adapters.database.db.session import DatabaseSettings
from src.infrastructure.adapters.database.repository.branch import BranchRepository
from src.infrastructure.adapters.entrypoints.consumer import Consumer
from src.infrastructure.settings.config import (
    LogstashConfig,
    ProducerConfig,
    SystemConfig,
)
from src.infrastructure.settings.web_application import app


class BaseViewConfTest(BaseConfTest):
    fastapi_app = app

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
        cls.branch_repository = BranchRepository(db=cls.db)  # type: ignore

        producer_config = ProducerConfig()
        logstash_config = LogstashConfig()
        system_config = SystemConfig()
        cls.consumer = Consumer(producer_config, logstash_config, system_config)

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        cls.consumer.stop_consuming()

    @property
    def client(self) -> TestClient:
        """
        Fixture that creates client for requesting server.

        :param fastapi_app: the application.
        :yield: client for the app.
        """

        test_client = TestClient(
            app=self.fastapi_app,
            base_url="http://localhost:9857",
        )

        test_client.headers.update(
            {
                "Content-Type": "application/json",
            },
        )

        return test_client
