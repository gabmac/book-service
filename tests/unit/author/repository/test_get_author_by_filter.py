from tests.unit.author.repository.conftest import AuthorRepositoryConftest

from src.domain.entities.author import AuthorFilter


class TestGetAuthorByFilter(AuthorRepositoryConftest):

    async def test_filter_by_name_found(self):
        # Arrange - Create and save authors with different names
        author1 = self.author_model_factory.build(name="John Doe")
        author2 = self.author_model_factory.build(name="Jane Smith")
        author3 = self.author_model_factory.build(name="John Smith")

        self.author_repository.upsert_author(author=author1)
        self.author_repository.upsert_author(author=author2)
        self.author_repository.upsert_author(author=author3)

        # Act - Filter by name similar to "John"
        filter_criteria = AuthorFilter(name="John")
        results = self.author_repository.get_author_by_filter(filter=filter_criteria)

        self.assertEqual(
            results.sort(key=lambda x: x.name),
            [author1, author3].sort(key=lambda x: x.name),
        )

    async def test_filter_by_name_not_found(self):
        # Arrange - Create and save authors with different names
        author1 = self.author_model_factory.build(name="John Doe")
        author2 = self.author_model_factory.build(name="Jane Smith")

        self.author_repository.upsert_author(author=author1)
        self.author_repository.upsert_author(author=author2)

        # Act - Filter by name that doesn't exist
        filter_criteria = AuthorFilter(name="NonExistentAuthor")
        results = self.author_repository.get_author_by_filter(filter=filter_criteria)

        # Assert - Should return empty list
        self.assertEqual(results, [])

    async def test_no_filter_returns_all(self):
        # Arrange - Create and save multiple authors
        author1 = self.author_model_factory.build()
        author2 = self.author_model_factory.build()
        author3 = self.author_model_factory.build()

        self.author_repository.upsert_author(author=author1)
        self.author_repository.upsert_author(author=author2)
        self.author_repository.upsert_author(author=author3)

        # Act - Call with no filter
        results = self.author_repository.get_author_by_filter(filter=None)

        # Assert - Should return all authors
        self.assertGreaterEqual(len(results), 3)

    async def test_empty_filter_returns_all(self):
        # Arrange - Create and save multiple authors
        author1 = self.author_model_factory.build()
        author2 = self.author_model_factory.build()

        self.author_repository.upsert_author(author=author1)
        self.author_repository.upsert_author(author=author2)

        # Act - Call with empty filter
        empty_filter = AuthorFilter(name=None)
        results = self.author_repository.get_author_by_filter(filter=empty_filter)

        # Assert - Should return all authors
        self.assertEqual(
            results.sort(key=lambda x: x.name),
            [author1, author2].sort(key=lambda x: x.name),
        )
