import logging

from logstash_async.handler import AsynchronousLogstashHandler

from src.infrastructure.settings.environments import Environments


class LogStash:
    logger = None

    def __init__(self, host: str, port: int, loggername: str, environment: str):
        self.host = host
        self.port = port
        self.loggername = loggername
        self.environment = environment

    def logstash_init(
        self,
    ) -> logging.Logger:
        if self.logger is None:
            self.logger = logging.getLogger(self.loggername)
            self.logger.setLevel(logging.INFO)
            if self.environment != Environments.TEST:
                self.logger.addHandler(
                    AsynchronousLogstashHandler(
                        host=self.host,
                        port=self.port,
                        ssl_enable=False,
                        ssl_verify=False,
                        database_path=None,
                    ),
                )

        return self.logger
