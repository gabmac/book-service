from src.application.dto.book_dto import Book as BookDto
from src.application.ports.producer.book_producer import BookProducerPort
from src.domain.entities.book import Book


class CreateBookProduce:
    def __init__(self, producer: BookProducerPort):
        self.producer = producer

    async def execute(self, payload: BookDto) -> None:
        book = Book(
            isbn_code=payload.isbn_code,
            editor=payload.editor,
            edition=payload.edition,
            type=payload.type,
            publish_date=payload.publish_date,
            created_by=payload.user,
            updated_by=payload.user,
        )
        self.producer.upsert_book(book)
