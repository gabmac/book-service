from src.application.exceptions import NotFoundException
from src.application.ports.database.book_category import BookCategoryReadRepositoryPort
from src.application.ports.producer.book_category_producer import (
    BookCategoryProducerPort,
)
from src.domain.entities.book_category import BookCategory


class CreateBookCategoryProduce:
    def __init__(
        self,
        book_category_producer: BookCategoryProducerPort,
        repository: BookCategoryReadRepositoryPort,
    ):
        self.book_category_producer = book_category_producer
        self.repository = repository

    def execute(self, book_category: BookCategory) -> BookCategory:
        try:
            old_book_category = self.repository.get_book_category_by_title(
                book_category.title,
            )
            new_book_category = BookCategory(
                id=old_book_category.id,
                title=book_category.title,
                version=old_book_category.version + 1,
                description=book_category.description,
                created_by=old_book_category.created_by,
                created_at=old_book_category.created_at,
                updated_by=book_category.updated_by,
                updated_at=book_category.updated_at,
            )
        except NotFoundException:
            new_book_category = BookCategory.model_validate(book_category)
        finally:
            self.book_category_producer.upsert_book_category(new_book_category)
            return new_book_category
