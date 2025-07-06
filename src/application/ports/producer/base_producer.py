from src.application.dto.producer import Message
from src.infrastructure.adapters.entrypoints.producer import Producer


class BaseProducerPort:
    def __init__(self, producer: Producer):
        self.producer = producer

    def publish(self, message: Message) -> None:
        self.producer.publish(message)
