from tests.conftest import BaseProducerConfTest
from tests.unit.physical_exemplar.conftest import BasePhysicalExemplarConfTest

from src.infrastructure.adapters.producer.physical_exemplar_producer import (
    PhysicalExemplarProducerAdapter,
)


class PhysicalExemplarProducerConftest(
    BasePhysicalExemplarConfTest,
    BaseProducerConfTest,
):
    def setUp(self):
        super().setUp()
        # Mock the Producer dependency
        self.physical_exemplar_producer = PhysicalExemplarProducerAdapter(
            producer=self.mock_producer,
        )
