from tests.unit.book.usecase.conftest import BookUseCaseConftest

from src.application.usecase.book.filter_book import FilterBook
from src.domain.entities.book import BookSearchFilter


class TestFilterBook(BookUseCaseConftest):

    def setUp(self):
        super().setUp()
        self.filter_book = FilterBook(
            book_repository=self.mock_book_repository,
        )
        self.mock_book_repository.get_book_by_filter.return_value = None
        self.mock_book_repository.get_book_by_filter.side_effect = None

    def tearDown(self):
        super().tearDown()
        self.mock_book_repository.get_book_by_filter.reset_mock()

    def test_execute_with_filter(self):
        # Arrange
        book1 = self.book_model_factory.build(isbn_code="123456789")
        book2 = self.book_model_factory.build(isbn_code="987654321")
        expected_books = [book1, book2]

        filter_criteria = self.book_filter_model_factory.build()

        # Mock repository response
        self.mock_book_repository.get_book_by_filter.return_value = expected_books

        # Act
        result = self.filter_book.execute(filter_criteria)

        # Assert
        self.mock_book_repository.get_book_by_filter.assert_called_once_with(
            filter_criteria,
        )
        self.assertEqual(result, expected_books)

    def test_execute_with_empty_filter(self):
        # Arrange
        book1 = self.book_model_factory.build()
        book2 = self.book_model_factory.build()
        book3 = self.book_model_factory.build()
        all_books = [book1, book2, book3]

        empty_filter = BookSearchFilter()

        # Mock repository response
        self.mock_book_repository.get_book_by_filter.return_value = all_books

        # Act
        result = self.filter_book.execute(empty_filter)

        # Assert
        self.mock_book_repository.get_book_by_filter.assert_called_once_with(
            empty_filter,
        )
        self.assertEqual(result, all_books)

    def test_execute_with_none_filter(self):
        # Arrange
        book1 = self.book_model_factory.build()
        all_books = [book1]

        # Mock repository response
        self.mock_book_repository.get_book_by_filter.return_value = all_books

        # Act
        result = self.filter_book.execute(None)

        # Assert
        self.mock_book_repository.get_book_by_filter.assert_called_once_with(None)
        self.assertEqual(result, all_books)

    def test_execute_no_results(self):
        # Arrange
        filter_criteria = BookSearchFilter(isbn_code="nonexistent")

        # Mock repository response - no books found
        self.mock_book_repository.get_book_by_filter.return_value = []

        # Act
        result = self.filter_book.execute(filter_criteria)

        # Assert
        self.mock_book_repository.get_book_by_filter.assert_called_once_with(
            filter_criteria,
        )
        self.assertEqual(result, [])
