from typing import Set

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

from src.infrastructure.settings.environments import Environments


class SystemConfig(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="SYSTEM_")

    environment: Environments = Field(
        default=Environments.LOCAL,
        description="Environment of the system",
    )

    host: str = Field(
        description="Host of the system",
        default="",
    )
    port: int = Field(
        description="Port of the system",
        default=0,
    )

    application_name: str = Field(
        default="book-service",
        description="Application name",
    )

    executor: str = Field(
        default="",
        description="Executor of the system",
    )


class LogstashConfig(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="LOGSTASH_")

    host: str = Field(
        description="Logstash host",
        default="",
    )
    port: int = Field(
        description="Logstash port",
        default=0,
    )
    loggername: str = Field(
        default="book-service",
        description="Logstash logger name",
    )


class ProducerConfig(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="PRODUCER_")

    localhost: str = Field(
        description="Producer localhost",
        default="",
    )
    user: str = Field(
        description="Producer user",
        default="",
    )
    password: str = Field(
        description="Producer password",
        default="",
    )
    queues: Set[str] = Field(
        description="Producer queues",
        default={"book.creation"},
    )


class DatabaseConfig(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="DATABASE_")

    host: str = Field(
        description="Database host",
        default="",
    )
    password: str = Field(
        description="Database password",
        default="",
    )
    port: int = Field(
        description="Database port",
        default=0,
    )
    user: str = Field(
        description="Database user",
        default="",
    )
    database: str = Field(
        description="Database database",
        default="",
    )


class SlaveDatabaseConfig(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="DATABASE_SLAVE_")

    host: str = Field(
        description="Database slave host",
        default="",
    )
    port: int = Field(
        description="Database slave port",
        default=0,
    )
