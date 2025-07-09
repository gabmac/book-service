from tests.unit.book_category.producer.conftest import BookCategoryProducerConftest

from src.application.dto.producer import Message


class TestUpsertBookCategory(BookCategoryProducerConftest):

    def test_upsert_book_category_publishes_correct_message(self):
        # Arrange
        book_category = self.book_category_model_factory.build()
        expected_message = Message(
            queue_name="book_category.upsert",
            message=book_category.model_dump_json(),
        )

        # Act
        self.book_category_producer.upsert_book_category(book_category=book_category)

        # Assert
        self.mock_producer.publish.assert_called_once_with(message=expected_message)
