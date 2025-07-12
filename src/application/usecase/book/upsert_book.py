from src.application.exceptions import NotFoundException
from src.application.ports.database.book import BookRepositoryPort
from src.application.ports.producer.book_producer import BookProducerPort
from src.domain.entities.book import Book


class UpsertBook:
    def __init__(
        self,
        book_repository: BookRepositoryPort,
        book_producer: BookProducerPort,
    ):
        self.book_repository = book_repository
        self.book_producer = book_producer

    def execute(self, book: Book) -> Book:
        try:
            old_book = self.book_repository.get_book_by_id(book.id)
            book.created_at = old_book.created_at
            book.created_by = old_book.created_by
        except NotFoundException:
            pass
        finally:
            self.book_producer.notify_external_book_upsert(book)
            book = self.book_repository.upsert_book(book)

        return book
