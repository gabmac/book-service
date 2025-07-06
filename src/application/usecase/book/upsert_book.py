import json

from src.application.dto.producer import Message
from src.application.exceptions import NotFoundException
from src.application.ports.database.book import BookRepositoryPort
from src.domain.entities.book import Book


class UpsertBook:
    def __init__(self, book_repository: BookRepositoryPort):
        self.book_repository = book_repository

    def execute(self, payload: Message) -> Book:
        book = Book.model_validate(json.loads(payload.message))
        try:
            old_book = self.book_repository.get_book_by_id(book.id)
            book.created_at = old_book.created_at
            book.created_by = old_book.created_by
        except NotFoundException:
            book = Book.model_validate(json.loads(payload.message))
        finally:
            book = self.book_repository.upsert_book(book)

        return book
