import logging

from logstash_async.handler import AsynchronousLogstashHandler


class LogStash:
    logger = None

    def __init__(self, host: str, port: int, loggername: str):
        self.host = host
        self.port = port
        self.loggername = loggername

    def logstash_init(
        self,
    ) -> logging.Logger:
        if self.logger is None:
            self.logger = logging.getLogger(self.loggername)
            self.logger.setLevel(logging.INFO)
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
