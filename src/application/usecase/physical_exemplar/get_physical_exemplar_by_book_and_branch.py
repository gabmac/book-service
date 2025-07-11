from uuid import UUID

from src.application.ports.database.physical_exemplar import (
    PhysicalExemplarRepositoryPort,
)
from src.domain.entities.physical_exemplar import PhysicalExemplar


class GetPhysicalExemplarByBookAndBranch:
    def __init__(self, repository: PhysicalExemplarRepositoryPort):
        self.repository = repository

    def execute(self, book_id: UUID, branch_id: UUID) -> PhysicalExemplar:
        return self.repository.get_physical_exemplar_by_book_and_branch(
            book_id=book_id,
            branch_id=branch_id,
        )
