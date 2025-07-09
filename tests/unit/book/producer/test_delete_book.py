import json
from uuid import uuid4

from tests.unit.book.producer.conftest import BookProducerConftest

from src.application.dto.producer import Message


class TestDeleteBook(BookProducerConftest):

    def test_delete_book(self):
        # Arrange
        book_id = uuid4()

        # Act
        self.book_producer.delete_book(id=book_id)

        # Assert
        self.mock_producer.publish.assert_called_once_with(
            message=Message(
                queue_name="book.deletion",
                message=json.dumps({"id": str(book_id)}),
            ),
        )
