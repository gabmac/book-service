from tests.unit.author.usecase.conftest import AuthorUseCaseConftest

from src.application.usecase.author.filter_author import FilterAuthor
from src.domain.entities.author import AuthorFilter


class TestFilterAuthor(AuthorUseCaseConftest):

    def setUp(self):
        super().setUp()
        self.filter_author = FilterAuthor(
            author_repository=self.mock_author_repository,
        )
        self.mock_author_repository.get_author_by_filter.return_value = None
        self.mock_author_repository.get_author_by_filter.side_effect = None

    def tearDown(self):
        super().tearDown()
        self.mock_author_repository.get_author_by_filter.reset_mock()

    def test_execute_with_filter(self):
        # Arrange
        author1 = self.author_model_factory.build(name="John Doe")
        author2 = self.author_model_factory.build(name="John Smith")
        authors = [author1, author2]

        filter_obj = AuthorFilter(name="John")

        # Mock repository response
        self.mock_author_repository.get_author_by_filter.return_value = authors

        # Act
        result = self.filter_author.execute(filter_obj)

        # Assert
        self.mock_author_repository.get_author_by_filter.assert_called_once_with(
            filter_obj,
        )
        self.assertEqual(result, authors)

    def test_execute_without_filter(self):
        # Arrange
        author1 = self.author_model_factory.build()
        author2 = self.author_model_factory.build()
        authors = [author1, author2]

        # Mock repository response
        self.mock_author_repository.get_author_by_filter.return_value = authors

        # Act
        result = self.filter_author.execute(None)

        # Assert
        self.mock_author_repository.get_author_by_filter.assert_called_once_with(None)
        self.assertEqual(result, authors)

    def test_execute_empty_result(self):
        # Arrange
        filter_obj = AuthorFilter(name="Non-existent Author")

        # Mock repository response - no authors found
        self.mock_author_repository.get_author_by_filter.return_value = []

        # Act
        result = self.filter_author.execute(filter_obj)

        # Assert - empty list
        self.mock_author_repository.get_author_by_filter.assert_called_once_with(
            filter_obj,
        )
        self.assertEqual(result, [])
