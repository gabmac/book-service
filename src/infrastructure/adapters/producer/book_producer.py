import json
from uuid import UUID

from src.application.dto.producer import Message
from src.application.ports.producer.book_producer import BookProducerPort
from src.domain.entities.book import Book
from src.infrastructure.adapters.entrypoints.producer import Producer


class BookProducerAdapter(BookProducerPort):
    def __init__(self, producer: Producer):
        self.producer = producer

    def upsert_book(self, book: Book) -> None:
        self.producer.publish(
            message=Message(
                queue_name="book.upsert",
                message=book.model_dump_json(),
            ),
        )

    def delete_book(self, id: UUID) -> None:
        self.producer.publish(
            message=Message(
                queue_name="book.deletion",
                message=json.dumps({"id": str(id)}),
            ),
        )

    def notify_external_book_upsert(self, book: Book) -> None:
        self.producer.publish(
            message=Message(
                queue_name="external.book.upsert",
                message=book.model_dump_json(),
            ),
        )

    def notify_external_book_deletion(self, id: UUID) -> None:
        self.producer.publish(
            message=Message(
                queue_name="external.book.deletion",
                message=json.dumps({"id": str(id)}),
            ),
        )
