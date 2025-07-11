from tests.unit.book_category.repository.conftest import BookCategoryRepositoryConftest
from uuid6 import uuid7


class TestDeleteBookCategory(BookCategoryRepositoryConftest):

    def test_delete_existing_book_category(self):
        # Arrange - Create and save a book category
        book_category = self.book_category_model_factory.build()
        self.book_category_repository.upsert_book_category(book_category=book_category)

        # Act - Delete the book category
        self.book_category_repository.delete_book_category(id=book_category.id)

    def test_delete_non_existent_book_category(self):
        # Arrange - Generate a random UUID that doesn't exist

        self.book_category_repository.delete_book_category(id=uuid7())
