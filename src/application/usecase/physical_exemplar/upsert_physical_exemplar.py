from src.application.ports.database.physical_exemplar import (
    PhysicalExemplarRepositoryPort,
)
from src.domain.entities.physical_exemplar import PhysicalExemplar


class UpsertPhysicalExemplar:
    def __init__(self, repository: PhysicalExemplarRepositoryPort):
        self.repository = repository

    def execute(self, physical_exemplar: PhysicalExemplar) -> PhysicalExemplar:
        return self.repository.upsert_physical_exemplar(physical_exemplar)
