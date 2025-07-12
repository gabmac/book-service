from abc import ABC, abstractmethod
from typing import List
from uuid import UUID

from src.domain.entities.book import Book, BookSearchFilter
from src.infrastructure.adapters.database.db.session import DatabaseSettings


class BookReadRepositoryPort(ABC):
    def __init__(self, db: DatabaseSettings) -> None:
        self.db = db

    @abstractmethod
    def get_book_by_id(self, id: UUID) -> Book:
        pass

    @abstractmethod
    def get_book_by_filter(
        self,
        filter: BookSearchFilter,
    ) -> List[Book]:
        pass


class BookWriteRepositoryPort(ABC):
    def __init__(self, db: DatabaseSettings) -> None:
        self.db = db

    @abstractmethod
    def upsert_book(self, book: Book) -> Book:
        pass

    @abstractmethod
    def delete_book(self, id: str) -> None:
        pass
