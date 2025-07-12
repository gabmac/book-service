import json
from uuid import UUID

from src.application.dto.producer import Message
from src.application.ports.producer.author_producer import AuthorProducerPort
from src.domain.entities.author import Author
from src.infrastructure.adapters.entrypoints.producer import Producer


class AuthorProducerAdapter(AuthorProducerPort):
    def __init__(self, producer: Producer):
        self.producer = producer

    def upsert_author(self, author: Author) -> None:
        self.producer.publish(
            message=Message(
                queue_name="author.upsert",
                message=author.model_dump_json(),
            ),
        )

    def delete_author(self, id: UUID) -> None:
        self.producer.publish(
            message=Message(
                queue_name="author.deletion",
                message=json.dumps({"id": str(id)}),
            ),
        )

    def notify_external_author_upsert(self, author: Author) -> None:
        self.producer.publish(
            message=Message(
                queue_name="external.author.upsert",
                message=author.model_dump_json(),
            ),
        )

    def notify_external_author_deletion(self, id: UUID) -> None:
        self.producer.publish(
            message=Message(
                queue_name="external.author.deletion",
                message=json.dumps({"id": str(id)}),
            ),
        )
