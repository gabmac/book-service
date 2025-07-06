from src.application.ports.database.book import BookRepositoryPort
from src.application.ports.usecase.consumer import ConsumerUsecase
from src.domain.entities.book import Book


class UpsertBook(ConsumerUsecase):
    def __init__(self, book_repository: BookRepositoryPort):
        self.book_repository = book_repository

    def execute(self, payload: bytes) -> None:
        data = self._convert_to_json(payload)
        book = Book.model_validate(data)
        self.book_repository.upsert_book(book)
