from typing import Optional

from src.application.exceptions import OptimisticLockException
from src.application.ports.database.book import (
    BookWriteRepositoryPort,
)
from src.application.ports.producer.book_producer import BookProducerPort
from src.domain.entities.book import Book


class UpsertBook:
    def __init__(
        self,
        book_write_repository: BookWriteRepositoryPort,
        book_producer: BookProducerPort,
    ):
        self.book_write_repository = book_write_repository
        self.book_producer = book_producer

    def execute(self, book: Book) -> Optional[Book]:
        self.book_producer.notify_external_book_upsert(book)
        try:
            book = self.book_write_repository.upsert_book(book)
        except OptimisticLockException:
            return None

        return book
