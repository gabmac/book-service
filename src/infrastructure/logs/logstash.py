import logging

from logstash_async.handler import SynchronousLogstashHandler


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
                SynchronousLogstashHandler(
                    host=self.host,
                    port=self.port,
                    ssl_enable=False,
                    ssl_verify=False,
                ),
            )

        return self.logger
