import json

from tests.integration.book_category.conftest import BookCategoryViewConfTest

from src.application.dto.book_category import ProcessingBookCategory
from src.domain.entities.book_category import BookCategory, BookCategoryFilter


class TestCreateBookCategory(BookCategoryViewConfTest):
    def test_create_book_category(self):

        # Scenario: Create a book category

        # When a request is made to create a book category
        body = self.book_category_upsert_model_factory.build()
        response = self.client.put("api/book_category", json=body.model_dump())

        # Then the response is a 202 status code
        self.assertEqual(response.status_code, 202)
        response_body = ProcessingBookCategory.model_validate_json(
            json.dumps(response.json()),
        )

        # And the message is consumed from the queue
        self.consumer.consume("book_category.upsert")
        stored_book_categories = (
            self.book_category_repository.get_book_category_by_filter(
                BookCategoryFilter(),
            )
        )

        # And the book category is stored in the database
        exclude_fields = {"created_at", "updated_at"}
        self.assertEqual(
            stored_book_categories[0].model_dump(exclude=exclude_fields),
            BookCategory.model_validate(response_body.book_category).model_dump(
                exclude=exclude_fields,
            ),
        )

        self.assertEqual(response_body.message, "Task is processing")
