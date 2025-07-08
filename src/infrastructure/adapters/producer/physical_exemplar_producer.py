from src.application.dto.producer import Message
from src.application.ports.producer.physical_exemplar_producer import (
    PhysicalExemplarProducerPort,
)
from src.domain.entities.physical_exemplar import PhysicalExemplar
from src.infrastructure.adapters.entrypoints.producer import Producer


class PhysicalExemplarProducerAdapter(PhysicalExemplarProducerPort):
    def __init__(self, producer: Producer):
        self.producer = producer

    def upsert_physical_exemplar(self, physical_exemplar: PhysicalExemplar) -> None:
        self.producer.publish(
            message=Message(
                queue_name="physical_exemplar.upsert",
                message=physical_exemplar.model_dump_json(),
            ),
        )
