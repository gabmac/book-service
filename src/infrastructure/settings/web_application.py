"""Application Settings"""

from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import (
    APIRouter,
    FastAPI,
)
from fastapi.middleware.cors import CORSMiddleware

from src.infrastructure.adapters.database.db.session import DatabaseSettings
from src.infrastructure.adapters.database.repository.author import AuthorRepository
from src.infrastructure.adapters.database.repository.book import BookRepository
from src.infrastructure.adapters.database.repository.book_category import (
    BookCategoryRepository,
)
from src.infrastructure.adapters.entrypoints.api.router import Initializer
from src.infrastructure.adapters.entrypoints.producer import Producer
from src.infrastructure.cross_cutting.middleware_context import (
    RequestContextsMiddleware,
)
from src.infrastructure.cross_cutting.middleware_logging import (
    RequestContextLogMiddleware,
)
from src.infrastructure.logs.logstash import LogStash
from src.infrastructure.settings.config import (
    DatabaseConfig,
    LogstashConfig,
    ProducerConfig,
    SlaveDatabaseConfig,
    SystemConfig,
)


class AppConfig:
    """Application Configurations"""

    def __init__(
        self,
        router: APIRouter,
        logstash: LogstashConfig,
        logstash_logger: LogStash,
        config: SystemConfig,
        db: DatabaseSettings,
        producer: Producer,
    ):
        self.logstash_logger = logstash_logger
        self.api_router = router
        self.logstash = logstash
        self.config = config
        self.db = db

        # pylint: disable=unused-argument
        @asynccontextmanager
        async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
            yield
            producer.stop()

        # pylint: enable=unused-argument

        self.app = FastAPI(
            title="Book Service",
            description="Book Service",
            openapi_url="/openapi.json",
            docs_url="/docs",
            redoc_url="/redoc",
            lifespan=lifespan,
        )

    def init_cors(self) -> None:
        """Initialize CORS"""
        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

    def init_context(self) -> None:
        self.app.add_middleware(
            RequestContextsMiddleware,
        )
        self.app.add_middleware(
            RequestContextLogMiddleware,
            config=self.logstash,
        )

    def init_logstash(self) -> None:
        self.logstash_logger.logstash_init()

    def init_routes(self) -> None:
        """Intialize Routes"""
        self.app.include_router(self.api_router)

    def start_application(self) -> FastAPI:
        """Start Application with Environment"""
        self.init_context()
        self.init_cors()
        self.init_logstash()
        self.init_routes()
        return self.app


def init_api() -> FastAPI:
    logstash_config = LogstashConfig()
    logstash_logger = LogStash(
        host=logstash_config.host,
        port=logstash_config.port,
        loggername=logstash_config.loggername,
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

    producer_config = ProducerConfig()
    producer = Producer(config=producer_config, logstash_config=logstash_config)

    book_repository = BookRepository(db=db)
    author_repository = AuthorRepository(db=db)
    book_category_repository = BookCategoryRepository(db=db)

    initializer = Initializer(
        producer=producer,
        book_repository=book_repository,
        author_repository=author_repository,
        book_category_repository=book_category_repository,
    )

    return AppConfig(
        router=initializer.api_router,
        logstash=logstash_config,
        logstash_logger=logstash_logger,
        config=SystemConfig(),
        db=db,
        producer=producer,
    ).start_application()


app = init_api()
