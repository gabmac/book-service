from tests.unit.author.usecase.conftest import AuthorUseCaseConftest

from src.application.usecase.author.get_by_id import GetAuthorById


class TestGetAuthorById(AuthorUseCaseConftest):

    def setUp(self):
        super().setUp()
        self.get_author_by_id = GetAuthorById(
            author_repository=self.mock_author_repository,
        )
        self.mock_author_repository.get_author_by_id.return_value = None
        self.mock_author_repository.get_author_by_id.side_effect = None

    def tearDown(self):
        super().tearDown()
        self.mock_author_repository.get_author_by_id.reset_mock()

    def test_execute_existing_author(self):
        # Arrange
        author = self.author_model_factory.build()

        # Mock repository response
        self.mock_author_repository.get_author_by_id.return_value = author

        # Act
        result = self.get_author_by_id.execute(author.id)

        # Assert
        self.mock_author_repository.get_author_by_id.assert_called_once_with(author.id)
        # The result should be a validated Author entity
        self.assertEqual(result, author)
