from tests.unit.book_category.repository.conftest import BookCategoryRepositoryConftest


class TestUpsertBookCategory(BookCategoryRepositoryConftest):

    def test_new_book_category(self):
        # Arrange
        book_category = self.book_category_model_factory.build()

        # Act
        result = self.book_category_repository.upsert_book_category(
            book_category=book_category,
        )

        # Assert
        self.assertEqual(result, book_category)

    def test_update_book_category(self):
        # Arrange - Create and save a book category first
        book_category = self.book_category_model_factory.build()
        self.book_category_repository.upsert_book_category(book_category=book_category)

        # Act - Update the book category title
        book_category.title = "Updated Category"
        result = self.book_category_repository.upsert_book_category(
            book_category=book_category,
        )

        # Assert
        self.assertEqual(result, book_category)
