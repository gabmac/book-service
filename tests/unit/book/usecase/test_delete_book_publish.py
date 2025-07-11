from tests.unit.book.usecase.conftest import BookUseCaseConftest
from uuid6 import uuid7

from src.application.usecase.book.delete_book_publish import DeleteBookPublish


class TestDeleteBookPublish(BookUseCaseConftest):

    def setUp(self):
        super().setUp()
        self.delete_book_publish = DeleteBookPublish(
            book_producer=self.mock_book_producer,
        )

    def test_execute_successful_publish(self):
        # Arrange
        book_id = uuid7()

        # Mock producer response
        self.mock_book_producer.delete_book.return_value = None

        # Act
        result = self.delete_book_publish.execute(book_id)

        # Assert
        self.mock_book_producer.delete_book.assert_called_once_with(book_id)
        self.assertIsNone(result)
