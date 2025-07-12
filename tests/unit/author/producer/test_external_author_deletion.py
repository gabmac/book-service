import json

from tests.unit.author.producer.conftest import AuthorProducerConftest
from uuid6 import uuid7

from src.application.dto.producer import Message


class TestExternalAuthorDeletion(AuthorProducerConftest):

    def test_notify_external_author_deletion(self):
        # Arrange
        author_id = uuid7()

        # Act
        self.author_producer.notify_external_author_deletion(id=author_id)

        # Assert
        self.mock_producer.publish.assert_called_once_with(
            message=Message(
                queue_name="external.author.deletion",
                message=json.dumps({"id": str(author_id)}),
            ),
        )
