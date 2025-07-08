from typing import List
from uuid import UUID

from src.application.ports.database.physical_exemplar import (
    PhysicalExemplarRepositoryPort,
)
from src.domain.entities.book import BookFilter
from src.domain.entities.physical_exemplar import PhysicalExemplar


class FilterPhysicalExemplarByBranch:
    def __init__(self, physical_exemplar_repository: PhysicalExemplarRepositoryPort):
        self.physical_exemplar_repository = physical_exemplar_repository

    def execute(
        self,
        branch_id: UUID,
        book_filter: BookFilter,
    ) -> List[PhysicalExemplar]:
        return self.physical_exemplar_repository.filter_by_branch_and_book_filter(
            branch_id=branch_id,
            book_filter=book_filter,
        )
