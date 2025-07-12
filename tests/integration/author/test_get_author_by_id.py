import json

from tests.integration.author.conftest import AuthorViewConfTest

from src.application.dto.author import AuthorResponse


class TestGetAuthorById(AuthorViewConfTest):
    def test_get_author_by_id_success(self):

        # Scenario: Get an author by ID

        # Given an author is stored in the database
        author = self.author_model_factory.build(
            name="Test Author",
            created_by="test_user",
            updated_by="test_user",
        )
        stored_author = self.author_write_repository.upsert_author(author)

        # When a request is made to get the author by ID
        response = self.client.get(f"api/author/{stored_author.id}")

        # Then the response is a 200 status code
        self.assertEqual(response.status_code, 200)
        response_body = AuthorResponse.model_validate_json(
            json.dumps(response.json()),
        )

        # And the response contains the correct author data
        exclude_fields = {"created_at", "updated_at"}
        self.assertEqual(
            stored_author.model_dump(exclude=exclude_fields),
            response_body.model_dump(exclude=exclude_fields),
        )

    def test_get_author_by_id_not_found(self):

        # Scenario: Get a non-existent author by ID

        # Given no author with a specific ID exists
        non_existent_id = "550e8400-e29b-41d4-a716-446655440000"

        # When a request is made to get the author by non-existent ID
        response = self.client.get(f"api/author/{non_existent_id}")

        # Then the response is a 404 status code
        self.assertEqual(response.status_code, 404)
        response_data = response.json()
        self.assertIn("detail", response_data)
