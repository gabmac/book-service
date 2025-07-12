from tests.unit.author.producer.conftest import AuthorProducerConftest

from src.application.dto.producer import Message


class TestExternalAuthorUpsert(AuthorProducerConftest):

    def test_notify_external_author_upsert(self):
        # Arrange
        author = self.author_model_factory.build()

        # Act
        self.author_producer.notify_external_author_upsert(author=author)

        # Assert
        self.mock_producer.publish.assert_called_once_with(
            message=Message(
                queue_name="external.author.upsert",
                message=author.model_dump_json(),
            ),
        )
