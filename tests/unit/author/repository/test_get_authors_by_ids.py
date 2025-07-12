from typing import List

from tests.unit.author.repository.conftest import AuthorRepositoryConftest
from uuid6 import uuid7


class TestGetAuthorsByIds(AuthorRepositoryConftest):

    def test_get_multiple_existing_authors(self):
        # Arrange - Create and save multiple authors
        author1 = self.author_model_factory.build()
        author2 = self.author_model_factory.build()
        author3 = self.author_model_factory.build()

        self.author_write_repository.upsert_author(author=author1)
        self.author_write_repository.upsert_author(author=author2)
        self.author_write_repository.upsert_author(author=author3)

        # Act - Retrieve authors by their IDs
        ids = [author1.id, author2.id, author3.id]
        results = self.author_read_repository.get_authors_by_ids(ids=ids)

        # Assert - Should return all three authors
        self.assertEqual(
            results.sort(key=lambda x: x.id),
            [author1, author2, author3].sort(key=lambda x: x.id),
        )

    def test_get_partial_existing_authors(self):
        # Arrange - Create and save some authors
        author1 = self.author_model_factory.build()
        author2 = self.author_model_factory.build()
        author3 = self.author_model_factory.build()

        self.author_write_repository.upsert_author(author=author1)
        self.author_write_repository.upsert_author(author=author2)
        self.author_write_repository.upsert_author(author=author3)

        # Act - Request with mix of existing and non-existing IDs
        ids = [author1.id, author2.id]
        results = self.author_read_repository.get_authors_by_ids(ids=ids)

        # Assert - Should return only the existing authors
        self.assertEqual(
            results.sort(key=lambda x: x.id),
            [author1, author2].sort(key=lambda x: x.id),
        )

    def test_get_no_existing_authors(self):
        # Arrange - Generate non-existent IDs
        non_existent_ids = [uuid7()]

        # Act - Request with non-existing IDs
        results = self.author_read_repository.get_authors_by_ids(ids=non_existent_ids)  # type: ignore

        # Assert - Should return empty list
        self.assertEqual(results, [])

    def test_get_empty_ids_list(self):
        # Arrange - Empty list of IDs
        empty_ids: List = []

        # Act - Request with empty IDs list
        results = self.author_read_repository.get_authors_by_ids(ids=empty_ids)

        # Assert - Should return empty list
        self.assertEqual(results, [])
