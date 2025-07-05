"""Application Settings"""


from fastapi import (
    APIRouter,
    FastAPI,
    HTTPException,
    Request,
    status,
)
from fastapi.middleware.cors import CORSMiddleware

from src.infrastructure.adapters.entrypoints.api.router import api_router
from src.infrastructure.cross_cutting.middleware_context import (
    RequestContextsMiddleware,
)
from src.infrastructure.cross_cutting.middleware_logging import (
    RequestContextLogMiddleware,
)
from src.infrastructure.logs.logstash import LogStash
from src.infrastructure.settings.config import (
    LogstashConfig,
    SystemConfig,
)
from src.infrastructure.settings.environments import Environments


class AppConfig:
    """Application Configurations"""

    def __init__(
        self,
        router: APIRouter,
        logstash: LogstashConfig,
        logstash_logger: LogStash,
        # producer: Producer,
        config: SystemConfig,
        # db: DatabaseSettings,
    ):
        self.logstash_logger = logstash_logger
        self.api_router = router
        self.logstash = logstash
        # self.producer = producer
        self.config = config
        # self.db = db
        self.app = FastAPI(
            title="Book Service",
            description="Book Service",
            openapi_url="/openapi.json",
            docs_url="/docs",
            redoc_url="/redoc",
            # lifespan=self.lifespan,
        )

        self.app.add_exception_handler(
            exc_class_or_status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            handler=self.exception_handler,  # type: ignore[arg-type]
        )

    # @asynccontextmanager
    # async def lifespan(self):
    #     if self.config.environment != Environments.LOCAL.value:
    #         self.db.init_db()
    #     yield
    #     self.producer.close()

    def init_cors(self) -> None:
        """Initialize CORS"""
        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

    @staticmethod
    # pylint: disable=unused-argument
    async def exception_handler(request: Request, exc: Exception) -> None:
        # pylint: enable=unused-argument
        if SystemConfig().environment != Environments.LOCAL.value:
            raise HTTPException(
                detail="Something fail",
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
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


# producer_config = ProducerConfig()
# producer = Producer(localhost=producer_config.localhost, queues=producer_config.queues)
logstash_config = LogstashConfig()
logstash_logger = LogStash(
    host=logstash_config.host,
    port=logstash_config.port,
    loggername=logstash_config.loggername,
)

# db_config = DatabaseConfig()
# db = DatabaseSettings(host=db_config.host, password=db_config.password, port=db_config.port, user=db_config.user, database=db_config.database)

app = AppConfig(
    router=api_router,
    logstash=logstash_config,
    logstash_logger=logstash_logger,
    # producer=producer,
    config=SystemConfig(),
    # db=db,
).start_application()
