import json

from tests.integration.book_category.conftest import BookCategoryViewConfTest


class TestFilterBookCategory(BookCategoryViewConfTest):

    def setUp(self):
        super().setUp()
        book_category1 = self.book_category_model_factory.build(
            title="Science Fiction",
            description="Books about futuristic and scientific concepts",
            created_by="test_user",
            updated_by="test_user",
        )
        book_category2 = self.book_category_model_factory.build(
            title="Fantasy Literature",
            description="Books with magical and mythical elements",
            created_by="test_user",
            updated_by="test_user",
        )
        book_category3 = self.book_category_model_factory.build(
            title="Mystery Fiction",
            description="Books with suspenseful and investigative plots",
            created_by="test_user",
            updated_by="test_user",
        )

        # Store book categories in database
        self.stored_category1 = (
            self.book_category_write_repository.upsert_book_category(
                book_category1,
            )
        )
        self.stored_category2 = (
            self.book_category_write_repository.upsert_book_category(
                book_category2,
            )
        )
        self.stored_category3 = (
            self.book_category_write_repository.upsert_book_category(
                book_category3,
            )
        )

    def test_filter_book_category_with_filters(self):

        # Scenario: Filter book categories by title and description

        # Given book categories are stored in the database

        # When a request is made to filter book categories by title and description
        response = self.client.get(
            "api/book_category",
            params={
                "title": "Fiction",
                "description": "Books",
            },
        )

        # Then the response is a 200 status code
        self.assertEqual(response.status_code, 200)
        response_data = response.json()

        # And the response should list all book categories that match both filters
        expected_categories = [self.stored_category1, self.stored_category3]
        category_expected = [
            json.loads(expected_category.model_dump_json())
            for expected_category in expected_categories
        ]

        self.assertEqual(
            sorted(category_expected, key=lambda x: x["id"]),
            sorted(response_data, key=lambda x: x["id"]),
        )

    def test_filter_book_category_no_results(self):

        # Scenario: Filter book categories with no matches

        # Given book categories are stored in the database

        # When a request is made to filter book categories by non-existent criteria
        response = self.client.get(
            "api/book_category",
            params={
                "title": "NonExistent",
                "description": "NoMatch",
            },
        )

        # Then the response is a 200 status code
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertEqual(len(response_data), 0)

    def test_filter_book_category_no_filter(self):

        # Scenario: Get all book categories without filters

        # Given book categories are stored in the database

        # When a request is made without any filters
        response = self.client.get("api/book_category")

        # Then the response is a 200 status code
        self.assertEqual(response.status_code, 200)
        response_data = response.json()

        # And the response should list all book categories
        expected_categories = [
            self.stored_category1,
            self.stored_category2,
            self.stored_category3,
        ]
        category_expected = [
            json.loads(expected_category.model_dump_json())
            for expected_category in expected_categories
        ]

        self.assertEqual(
            sorted(category_expected, key=lambda x: x["id"]),
            sorted(response_data, key=lambda x: x["id"]),
        )
