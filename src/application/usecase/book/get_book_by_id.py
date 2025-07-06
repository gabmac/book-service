from uuid import UUID

from fastapi import HTTPException

from src.application.dto.book_dto import BookResponse
from src.application.exceptions import NotFoundException
from src.application.ports.database.book import BookRepositoryPort


class GetBookById:
    def __init__(self, book_repository: BookRepositoryPort):
        self.book_repository = book_repository

    def execute(self, id: UUID) -> BookResponse:
        try:
            book = self.book_repository.get_book_by_id(id)
            return BookResponse.model_validate(book)
        except NotFoundException as e:
            raise HTTPException(status_code=404, detail=e.message)
