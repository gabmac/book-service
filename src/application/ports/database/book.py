from abc import ABC, abstractmethod
from typing import List
from uuid import UUID

from src.application.dto.book_dto import BookFilter
from src.domain.entities.book import Book
from src.infrastructure.adapters.database.db.session import DatabaseSettings


class BookRepositoryPort(ABC):
    def __init__(self, db: DatabaseSettings) -> None:
        self.db = db

    @abstractmethod
    def upsert_book(self, book: Book) -> None:
        pass

    @abstractmethod
    def get_book_by_id(self, id: UUID) -> Book:
        pass

    @abstractmethod
    def get_book_by_filter(self, filter: BookFilter) -> List[Book]:
        pass
