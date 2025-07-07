import time

from src.infrastructure.adapters.entrypoints.consumer import Consumer
from src.infrastructure.logs.logstash import LogStash
from src.infrastructure.settings.config import LogstashConfig, ProducerConfig

if __name__ == "__main__":
    logstash_config = LogstashConfig()
    handler = LogStash(
        logstash_config.host,
        logstash_config.port,
        logstash_config.loggername,
    )
    handler.logstash_init()
    cont = 0
    while cont <= 10:
        try:
            handler.logger.info("Starting consumer")  # type: ignore
            consumer = Consumer(
                config=ProducerConfig(),
                logstash_config=logstash_config,
            )
            break
        except Exception:
            time.sleep(3)
            cont += 1
            if cont == 10:
                raise Exception("Consumer not started")

    Consumer.start_consuming()
