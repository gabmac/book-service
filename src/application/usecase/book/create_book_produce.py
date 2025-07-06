from src.application.dto.book_dto import Book as BookDto
from src.application.dto.producer import Message
from src.domain.entities.book import Book
from src.infrastructure.adapters.entrypoints.producer import Producer


class CreateBookProduce:
    def __init__(self, producer: Producer):
        self.producer = producer

    async def execute(self, payload: BookDto) -> None:
        book = Book.model_validate(payload)
        self.producer.publish(
            message=Message(
                queue_name="book.creation",
                message=book.model_dump_json(),
            ),
        )
