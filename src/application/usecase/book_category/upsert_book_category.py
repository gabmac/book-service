from src.application.ports.database.book_category import BookCategoryRepositoryPort
from src.domain.entities.book_category import BookCategory


class UpsertBookCategory:
    def __init__(self, repository: BookCategoryRepositoryPort):
        self.book_category_producer = repository

    def execute(self, book_category: BookCategory) -> BookCategory:
        return self.book_category_producer.upsert_book_category(book_category)
