from tests.unit.book.producer.conftest import BookProducerConftest

from src.application.dto.producer import Message


class TestExternalBookUpsert(BookProducerConftest):

    def test_notify_external_book_upsert(self):
        # Arrange
        book = self.book_model_factory.build()

        # Act
        self.book_producer.notify_external_book_upsert(book=book)

        # Assert
        self.mock_producer.publish.assert_called_once_with(
            message=Message(
                queue_name="external.book.upsert",
                message=book.model_dump_json(),
            ),
        )
