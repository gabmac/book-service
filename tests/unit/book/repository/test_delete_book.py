from tests.unit.book.repository.conftest import BookRepositoryConftest
from uuid6 import uuid7


class TestDeleteBook(BookRepositoryConftest):

    def test_delete_existing_book(self):
        # Arrange - Create and save a book# Arrange - Create and save a book first
        self.author1 = self.author_model_factory.build()
        self.author2 = self.author_model_factory.build()
        self.book_category1 = self.book_category_model_factory.build()
        self.book_category2 = self.book_category_model_factory.build()
        self.book_data1 = self.book_data_model_factory.build()
        self.book_data2 = self.book_data_model_factory.build()

        self.author_write_repository.upsert_author(author=self.author1)
        self.author_write_repository.upsert_author(author=self.author2)
        self.book_category_write_repository.upsert_book_category(
            book_category=self.book_category1,
        )
        self.book_category_write_repository.upsert_book_category(
            book_category=self.book_category2,
        )

        authors = [self.author1, self.author2]
        book_categories = [self.book_category1, self.book_category2]
        book_data = [self.book_data1, self.book_data2]
        book = self.book_model_factory.build(
            authors=authors,
            book_categories=book_categories,
            book_data=book_data,
        )

        # Act
        self.book_write_repository.upsert_book(book=book)

        # Act - Delete the book
        self.book_write_repository.delete_book(id=str(book.id))

    def test_delete_non_existent_book(self):
        # Arrange - Generate a random UUID that doesn't exist

        # Act - Should not raise error for non-existent book
        self.book_write_repository.delete_book(id=str(uuid7()))
