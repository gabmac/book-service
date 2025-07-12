import json

from tests.integration.author.conftest import AuthorViewConfTest


class TestFilterAuthor(AuthorViewConfTest):

    def setUp(self):
        super().setUp()
        author1 = self.author_model_factory.build(
            name="John Doe",
            created_by="test_user",
            updated_by="test_user",
        )
        author2 = self.author_model_factory.build(
            name="Jane Smith",
            created_by="test_user",
            updated_by="test_user",
        )
        author3 = self.author_model_factory.build(
            name="Bob Johnson",
            created_by="test_user",
            updated_by="test_user",
        )

        # Store authors in database
        self.stored_author1 = self.author_write_repository.upsert_author(author1)
        self.stored_author2 = self.author_write_repository.upsert_author(author2)
        self.stored_author3 = self.author_write_repository.upsert_author(author3)

    def test_filter_author_with_filter(self):

        # Scenario: Filter authors by name

        # Given authors are stored in the database

        # When a request is made to filter authors by name
        response = self.client.get("api/author", params={"name": "John"})

        # Then the response is a 200 status code
        self.assertEqual(response.status_code, 200)
        response_data = response.json()

        # And the response should list authors that match the filter
        expected_authors = [
            self.stored_author1,
            self.stored_author3,
        ]  # John Doe, Bob Johnson (contains "John")
        author_expected = [
            json.loads(expected_author.model_dump_json())
            for expected_author in expected_authors
        ]

        self.assertEqual(
            sorted(author_expected, key=lambda x: x["id"]),
            sorted(response_data, key=lambda x: x["id"]),
        )

    def test_filter_author_no_results(self):

        # Scenario: Filter authors with no matches

        # Given authors are stored in the database

        # When a request is made to filter authors by non-existent name
        response = self.client.get("api/author", params={"name": "NonExistent"})

        # Then the response is a 200 status code
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertEqual(len(response_data), 0)

    def test_filter_author_no_filter(self):

        # Scenario: Get all authors without filters

        # Given authors are stored in the database

        # When a request is made without any filters
        response = self.client.get("api/author")

        # Then the response is a 200 status code
        self.assertEqual(response.status_code, 200)
        response_data = response.json()

        # And the response should list all authors
        expected_authors = [
            self.stored_author1,
            self.stored_author2,
            self.stored_author3,
        ]
        author_expected = [
            json.loads(expected_author.model_dump_json())
            for expected_author in expected_authors
        ]

        self.assertEqual(
            sorted(author_expected, key=lambda x: x["id"]),
            sorted(response_data, key=lambda x: x["id"]),
        )
