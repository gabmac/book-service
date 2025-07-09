from uuid import uuid4

from tests.unit.book.usecase.conftest import BookUseCaseConftest

from src.application.exceptions import NotFoundException
from src.application.usecase.book.get_book_by_id import GetBookById


class TestGetBookById(BookUseCaseConftest):

    def setUp(self):
        super().setUp()
        self.get_book_by_id = GetBookById(
            book_repository=self.mock_book_repository,
        )
        self.mock_book_repository.get_book_by_id.return_value = None
        self.mock_book_repository.get_book_by_id.side_effect = None

    def tearDown(self) -> None:
        super().tearDown()
        self.mock_book_repository.get_book_by_id.reset_mock()

    def test_execute_existing_book(self):
        # Arrange
        book = self.book_model_factory.build()

        # Mock repository response
        self.mock_book_repository.get_book_by_id.return_value = book

        # Act
        result = self.get_book_by_id.execute(book.id)

        # Assert
        self.mock_book_repository.get_book_by_id.assert_called_once_with(book.id)
        self.assertEqual(result, book)

    def test_execute_non_existent_book(self):
        # Arrange
        non_existent_id = uuid4()

        # Mock repository response - book not found
        self.mock_book_repository.get_book_by_id.side_effect = NotFoundException(
            "Book not found",
        )

        # Act & Assert
        with self.assertRaises(NotFoundException):
            self.get_book_by_id.execute(non_existent_id)

        self.mock_book_repository.get_book_by_id.assert_called_once_with(
            non_existent_id,
        )
