from uuid import UUID

from tests.integration.book.conftest import BookViewConfTest

from src.application.exceptions import NotFoundException


class TestDeleteBook(BookViewConfTest):
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

        self.stored_author = self.author_write_repository.upsert_author(author)
        self.stored_category = self.book_category_write_repository.upsert_book_category(
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

        self.stored_book = self.book_write_repository.upsert_book(book)

    def test_delete_book_success(self):
        # Scenario: Successfully delete an existing book

        # When a request is made to delete the book
        response = self.client.delete(
            "api/book",
            params={"id": str(self.stored_book.id)},
        )

        # Then the response is a 202 status code (task is processing)
        self.assertEqual(response.status_code, 202)

        # And the message is consumed from the queue
        self.consumer.consume("book.deletion")

        # Verify the book details in the response
        with self.assertRaises(NotFoundException):
            self.book_read_repository.get_book_by_id(self.stored_book.id)

    def test_delete_book_not_found(self):
        # Scenario: Attempt to delete a book that doesn't exist

        # Given a book ID that doesn't exist
        non_existent_id = "11111111-1111-1111-1111-111111111111"

        # When a request is made to delete the book by ID
        response = self.client.delete("api/book", params={"id": non_existent_id})

        # Then the response is a 404 status code
        self.assertEqual(response.status_code, 202)
        self.consumer.consume("book.deletion")

        # Verify the book details in the response
        with self.assertRaises(NotFoundException):
            self.book_read_repository.get_book_by_id(UUID(non_existent_id))
