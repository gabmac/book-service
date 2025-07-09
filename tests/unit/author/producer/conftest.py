from unittest.mock import Mock

from tests.conftest import BaseProducerConfTest
from tests.unit.author.conftest import BaseAuthorConfTest

from src.infrastructure.adapters.producer.author_producer import AuthorProducerAdapter


class AuthorProducerConftest(BaseAuthorConfTest, BaseProducerConfTest):
    def setUp(self):
        super().setUp()
        # Mock the Producer dependency
        self.mock_producer = Mock()
        self.author_producer = AuthorProducerAdapter(producer=self.mock_producer)
