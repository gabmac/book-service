from abc import ABC, abstractmethod
from uuid import UUID

from src.domain.entities.book_category import BookCategory


class BookCategoryRepositoryPort(ABC):

    @abstractmethod
    def upsert_book_category(self, book_category: BookCategory) -> BookCategory:
        pass

    @abstractmethod
    def delete_book_category(self, id: UUID) -> None:
        pass

    @abstractmethod
    def get_book_category_by_id(self, id: UUID) -> BookCategory:
        pass

    @abstractmethod
    def get_book_category_by_title(self, title: str) -> BookCategory:
        pass
