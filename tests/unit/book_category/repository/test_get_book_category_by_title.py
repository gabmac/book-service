from tests.unit.book_category.repository.conftest import BookCategoryRepositoryConftest

from src.application.exceptions import NotFoundException


class TestGetBookCategoryByTitle(BookCategoryRepositoryConftest):

    def test_get_existing_book_category_by_title(self):
        # Arrange - Create and save a book category first
        book_category = self.book_category_model_factory.build(title="Science Fiction")
        self.book_category_write_repository.upsert_book_category(
            book_category=book_category,
        )

        # Act - Retrieve the book category by title
        result = self.book_category_read_repository.get_book_category_by_title(
            title="Science Fiction",
        )

        # Assert - Verify the book category is returned correctly
        self.assertEqual(result, book_category)

    def test_get_non_existent_book_category_by_title(self):
        # Arrange - Create and save a book category with different title
        book_category = self.book_category_model_factory.build(title="Fantasy")
        self.book_category_write_repository.upsert_book_category(
            book_category=book_category,
        )

        # Act & Assert - Should raise NotFoundException for non-existent title
        with self.assertRaises(NotFoundException) as context:
            self.book_category_read_repository.get_book_category_by_title(
                title="NonExistentCategory",
            )

        self.assertEqual(str(context.exception), "Book category not found")
