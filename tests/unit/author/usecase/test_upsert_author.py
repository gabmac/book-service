from tests.unit.author.usecase.conftest import AuthorUseCaseConftest

from src.application.exceptions import NotFoundException
from src.application.usecase.author.upsert_author import UpsertAuthor


class TestUpsertAuthor(AuthorUseCaseConftest):

    def setUp(self):
        super().setUp()
        self.upsert_author = UpsertAuthor(
            author_repository=self.mock_author_repository,
            author_producer=self.mock_author_producer,
        )
        self.mock_author_repository.get_author_by_id.return_value = None
        self.mock_author_repository.get_author_by_id.side_effect = None
        self.mock_author_repository.upsert_author.return_value = None
        self.mock_author_repository.upsert_author.side_effect = None

    def tearDown(self):
        super().tearDown()
        self.mock_author_repository.get_author_by_id.reset_mock()
        self.mock_author_repository.upsert_author.reset_mock()

    def test_execute_new_author(self):
        # Arrange
        author = self.author_model_factory.build()

        # Mock repository response - author not found (new author)
        self.mock_author_repository.get_author_by_id.side_effect = NotFoundException(
            "Author not found",
        )
        self.mock_author_repository.upsert_author.return_value = author

        # Act
        result = self.upsert_author.execute(author)

        # Assert
        self.mock_author_repository.get_author_by_id.assert_called_once_with(author.id)
        self.mock_author_repository.upsert_author.assert_called_once_with(author)
        self.assertEqual(result, author)

    def test_execute_existing_author(self):
        # Arrange
        existing_author = self.author_model_factory.build()
        updated_author = self.author_model_factory.build(
            id=existing_author.id,
            name="Updated Name",
        )

        # Mock repository response - author found (update)
        self.mock_author_repository.get_author_by_id.return_value = existing_author
        self.mock_author_repository.upsert_author.return_value = updated_author

        # Act
        result = self.upsert_author.execute(updated_author)

        # Assert
        self.mock_author_repository.get_author_by_id.assert_called_once_with(
            updated_author.id,
        )
        self.mock_author_repository.upsert_author.assert_called_once()

        # Verify that created_at and created_by are preserved from existing author
        called_author = self.mock_author_repository.upsert_author.call_args[0][0]
        self.assertEqual(called_author.created_at, existing_author.created_at)
        self.assertEqual(called_author.created_by, existing_author.created_by)
        self.assertEqual(called_author.name, updated_author.name)

        self.assertEqual(result, updated_author)
