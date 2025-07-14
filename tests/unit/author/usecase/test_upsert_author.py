from tests.unit.author.usecase.conftest import AuthorUseCaseConftest

from src.application.exceptions import OptimisticLockException
from src.application.usecase.author.upsert_author import UpsertAuthor


class TestUpsertAuthor(AuthorUseCaseConftest):

    def setUp(self):
        super().setUp()
        self.upsert_author = UpsertAuthor(
            author_write_repository=self.mock_author_write_repository,
            author_producer=self.mock_author_producer,
        )
        self.mock_author_write_repository.upsert_author.return_value = None
        self.mock_author_write_repository.upsert_author.side_effect = None
        self.mock_author_producer.notify_external_author_upsert.return_value = None
        self.mock_author_producer.notify_external_author_upsert.side_effect = None

    def tearDown(self):
        super().tearDown()
        self.mock_author_write_repository.upsert_author.reset_mock()
        self.mock_author_producer.notify_external_author_upsert.reset_mock()

    def test_execute_author(self):
        # Arrange
        author = self.author_model_factory.build()

        # Mock repository response - author not found (new author)
        self.mock_author_write_repository.upsert_author.return_value = author

        # Act
        result = self.upsert_author.execute(author)

        # Assert
        self.mock_author_producer.notify_external_author_upsert.assert_called_once_with(
            author,
        )
        self.mock_author_write_repository.upsert_author.assert_called_once_with(author)
        self.assertEqual(result, author)

    def test_execute_author_with_optimistic_lock_exception(self):
        # Arrange
        author = self.author_model_factory.build()
        self.mock_author_write_repository.upsert_author.side_effect = (
            OptimisticLockException
        )
        # Act
        result = self.upsert_author.execute(author)
        # Assert
        self.mock_author_producer.notify_external_author_upsert.assert_called_once_with(
            author,
        )
        self.mock_author_write_repository.upsert_author.assert_called_once_with(author)
        self.assertIsNone(result)
