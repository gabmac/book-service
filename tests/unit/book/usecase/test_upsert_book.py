from tests.unit.book.usecase.conftest import BookUseCaseConftest

from src.application.exceptions import NotFoundException
from src.application.usecase.book.upsert_book import UpsertBook
from src.domain.entities.book import Book


class TestUpsertBook(BookUseCaseConftest):

    def setUp(self):
        super().setUp()
        self.upsert_book = UpsertBook(
            book_repository=self.mock_book_repository,
            book_producer=self.mock_book_producer,
        )
        self.mock_book_repository.get_book_by_id.return_value = None
        self.mock_book_repository.get_book_by_id.side_effect = None
        self.mock_book_repository.upsert_book.return_value = None
        self.mock_book_repository.upsert_book.side_effect = None

    def tearDown(self) -> None:
        super().tearDown()
        self.mock_book_repository.upsert_book.reset_mock()
        self.mock_book_repository.get_book_by_id.reset_mock()

    def test_execute_new_book(self):
        # Arrange
        book = self.book_model_factory.build(
            author_ids=None,
            categories_id=None,
        )

        # Mock repository responses - book doesn't exist
        self.mock_book_repository.get_book_by_id.side_effect = NotFoundException(
            "Book not found",
        )
        self.mock_book_repository.upsert_book.return_value = book

        # Act
        result = self.upsert_book.execute(book)

        # Assert
        self.mock_book_repository.get_book_by_id.assert_called_once_with(book.id)
        self.mock_book_repository.upsert_book.assert_called_once_with(book)
        self.assertEqual(result, book)

    def test_execute_existing_book_update(self):
        # Arrange

        existing_book = self.book_model_factory.build(
            author_ids=None,
            categories_id=None,
        )

        updated_book = self.book_model_factory.build(
            id=existing_book.id,
            author_ids=None,
            categories_id=None,
        )

        expected_book = Book.model_validate(updated_book)
        expected_book.created_at = existing_book.created_at
        expected_book.created_by = existing_book.created_by

        # Mock repository responses - book exists
        self.mock_book_repository.get_book_by_id.return_value = existing_book
        self.mock_book_repository.upsert_book.return_value = expected_book

        # Act
        result = self.upsert_book.execute(updated_book)

        # Assert
        self.mock_book_repository.get_book_by_id.assert_called_once_with(
            updated_book.id,
        )
        self.mock_book_repository.upsert_book.assert_called_once()

        # Verify that created_at and created_by were preserved
        self.assertEqual(
            expected_book,
            result,
        )
