from abc import ABC, abstractmethod
from uuid import UUID

from src.domain.entities.physical_exemplar import PhysicalExemplar


class PhysicalExemplarReadRepositoryPort(ABC):
    @abstractmethod
    def get_physical_exemplar_by_book_and_branch(
        self,
        book_id: UUID,
        branch_id: UUID,
    ) -> PhysicalExemplar:
        pass


class PhysicalExemplarWriteRepositoryPort(ABC):
    @abstractmethod
    def upsert_physical_exemplar(
        self,
        physical_exemplar: PhysicalExemplar,
    ) -> PhysicalExemplar:
        pass
