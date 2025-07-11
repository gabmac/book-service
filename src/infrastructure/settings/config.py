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


class ElasticsearchConfig(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="ELASTICSEARCH_")

    host: str = Field(
        description="Elasticsearch host",
        default="",
    )
    port: int = Field(
        description="Elasticsearch port",
        default=0,
    )
    username: str = Field(
        description="Elasticsearch username",
        default="",
    )
    password: str = Field(
        description="Elasticsearch password",
        default="",
    )
    use_ssl: bool = Field(
        description="Use SSL for Elasticsearch connection",
        default=False,
    )
    verify_certs: bool = Field(
        description="Verify SSL certificates",
        default=True,
    )
    timeout: int = Field(
        description="Connection timeout in seconds",
        default=30,
    )
    max_retries: int = Field(
        description="Maximum number of retries",
        default=3,
    )
    retry_on_timeout: bool = Field(
        description="Retry on timeout",
        default=True,
    )


class ElasticsearchIndexConfig(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="ELASTICSEARCH_INDEX_")

    books_index: str = Field(
        description="Index name for books with all nested data",
        default="books",
    )
    mappings_file_path: str = Field(
        description="Path to the JSON file containing Elasticsearch mappings",
        default="",
    )
    number_of_shards: int = Field(
        description="Number of primary shards for the index",
        default=1,
    )
    number_of_replicas: int = Field(
        description="Number of replica shards for the index",
        default=1,
    )
    max_result_window: int = Field(
        description="Maximum number of documents that can be returned in a single query",
        default=10000,
    )
    refresh_interval: str = Field(
        description="How often to refresh the index",
        default="1s",
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
        default={
            "book.upsert",
            "author.upsert",
            "book_category.upsert",
            "book.deletion",
            "author.deletion",
            "branch.upsert",
            "physical_exemplar.upsert",
        },
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
