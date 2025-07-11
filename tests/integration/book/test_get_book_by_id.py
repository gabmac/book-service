import json

from tests.integration.book.conftest import BookViewConfTest
from uuid6 import uuid7


class TestGetBookById(BookViewConfTest):
    def setUp(self):
        super().setUp()

        # Create authors and categories
        author = self.author_model_factory.build(
            name="Test Author",
            created_by="test_user",
            updated_by="test_user",
        )
        category = self.book_category_model_factory.build(
            title="Test Category",
            description="Test description",
            created_by="test_user",
            updated_by="test_user",
        )

        self.stored_author = self.author_repository.upsert_author(author)
        self.stored_category = self.book_category_repository.upsert_book_category(
            category,
        )

        # Create a book
        book_data = [
            self.book_data_model_factory.build(
                title="Test Book Data",
                language="en",
                created_by="test_user",
                updated_by="test_user",
            ),
        ]
        book = self.book_model_factory.build(
            isbn_code="978-0-123456-78-9",
            editor="Test Editor",
            authors=[self.stored_author],
            book_categories=[self.stored_category],
            book_data=book_data,
            created_by="test_user",
            updated_by="test_user",
        )

        self.stored_book = self.book_repository.upsert_book(book)

    def test_get_book_by_id_success(self):
        # Scenario: Successfully get a book by ID

        # When a request is made to get the book by ID
        response = self.client.get(f"api/book/{self.stored_book.id}")

        # Then the response is a 200 status code
        self.assertEqual(response.status_code, 200)
        response_data = response.json()

        self.assertDictEqual(
            response_data,
            json.loads(self.stored_book.model_dump_json(exclude_none=True)),
        )

    def test_get_book_by_id_not_found(self):
        # Scenario: Attempt to get a book that doesn't exist

        # Given a book ID that doesn't exist

        non_existent_id = str(uuid7())

        # When a request is made to get the book by ID
        response = self.client.get(f"api/book/{non_existent_id}")

        # Then the response is a 404 status code
        self.assertEqual(response.status_code, 404)
        response_data = response.json()
        self.assertEqual(response_data["detail"], "Book not found")
