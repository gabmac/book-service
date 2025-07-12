import json

from tests.integration.author.conftest import AuthorViewConfTest

from src.application.dto.author import ProcessingAuthor
from src.domain.entities.author import Author


class TestCreateAuthor(AuthorViewConfTest):
    def test_create_author(self):

        # Scenario: Create an author

        # When a request is made to create an author
        body = self.author_upsert_model_factory.build()
        response = self.client.post("api/author", json=body.model_dump())

        # Then the response is a 202 status code
        self.assertEqual(response.status_code, 202)
        response_body = ProcessingAuthor.model_validate_json(
            json.dumps(response.json()),
        )

        # And the message is consumed from the queue
        self.consumer.consume("author.upsert")
        stored_authors = self.author_read_repository.get_author_by_id(
            response_body.author.id,
        )

        # And the author is stored in the database
        exclude_fields = {"created_at", "updated_at"}
        self.assertEqual(
            stored_authors.model_dump(exclude=exclude_fields),
            Author.model_validate(response_body.author).model_dump(
                exclude=exclude_fields,
            ),
        )

        self.assertEqual(response_body.message, "Task is processing")
