from tests.conftest import BaseProducerConfTest
from tests.unit.book_category.conftest import BaseBookCategoryConfTest

from src.infrastructure.adapters.producer.book_category_producer import (
    BookCategoryProducerAdapter,
)


class BookCategoryProducerConftest(BaseBookCategoryConfTest, BaseProducerConfTest):
    def setUp(self):
        super().setUp()
        # Mock the Producer dependency
        self.book_category_producer = BookCategoryProducerAdapter(
            producer=self.mock_producer,
        )
