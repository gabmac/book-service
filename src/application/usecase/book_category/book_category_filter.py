from typing import List

from src.application.ports.database.book_category import BookCategoryReadRepositoryPort
from src.domain.entities.book_category import BookCategory, BookCategoryFilter


class FilterBookCategory:
    def __init__(self, repository: BookCategoryReadRepositoryPort):
        self.repository = repository

    def execute(self, filter: BookCategoryFilter) -> List[BookCategory]:
        return self.repository.get_book_category_by_filter(filter)
