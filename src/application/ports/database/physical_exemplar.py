from abc import ABC, abstractmethod
from typing import List
from uuid import UUID

from src.domain.entities.book import BookFilter
from src.domain.entities.physical_exemplar import PhysicalExemplar


class PhysicalExemplarRepositoryPort(ABC):
    @abstractmethod
    def upsert_physical_exemplar(
        self,
        physical_exemplar: PhysicalExemplar,
    ) -> PhysicalExemplar:
        pass

    @abstractmethod
    def filter_by_branch_and_book_filter(
        self,
        branch_id: UUID,
        book_filter: BookFilter,
    ) -> List[PhysicalExemplar]:
        pass

    # TODO: Remove unit test
    @abstractmethod
    def get_physical_exemplar_by_book_and_branch(
        self,
        book_id: UUID,
        branch_id: UUID,
    ) -> PhysicalExemplar:
        pass
