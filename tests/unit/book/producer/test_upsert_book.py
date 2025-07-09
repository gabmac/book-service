from tests.unit.book.producer.conftest import BookProducerConftest

from src.application.dto.producer import Message


class TestUpsertBook(BookProducerConftest):

    def test_upsert_book(self):
        # Arrange
        book = self.book_model_factory.build()

        # Act
        self.book_producer.upsert_book(book=book)

        # Assert
        self.mock_producer.publish.assert_called_once_with(
            message=Message(
                queue_name="book.upsert",
                message=book.model_dump_json(),
            ),
        )
