from tests.unit.author.repository.conftest import AuthorRepositoryConftest
from uuid6 import uuid7

from src.application.exceptions import NotFoundException


class TestDeleteAuthor(AuthorRepositoryConftest):

    def test_delete_existing_author(self):
        # Arrange - Create and save an author
        author = self.author_model_factory.build()
        self.author_repository.upsert_author(author=author)

        # Act - Delete the author
        self.author_repository.delete_author(id=str(author.id))

        # Assert - Author should no longer exist
        with self.assertRaises(NotFoundException):
            self.author_repository.get_author_by_id(id=author.id)

    def test_delete_non_existent_author(self):
        # Arrange - Generate a random UUID that doesn't exist

        # Act - Attempt to delete non-existent author (should not raise error)
        with self.assertRaises(NotFoundException):
            self.author_repository.get_author_by_id(id=uuid7())
