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
