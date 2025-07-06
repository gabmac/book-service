from typing import List

from src.application.ports.database.book import BookRepositoryPort
from src.domain.entities.book import Book, BookFilter


class FilterBook:
    def __init__(self, book_repository: BookRepositoryPort):
        self.book_repository = book_repository

    def execute(self, filter: BookFilter) -> List[Book]:
        return self.book_repository.get_book_by_filter(filter)
