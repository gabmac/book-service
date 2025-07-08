from abc import ABC, abstractmethod

from src.domain.entities.physical_exemplar import PhysicalExemplar


class PhysicalExemplarRepositoryPort(ABC):
    @abstractmethod
    def upsert_physical_exemplar(
        self,
        physical_exemplar: PhysicalExemplar,
    ) -> PhysicalExemplar:
        pass
