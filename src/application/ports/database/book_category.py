from abc import ABC, abstractmethod
from typing import List
from uuid import UUID

from src.domain.entities.book_category import BookCategory, BookCategoryFilter


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

    @abstractmethod
    def get_book_category_by_filter(
        self,
        filter: BookCategoryFilter,
    ) -> List[BookCategory]:
        pass

    @abstractmethod
    def get_book_categories_by_ids(self, ids: List[UUID]) -> List[BookCategory]:
        pass
