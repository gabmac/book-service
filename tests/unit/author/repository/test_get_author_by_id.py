from tests.unit.author.repository.conftest import AuthorRepositoryConftest
from uuid6 import uuid7

from src.application.exceptions import NotFoundException


class TestGetAuthorById(AuthorRepositoryConftest):

    def test_get_existing_author(self):
        # Arrange - Create and save an author first
        author = self.author_model_factory.build()
        self.author_write_repository.upsert_author(author=author)

        # Act - Retrieve the author by ID
        result = self.author_read_repository.get_author_by_id(id=author.id)

        # Assert - Verify the author is returned correctly
        self.assertEqual(result, author)

    def test_get_non_existent_author(self):
        # Arrange - Generate a random UUID that doesn't exist
        non_existent_id = uuid7()

        # Act & Assert - Should raise NotFoundException
        with self.assertRaises(NotFoundException) as context:
            self.author_read_repository.get_author_by_id(id=non_existent_id)

            self.assertEqual(str(context.exception), "Author not found")
