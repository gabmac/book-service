from src.application.dto.book_dto import Book
from src.infrastructure.adapters.entrypoints.producer import Producer


class CreateBookProduce:
    def __init__(self, producer: Producer):
        self.producer = producer

    async def execute(self, payload: Book) -> None:
        self.producer.publish(
            queue_name="book.creation",
            message=payload.model_dump_json(),
        )
