from uuid import UUID

from src.application.dto.producer import Message
from src.application.ports.producer.book_category_producer import (
    BookCategoryProducerPort,
)
from src.domain.entities.book_category import BookCategory
from src.infrastructure.adapters.entrypoints.producer import Producer


class BookCategoryProducerAdapter(BookCategoryProducerPort):
    def __init__(self, producer: Producer):
        self.producer = producer

    def upsert_book_category(self, book_category: BookCategory) -> None:
        self.producer.publish(
            message=Message(
                queue_name="book_category.upsert",
                message=book_category.model_dump_json(),
            ),
        )

    def delete_book_category(self, id: UUID) -> None:
        self.producer.publish(
            message=Message(
                queue_name="book_category.delete",
                message=str(id),
            ),
        )
