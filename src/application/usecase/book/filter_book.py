from typing import List

from src.application.dto.book_dto import BookFilter
from src.application.ports.database.book import BookRepositoryPort
from src.domain.entities.book import Book, BookSearchFilter


class FilterBook:
    def __init__(self, book_repository: BookRepositoryPort):
        self.book_repository = book_repository

    def execute(self, filter: BookFilter | None = None) -> List[Book]:
        # Convert DTO to entity
        search_filter = self._convert_dto_to_entity(filter)
        return self.book_repository.get_book_by_filter(search_filter)

    def _convert_dto_to_entity(
        self,
        dto_filter: BookFilter | None,
    ) -> BookSearchFilter:
        """Convert BookFilter DTO to BookSearchFilter entity"""
        if dto_filter is None:
            return BookSearchFilter(
                page=1,
                size=10,
                sort_by="created_at",
                sort_order="desc",
            )

        return BookSearchFilter.model_validate(dto_filter)
