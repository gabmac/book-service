from uuid import UUID

from fastapi import HTTPException

from src.application.exceptions import NotFoundException
from src.application.ports.database.book import BookRepositoryPort
from src.domain.entities.book import Book


class GetBookById:
    def __init__(self, book_repository: BookRepositoryPort):
        self.book_repository = book_repository

    def execute(self, id: UUID) -> Book:
        try:
            book = self.book_repository.get_book_by_id(id)
            return Book.model_validate(book)
        except NotFoundException as e:
            raise HTTPException(status_code=404, detail=e.message)
