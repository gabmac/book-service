import json

from src.application.dto.producer import Message
from src.application.ports.database.book import BookRepositoryPort
from src.domain.entities.book import Book


class UpsertBook:
    def __init__(self, book_repository: BookRepositoryPort):
        self.book_repository = book_repository

    def execute(self, payload: Message) -> None:
        book = Book.model_validate(json.loads(payload.message))
        self.book_repository.upsert_book(book)
