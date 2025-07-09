from tests.unit.author.repository.conftest import AuthorRepositoryConftest


class TestUpsertAuthor(AuthorRepositoryConftest):

    def test_new_author(self):
        author = self.author_model_factory.build()
        self.assertEqual(
            self.author_repository.upsert_author(author=author),
            author,
        )

    def test_update_author(self):
        author = self.author_model_factory.build()
        self.author_repository.upsert_author(author=author)
        author.name = "Updated Author"
        self.assertEqual(
            self.author_repository.upsert_author(author=author),
            author,
        )
