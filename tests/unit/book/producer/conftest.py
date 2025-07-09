from tests.conftest import BaseProducerConfTest
from tests.unit.book.conftest import BaseBookConfTest

from src.infrastructure.adapters.producer.book_producer import BookProducerAdapter


class BookProducerConftest(BaseBookConfTest, BaseProducerConfTest):
    def setUp(self):
        super().setUp()
        # Mock the Producer dependency
        self.book_producer = BookProducerAdapter(
            producer=self.mock_producer,
        )
