from tests.unit.book.usecase.conftest import BookUseCaseConftest

from src.application.exceptions import OptimisticLockException
from src.application.usecase.book.upsert_book import UpsertBook


class TestUpsertBook(BookUseCaseConftest):

    def setUp(self):
        super().setUp()
        self.upsert_book = UpsertBook(
            book_write_repository=self.mock_book_write_repository,
            book_producer=self.mock_book_producer,
        )
        self.mock_book_write_repository.upsert_book.return_value = None
        self.mock_book_write_repository.upsert_book.side_effect = None
        self.mock_book_producer.notify_external_book_upsert.return_value = None
        self.mock_book_producer.notify_external_book_upsert.side_effect = None

    def tearDown(self) -> None:
        super().tearDown()
        self.mock_book_write_repository.upsert_book.reset_mock()
        self.mock_book_producer.notify_external_book_upsert.reset_mock()

    def test_execute_book_upsert(self):
        # Arrange
        book = self.book_model_factory.build()
        expected_book = self.book_model_factory.build(
            id=book.id,
            isbn_code=book.isbn_code,
            editor=book.editor,
            edition=book.edition,
            type=book.type,
            publish_date=book.publish_date,
            book_data=book.book_data,
            version=book.version,
            authors=book.authors,
            book_categories=book.book_categories,
            author_ids=book.author_ids,
            category_ids=book.category_ids,
            created_by=book.created_by,
            updated_by=book.updated_by,
            created_at=book.created_at,
            updated_at=book.updated_at,
        )

        # Mock repository responses
        self.mock_book_write_repository.upsert_book.return_value = expected_book

        # Act
        result = self.upsert_book.execute(book)

        # Assert
        self.mock_book_producer.notify_external_book_upsert.assert_called_once_with(
            book,
        )
        self.mock_book_write_repository.upsert_book.assert_called_once_with(book)
        self.assertEqual(result, expected_book)

    def test_execute_book_upsert_optimistic_lock_exception(self):
        # Arrange
        book = self.book_model_factory.build()
        self.mock_book_write_repository.upsert_book.side_effect = (
            OptimisticLockException
        )

        # Act
        result = self.upsert_book.execute(book)

        # Assert
        self.assertIsNone(result)
        self.mock_book_producer.notify_external_book_upsert.assert_called_once_with(
            book,
        )
        self.mock_book_write_repository.upsert_book.assert_called_once_with(book)
