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
                queue_name="author.creation",
                message=author.model_dump_json(),
            ),
        )

    def delete_author(self, id: UUID) -> None:
        self.producer.publish(
            message=Message(
                queue_name="author.deletion",
                message=str(id),
            ),
        )
