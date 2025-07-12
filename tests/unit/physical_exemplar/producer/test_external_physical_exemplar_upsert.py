from tests.unit.physical_exemplar.producer.conftest import (
    PhysicalExemplarProducerConftest,
)

from src.application.dto.producer import Message


class TestExternalPhysicalExemplarUpsert(PhysicalExemplarProducerConftest):

    def test_notify_external_physical_exemplar_upsert(self):
        # Arrange
        physical_exemplar = self.physical_exemplar_model_factory.build()

        # Act
        self.physical_exemplar_producer.notify_external_physical_exemplar_upsert(
            physical_exemplar=physical_exemplar,
        )

        # Assert
        self.mock_producer.publish.assert_called_once_with(
            message=Message(
                queue_name="external.physical_exemplar.upsert",
                message=physical_exemplar.model_dump_json(),
            ),
        )
