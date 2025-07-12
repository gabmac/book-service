import json

from tests.integration.book.conftest import BookViewConfTest

from src.application.dto.book_dto import ProcessingBook


class TestCreateBook(BookViewConfTest):
    def setUp(self):
        super().setUp()
        # Common authors for tests
        self.author1 = self.author_model_factory.build(
            name="Author One",
            created_by="test_user",
            updated_by="test_user",
        )
        self.author2 = self.author_model_factory.build(
            name="Author Two",
            created_by="test_user",
            updated_by="test_user",
        )
        self.stored_author1 = self.author_write_repository.upsert_author(self.author1)
        self.stored_author2 = self.author_write_repository.upsert_author(self.author2)

        # Common book categories for tests
        self.category1 = self.book_category_model_factory.build(
            title="Fiction",
            description="Fiction books",
            created_by="test_user",
            updated_by="test_user",
        )
        self.category2 = self.book_category_model_factory.build(
            title="Science",
            description="Science books",
            created_by="test_user",
            updated_by="test_user",
        )
        self.stored_category1 = (
            self.book_category_write_repository.upsert_book_category(
                self.category1,
            )
        )
        self.stored_category2 = (
            self.book_category_write_repository.upsert_book_category(
                self.category2,
            )
        )

    def test_create_book_success(self):
        # Scenario: Successfully create a book

        # When a request is made to create a book with valid authors and categories
        body = self.book_dto_model_factory.build(
            author_ids=[self.stored_author1.id, self.stored_author2.id],
            category_ids=[self.stored_category1.id, self.stored_category2.id],
        )
        response = self.client.post("api/book", json=json.loads(body.model_dump_json()))

        # Then the response is a 202 status code (task is processing)
        self.assertEqual(response.status_code, 202)
        response_body = ProcessingBook.model_validate_json(json.dumps(response.json()))
        self.assertEqual(response_body.message, "Task is processing")

        # And the message is consumed from the queue
        self.consumer.consume("book.upsert")

        # And the book is created in the database
        # (simulate the consumer processing, then check the book exists)
        created_book = self.book_read_repository.get_book_by_id(response_body.book.id)

        exclude_book = {
            "book_data",
            "category_ids",
            "author_ids",
            "created_at",
            "updated_at",
        }
        # Assert

        self.assertEqual(
            json.loads(response_body.book.model_dump_json(exclude=exclude_book)),
            json.loads(created_book.model_dump_json(exclude=exclude_book)),
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
                    for book_data in created_book.book_data  # type: ignore
                ),
                key=lambda x: x["id"],
            ),
        )

    def test_create_book_authors_not_found(self):
        # Scenario: Attempt to create a book with non-existent authors

        # And author IDs that do not exist
        non_existent_author_id1 = "11111111-1111-1111-1111-111111111111"
        non_existent_author_id2 = "22222222-2222-2222-2222-222222222222"

        # When a request is made to create a book with non-existent authors
        body = self.book_dto_model_factory.build(
            author_ids=[non_existent_author_id1, non_existent_author_id2],
            category_ids=[self.stored_category1.id, self.stored_category2.id],
        )
        response = self.client.post("api/book", json=json.loads(body.model_dump_json()))

        # Then the response is a 404 status code
        self.assertEqual(response.status_code, 404)
        response_data = response.json()
        self.assertEqual(response_data["detail"], "Some authors not found")

    def test_create_book_categories_not_found(self):
        # Scenario: Attempt to create a book with non-existent book categories

        # And book category IDs that do not exist
        non_existent_category_id1 = "33333333-3333-3333-3333-333333333333"
        non_existent_category_id2 = "44444444-4444-4444-4444-444444444444"

        # When a request is made to create a book with non-existent categories
        body = self.book_dto_model_factory.build(
            author_ids=[self.stored_author1.id, self.stored_author2.id],
            category_ids=[non_existent_category_id1, non_existent_category_id2],
        )
        response = self.client.post("api/book", json=json.loads(body.model_dump_json()))

        # Then the response is a 404 status code
        self.assertEqual(response.status_code, 404)
        response_data = response.json()
        self.assertEqual(response_data["detail"], "Some book categories not found")
