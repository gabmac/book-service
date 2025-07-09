from tests.unit.author.producer.conftest import AuthorProducerConftest

from src.application.dto.producer import Message


class TestUpsertAuthor(AuthorProducerConftest):

    def test_upsert_author_publishes_correct_message(self):
        # Arrange
        author = self.author_model_factory.build()
        expected_message = Message(
            queue_name="author.upsert",
            message=author.model_dump_json(),
        )

        # Act
        self.author_producer.upsert_author(author=author)

        # Assert
        self.mock_producer.publish.assert_called_once_with(message=expected_message)
