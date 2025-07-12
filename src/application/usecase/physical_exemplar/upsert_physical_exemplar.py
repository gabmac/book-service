from src.application.ports.database.physical_exemplar import (
    PhysicalExemplarRepositoryPort,
)
from src.application.ports.producer.physical_exemplar_producer import (
    PhysicalExemplarProducerPort,
)
from src.domain.entities.physical_exemplar import PhysicalExemplar


class UpsertPhysicalExemplar:
    def __init__(
        self,
        repository: PhysicalExemplarRepositoryPort,
        physical_exemplar_producer: PhysicalExemplarProducerPort,
    ):
        self.repository = repository
        self.physical_exemplar_producer = physical_exemplar_producer

    def execute(self, physical_exemplar: PhysicalExemplar) -> PhysicalExemplar:
        self.physical_exemplar_producer.notify_external_physical_exemplar_upsert(
            physical_exemplar,
        )
        physical_exemplar = self.repository.upsert_physical_exemplar(physical_exemplar)
        return physical_exemplar
