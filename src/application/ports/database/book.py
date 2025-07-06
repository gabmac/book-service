from abc import ABC, abstractmethod

from src.domain.entities.book import Book
from src.infrastructure.adapters.database.db.session import DatabaseSettings


class BookRepositoryPort(ABC):
    def __init__(self, db: DatabaseSettings) -> None:
        self.db = db

    @abstractmethod
    def upsert_book(self, book: Book) -> None:
        pass
