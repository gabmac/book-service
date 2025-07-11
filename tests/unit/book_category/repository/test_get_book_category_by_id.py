from tests.unit.book_category.repository.conftest import BookCategoryRepositoryConftest
from uuid6 import uuid7

from src.application.exceptions import NotFoundException


class TestGetBookCategoryById(BookCategoryRepositoryConftest):

    def test_get_existing_book_category(self):
        # Arrange - Create and save a book category first
        book_category = self.book_category_model_factory.build()
        self.book_category_repository.upsert_book_category(book_category=book_category)

        # Act - Retrieve the book category by ID
        result = self.book_category_repository.get_book_category_by_id(
            id=book_category.id,
        )

        # Assert - Verify the book category is returned correctly
        self.assertEqual(result, book_category)

    def test_get_non_existent_book_category(self):
        # Arrange - Generate a random UUID that doesn't exist
        non_existent_id = uuid7()

        # Act & Assert - Should raise NotFoundException
        with self.assertRaises(NotFoundException) as context:
            self.book_category_repository.get_book_category_by_id(id=non_existent_id)

        self.assertEqual(str(context.exception), "Book category not found")
