from tests.unit.book_category.repository.conftest import BookCategoryRepositoryConftest

from src.application.exceptions import OptimisticLockException


class TestUpsertBookCategory(BookCategoryRepositoryConftest):

    def test_new_book_category(self):
        # Arrange
        book_category = self.book_category_model_factory.build()

        # Act
        result = self.book_category_write_repository.upsert_book_category(
            book_category=book_category,
        )

        # Assert
        self.assertEqual(result, book_category)

    def test_update_book_category(self):
        # Arrange - Create and save a book category first
        book_category = self.book_category_model_factory.build(version=3)
        self.book_category_write_repository.upsert_book_category(
            book_category=book_category,
        )

        # Act - Update the book category title
        book_category.title = "Updated Category"
        book_category.version = book_category.version + 1
        result = self.book_category_write_repository.upsert_book_category(
            book_category=book_category,
        )

        # Assert
        self.assertEqual(result, book_category)

    def test_update_book_category_with_optimistic_lock(self):
        # Arrange - Create and save a book category first
        book_category = self.book_category_model_factory.build(version=4)
        self.book_category_write_repository.upsert_book_category(
            book_category=book_category,
        )

        # Act - Update the book category title
        book_category.title = "Updated Category"
        book_category.version = book_category.version - 1

        # Assert - Should raise OptimisticLockException
        with self.assertRaises(OptimisticLockException):
            self.book_category_write_repository.upsert_book_category(
                book_category=book_category,
            )
