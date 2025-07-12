from uuid import UUID

from src.application.ports.database.book import BookReadRepositoryPort
from src.domain.entities.book import Book


class GetBookById:
    def __init__(self, book_repository: BookReadRepositoryPort):
        self.book_repository = book_repository

    def execute(self, id: UUID) -> Book:
        book = self.book_repository.get_book_by_id(id)
        return Book.model_validate(book)
