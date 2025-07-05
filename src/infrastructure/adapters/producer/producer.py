from typing import Set

from pika import BlockingConnection, ConnectionParameters, PlainCredentials
from pika.adapters.blocking_connection import BlockingChannel


class Producer:
    _instance = None
    _localhost = None
    _connection = None
    _channel: BlockingChannel | None = None
    _queues: Set[str] = set()

    def __new__(  # type: ignore
        cls,
        localhost: str,
        queues: Set[str],
        user: str,
        password: str,
    ):
        if cls._instance is None:
            cls._localhost = localhost
            cls._queues = queues
            credential = PlainCredentials(user, password)
            cls._connection = BlockingConnection(
                ConnectionParameters(cls._localhost, credentials=credential),
            )
            cls._channel = cls._connection.channel()
            cls._instance = cls
            _ = [cls._channel.queue_declare(queue=queue) for queue in cls._queues]

        return cls._instance

    def publish(self, queue: str, message: str) -> None:
        if self._channel is not None:
            self._channel.basic_publish(exchange="", routing_key=queue, body=message)

    def close(self) -> None:
        if self._connection is not None:
            self._connection.close()
