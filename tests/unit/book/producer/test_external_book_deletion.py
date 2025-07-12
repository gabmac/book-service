import json

from tests.unit.book.producer.conftest import BookProducerConftest
from uuid6 import uuid7

from src.application.dto.producer import Message


class TestExternalBookDeletion(BookProducerConftest):

    def test_notify_external_book_deletion(self):
        # Arrange
        book_id = uuid7()

        # Act
        self.book_producer.notify_external_book_deletion(id=book_id)

        # Assert
        self.mock_producer.publish.assert_called_once_with(
            message=Message(
                queue_name="external.book.deletion",
                message=json.dumps({"id": str(book_id)}),
            ),
        )
