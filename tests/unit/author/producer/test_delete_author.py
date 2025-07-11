import json

from tests.unit.author.producer.conftest import AuthorProducerConftest
from uuid6 import uuid7

from src.application.dto.producer import Message


class TestDeleteAuthor(AuthorProducerConftest):

    def test_delete_author_publishes_correct_message(self):
        # Arrange
        author_id = uuid7()
        expected_message = Message(
            queue_name="author.deletion",
            message=json.dumps({"id": str(author_id)}),
        )

        # Act
        self.author_producer.delete_author(id=author_id)

        # Assert
        self.mock_producer.publish.assert_called_once_with(message=expected_message)
