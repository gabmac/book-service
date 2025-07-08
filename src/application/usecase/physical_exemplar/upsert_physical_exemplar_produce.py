from src.application.ports.database.physical_exemplar import (
    PhysicalExemplarRepositoryPort,
)
from src.application.ports.producer.physical_exemplar_producer import (
    PhysicalExemplarProducerPort,
)
from src.domain.entities.physical_exemplar import PhysicalExemplar


class UpsertPhysicalExemplarProduce:
    def __init__(
        self,
        physical_exemplar_producer: PhysicalExemplarProducerPort,
        repository: PhysicalExemplarRepositoryPort,
    ):
        self.physical_exemplar_producer = physical_exemplar_producer
        self.repository = repository

    def execute(self, physical_exemplar: PhysicalExemplar) -> PhysicalExemplar:
        self.physical_exemplar_producer.upsert_physical_exemplar(physical_exemplar)
        return physical_exemplar
