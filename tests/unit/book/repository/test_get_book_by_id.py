from uuid import uuid4

from tests.unit.book.repository.conftest import BookRepositoryConftest

from src.application.exceptions import NotFoundException


class TestGetBookById(BookRepositoryConftest):

    def test_get_existing_book(self):
        # Arrange - Create and save a book first
        self.author1 = self.author_model_factory.build()
        self.author2 = self.author_model_factory.build()
        self.book_category1 = self.book_category_model_factory.build()
        self.book_category2 = self.book_category_model_factory.build()
        self.book_data1 = self.book_data_model_factory.build()
        self.book_data2 = self.book_data_model_factory.build()

        self.author_repository.upsert_author(author=self.author1)
        self.author_repository.upsert_author(author=self.author2)
        self.book_category_repository.upsert_book_category(
            book_category=self.book_category1,
        )
        self.book_category_repository.upsert_book_category(
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
        self.book_repository.upsert_book(book=book)

        # Act - Retrieve the book by ID
        result = self.book_repository.get_book_by_id(id=book.id)

        # Assert - Verify the book is returned correctly
        exclude_book = {"book_data", "category_ids", "author_ids"}
        exclude_book_data = {"created_at", "created_by", "updated_at", "updated_by"}
        # Assert
        self.assertEqual(
            result.model_dump(exclude=exclude_book),
            book.model_dump(exclude=exclude_book),
        )
        self.assertEqual(result.authors, authors)
        self.assertEqual(result.book_categories, book_categories)
        self.assertEqual(
            sorted(
                (
                    book_data.model_dump(exclude=exclude_book_data)
                    for book_data in result.book_data
                ),
                key=lambda x: x["id"],
            ),  # type: ignore
            sorted(
                (
                    book_data.model_dump(exclude=exclude_book_data)
                    for book_data in book.book_data
                ),
                key=lambda x: x["id"],
            ),
        )

    def test_get_non_existent_book(self):
        # Arrange - Generate a random UUID that doesn't exist
        non_existent_id = uuid4()

        # Act & Assert - Should raise NotFoundException
        with self.assertRaises(NotFoundException) as context:
            self.book_repository.get_book_by_id(id=non_existent_id)

        self.assertEqual(str(context.exception), "Book not found")
