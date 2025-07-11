from typing import Optional

from elasticsearch import Elasticsearch
from elasticsearch.exceptions import ConnectionError

from src.infrastructure.settings.config import ElasticsearchConfig


class ElasticsearchClient:
    """Elasticsearch client wrapper for connection management"""

    _instance = None
    _client: Optional[Elasticsearch] = None
    _config: Optional[ElasticsearchConfig] = None

    def __new__(cls, config: ElasticsearchConfig):  # type: ignore
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._config = config
            cls._instance._client = cls._instance._create_client()
        return cls._instance

    @property
    def client(self) -> Elasticsearch:
        """Get the Elasticsearch client instance"""
        if self._client is None:
            self._client = self._create_client()
        return self._client

    @property
    def config(self) -> ElasticsearchConfig:
        """Get the Elasticsearch configuration"""
        if self._config is None:
            raise ValueError("ElasticsearchClient not properly initialized")
        return self._config

    def _create_client(self) -> Elasticsearch:
        """Create Elasticsearch client with configuration"""
        if self._config is None:
            raise ValueError("ElasticsearchClient not properly initialized")

        scheme = "https" if self._config.use_ssl else "http"
        connection_params = {
            "hosts": [
                {
                    "host": self._config.host,
                    "port": self._config.port,
                    "scheme": scheme,
                },
            ],
            "request_timeout": self._config.timeout,
            "max_retries": self._config.max_retries,
            "retry_on_timeout": self._config.retry_on_timeout,
            # Force compatibility with Elasticsearch 8.x
            "headers": {
                "Accept": "application/vnd.elasticsearch+json; compatible-with=8",
            },
        }

        # Add authentication if provided
        if self._config.username and self._config.password:
            connection_params["http_auth"] = (
                self._config.username,
                self._config.password,
            )

        # Add SSL configuration
        if self._config.use_ssl:
            connection_params["use_ssl"] = True
            connection_params["verify_certs"] = self._config.verify_certs

        return Elasticsearch(**connection_params)  # type: ignore

    def ping(self) -> bool:
        """Test connection to Elasticsearch"""
        try:
            if self.client:
                self.client.ping()
                return True
        except ConnectionError:
            return False

        return False

    def get_cluster_health(self) -> None:
        """Get cluster health information"""
        try:
            self.client.cluster.health()
        except ConnectionError as e:
            raise ConnectionError(f"Failed to get cluster health: {e}")

    def close(self) -> None:
        """Close the Elasticsearch connection"""
        if self._client is not None:
            self._client.close()
            self._client = None
