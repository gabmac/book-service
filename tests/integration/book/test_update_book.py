import json

from tests.integration.book.conftest import BookViewConfTest

from src.application.dto.book_dto import ProcessingBook


class TestUpdateBook(BookViewConfTest):
    def setUp(self):
        super().setUp()

        # Create initial authors and categories
        self.original_author = self.author_model_factory.build(
            name="Original Author",
            created_by="test_user",
            updated_by="test_user",
        )
        self.original_category = self.book_category_model_factory.build(
            title="Original Category",
            description="Original description",
            created_by="test_user",
            updated_by="test_user",
        )

        self.stored_original_author = self.author_repository.upsert_author(
            self.original_author,
        )
        self.stored_original_category = (
            self.book_category_repository.upsert_book_category(self.original_category)
        )

        # Create an existing book
        existing_book_data = [
            self.book_data_model_factory.build(
                title="Original Book Data",
                language="en",
                created_by="test_user",
                updated_by="test_user",
            ),
        ]
        existing_book = self.book_model_factory.build(
            isbn_code="978-0-123456-78-9",
            editor="Original Editor",
            authors=[self.stored_original_author],
            book_categories=[self.stored_original_category],
            book_data=existing_book_data,
            created_by="test_user",
            updated_by="test_user",
        )
        self.stored_book = self.book_repository.upsert_book(existing_book)

        # Create new authors and categories for the update
        self.new_author = self.author_model_factory.build(
            name="Updated Author",
            created_by="test_user",
            updated_by="test_user",
        )
        self.new_category = self.book_category_model_factory.build(
            title="Updated Category",
            description="Updated description",
            created_by="test_user",
            updated_by="test_user",
        )

        self.stored_new_author = self.author_repository.upsert_author(self.new_author)
        self.stored_new_category = self.book_category_repository.upsert_book_category(
            self.new_category,
        )

    def test_update_book_success(self):
        # Scenario: Successfully update an existing book

        # When a request is made to update the book
        update_body = self.book_dto_model_factory.build(
            isbn_code="978-0-987654-32-1",
            editor="Updated Editor",
            author_ids=[self.stored_new_author.id],
            category_ids=[self.stored_new_category.id],
        )
        response = self.client.put(
            "api/book",
            json=json.loads(update_body.model_dump_json()),
            params={"id": str(self.stored_book.id)},
        )

        # Then the response is a 202 status code (task is processing)
        self.assertEqual(response.status_code, 202)
        response_body = ProcessingBook.model_validate_json(json.dumps(response.json()))
        self.assertEqual(response_body.message, "Task is processing")

        # And the message is consumed from the queue
        self.consumer.consume("book.upsert")

        # And the book is updated in the database
        exclude_book = {"book_data", "updated_at", "created_at", "create"}
        updated_book = self.book_repository.get_book_by_id(self.stored_book.id)
        self.assertDictEqual(
            json.loads(
                response_body.book.model_dump_json(
                    exclude_none=True,
                    exclude_unset=True,
                    exclude=exclude_book,
                ),
            ),
            json.loads(
                updated_book.model_dump_json(
                    exclude_none=True,
                    exclude_unset=True,
                    exclude=exclude_book,
                ),
            ),
        )

        exclude_book_data = {"created_at", "created_by", "updated_at", "updated_by"}
        self.assertEqual(
            sorted(
                (
                    book_data.model_dump(exclude=exclude_book_data)
                    for book_data in response_body.book.book_data  # type: ignore
                ),
                key=lambda x: x["id"],
            ),  # type: ignore
            sorted(
                (
                    book_data.model_dump(exclude=exclude_book_data)
                    for book_data in updated_book.book_data  # type: ignore
                ),
                key=lambda x: x["id"],
            ),
        )

    def test_update_book_not_found(self):
        # Scenario: Attempt to update a book that doesn't exist

        # When a request is made to update the book
        update_body = self.book_dto_model_factory.build(
            isbn_code="978-0-987654-32-1",
            editor="Updated Editor",
            author_ids=[self.stored_new_author.id],
            category_ids=[self.stored_new_category.id],
        )

        response = self.client.put(
            "api/book",
            json=json.loads(update_body.model_dump_json()),
            params={"id": "11111111-1111-1111-1111-111111111111"},
        )

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json()["detail"], "Book not found")
