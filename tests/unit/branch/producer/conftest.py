from tests.conftest import BaseProducerConfTest
from tests.unit.branch.conftest import BaseBranchConfTest

from src.infrastructure.adapters.producer.branch_producer import BranchProducerAdapter


class BranchProducerConftest(BaseBranchConfTest, BaseProducerConfTest):
    def setUp(self):
        super().setUp()
        # Mock the Producer dependency
        self.branch_producer = BranchProducerAdapter(
            producer=self.mock_producer,
        )
