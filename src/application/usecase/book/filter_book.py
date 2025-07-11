from typing import List

from src.application.dto.book_dto import BookFilter
from src.application.ports.database.book import BookRepositoryPort
from src.domain.entities.book import Book, BookSearchFilter


class FilterBook:
    def __init__(self, book_repository: BookRepositoryPort):
        self.book_repository = book_repository

    def execute(self, filter: BookFilter) -> List[Book]:
        # Convert DTO to entity
        search_filter = self._convert_dto_to_entity(filter)
        return self.book_repository.get_book_by_filter(search_filter)
    
    def _convert_dto_to_entity(self, dto_filter: BookFilter) -> BookSearchFilter:
        """Convert BookFilter DTO to BookSearchFilter entity"""
        return BookSearchFilter(
            isbn_code=dto_filter.isbn_code,
            editor=dto_filter.editor,
            edition=dto_filter.edition,
            type=dto_filter.type,
            publish_date_from=dto_filter.publish_date,
            publish_date_to=dto_filter.publish_date,
            author_name=dto_filter.author_name,
            category_title=dto_filter.book_category_name,
        )
