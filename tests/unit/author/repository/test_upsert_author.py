from tests.unit.author.repository.conftest import AuthorRepositoryConftest

from src.application.exceptions import OptimisticLockException


class TestUpsertAuthor(AuthorRepositoryConftest):

    def test_new_author(self):
        author = self.author_model_factory.build()
        self.assertEqual(
            self.author_write_repository.upsert_author(author=author),
            author,
        )

    def test_update_author(self):
        author = self.author_model_factory.build(version=2)
        self.author_write_repository.upsert_author(author=author)
        author.name = "Updated Author"
        author.version = 3
        self.assertEqual(
            self.author_write_repository.upsert_author(author=author),
            author,
        )

    def test_update_author_with_wrong_version(self):
        author = self.author_model_factory.build(version=3)
        self.author_write_repository.upsert_author(author=author)
        author.name = "Updated Author"
        author.version = author.version - 1
        with self.assertRaises(OptimisticLockException):
            self.author_write_repository.upsert_author(author=author)
