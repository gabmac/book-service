from src.application.ports.producer.book_producer import BookProducerPort
from src.domain.entities.book import Book


class CreateBookProduce:
    def __init__(self, producer: BookProducerPort):
        self.producer = producer

    async def execute(self, payload: Book) -> Book:
        book = Book(
            isbn_code=payload.isbn_code,
            editor=payload.editor,
            edition=payload.edition,
            type=payload.type,
            publish_date=payload.publish_date,
            created_by=payload.created_by,
            updated_by=payload.updated_by,
        )
        self.producer.upsert_book(book)

        return book
