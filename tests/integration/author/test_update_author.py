import json

from tests.integration.author.conftest import AuthorViewConfTest

from src.application.dto.author import ProcessingAuthor
from src.domain.entities.author import Author


class TestUpdateAuthor(AuthorViewConfTest):
    def test_update_author(self):

        # Scenario: Update an existing author

        # Given an author is already stored in the database
        existing_author = self.author_model_factory.build(
            name="Original Author",
            created_by="test_user",
            updated_by="test_user",
        )
        stored_author = self.author_repository.upsert_author(existing_author)

        # When a request is made to update the author
        update_body = self.author_upsert_model_factory.build(
            name="Updated Author Name",
        )
        response = self.client.put(
            f"api/author/{stored_author.id}",
            json=update_body.model_dump(),
        )

        # Then the response is a 202 status code
        self.assertEqual(response.status_code, 202)
        response_body = ProcessingAuthor.model_validate_json(
            json.dumps(response.json()),
        )

        # And the message is consumed from the queue
        self.consumer.consume("author.upsert")
        updated_authors = self.author_repository.get_author_by_id(stored_author.id)

        # And the author is updated in the database
        exclude_fields = {"created_at", "updated_at"}
        self.assertEqual(
            updated_authors.model_dump(exclude=exclude_fields),
            Author.model_validate(response_body.author).model_dump(
                exclude=exclude_fields,
            ),
        )

        self.assertEqual(response_body.message, "Task is processing")

    def test_update_author_not_found(self):
        # Scenario: Update a non-existent author

        # Given a non-existent author
        non_existent_id = "550e8400-e29b-41d4-a716-446655440000"

        # When a request is made to update the non-existent author
        update_body = self.author_upsert_model_factory.build(
            name="Updated Author Name",
        )
        response = self.client.put(
            f"api/author/{non_existent_id}",
            json=update_body.model_dump(),
        )

        # Then the response is a 404 status code
        self.assertEqual(response.status_code, 404)
        response_data = response.json()
        self.assertIn("detail", response_data)
