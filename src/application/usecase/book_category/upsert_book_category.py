from src.application.ports.database.book_category import BookCategoryWriteRepositoryPort
from src.domain.entities.book_category import BookCategory


class UpsertBookCategory:
    def __init__(self, repository: BookCategoryWriteRepositoryPort):
        self.repository = repository

    def execute(self, book_category: BookCategory) -> BookCategory:
        return self.repository.upsert_book_category(book_category)
