import json
from datetime import date

from src.domain.entities.book import Book
from tests.integration.book.conftest import BookViewConfTest

from src.domain.enums.book_type import BookType


class TestFilterBook(BookViewConfTest):

    def setUp(self):
        super().setUp()

        # Create authors and categories
        author1 = self.author_model_factory.build(
            name="Science Author",
            created_by="test_user",
            updated_by="test_user",
        )
        author2 = self.author_model_factory.build(
            name="Fiction Writer",
            created_by="test_user",
            updated_by="test_user",
        )

        category1 = self.book_category_model_factory.build(
            title="Science Fiction",
            description="Science fiction books",
            created_by="test_user",
            updated_by="test_user",
        )
        category2 = self.book_category_model_factory.build(
            title="Fantasy",
            description="Fantasy books",
            created_by="test_user",
            updated_by="test_user",
        )

        self.stored_author1 = self.author_repository.upsert_author(author1)
        self.stored_author2 = self.author_repository.upsert_author(author2)
        self.stored_category1 = self.book_category_repository.upsert_book_category(
            category1,
        )
        self.stored_category2 = self.book_category_repository.upsert_book_category(
            category2,
        )

        # Create books with different properties
        book_data1 = [
            self.book_data_model_factory.build(
                title="Book Data 1",
                language="en",
                created_by="test_user",
                updated_by="test_user",
            ),
        ]
        book_data2 = [
            self.book_data_model_factory.build(
                title="Book Data 2",
                language="es",
                created_by="test_user",
                updated_by="test_user",
            ),
        ]

        book1 = self.book_model_factory.build(
            isbn_code="978-0-123456-78-9",
            editor="Science Publisher",
            edition=1,
            type=BookType.PHYSICAL,
            publish_date=date(2023, 1, 1),
            authors=[self.stored_author1],
            book_categories=[self.stored_category1],
            book_data=book_data1,
            created_by="test_user",
            updated_by="test_user",
        )

        book2 = self.book_model_factory.build(
            isbn_code="978-0-987654-32-1",
            editor="Fantasy House",
            edition=2,
            type=BookType.EBOOK,
            publish_date=date(2023, 6, 15),
            authors=[self.stored_author2],
            book_categories=[self.stored_category2],
            book_data=book_data2,
            created_by="test_user",
            updated_by="test_user",
        )

        # Store books in database
        self.stored_book1 = self.book_repository.upsert_book(book1)
        self.stored_book2 = self.book_repository.upsert_book(book2)

    def test_filter_book_with_multiple_filters(self):

        # Scenario: Filter books by multiple criteria

        # Given books are stored in the database

        # When a request is made to filter books by multiple fields
        response = self.client.get(
            "api/book",
            params={
                "isbn_code": "978-0-123456-78-9",
                "editor": "Science Publisher",
                "edition": 1,
                "type": "physical",
            },
        )

        # Then the response is a 200 status code
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        response_book = Book.model_validate(response_data[0])

        # And the response should list books that match all filters
        self.validate_book([response_book],[self.stored_book1])
        
    def test_filter_book_no_results(self):

        # Scenario: Filter books with no matches

        # Given books are stored in the database

        # When a request is made to filter books by non-existent criteria
        response = self.client.get(
            "api/book",
            params={
                "isbn_code": "978-0-000000-00-0",
                "editor": "NonExistent Publisher",
            },
        )

        # Then the response is a 200 status code
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertEqual(len(response_data), 0)

    def test_filter_book_no_filter(self):

        # Scenario: Get all books without filters

        # Given books are stored in the database

        # When a request is made without any filters
        response = self.client.get("api/book")

        # Then the response is a 200 status code
        self.assertEqual(response.status_code, 200)
        response_data = response.json()

        # And the response should list all books
        expected_books = [self.stored_book1, self.stored_book2]

        response_book = [Book.model_validate(book) for book in response_data]
        self.validate_book(response_book, expected_books)
