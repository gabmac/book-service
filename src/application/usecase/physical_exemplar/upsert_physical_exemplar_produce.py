from src.application.exceptions import NotFoundException
from src.application.ports.database.book import BookRepositoryPort
from src.application.ports.database.branch import BranchRepositoryPort
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
        book_repository: BookRepositoryPort,
        branch_repository: BranchRepositoryPort,
    ):
        self.physical_exemplar_producer = physical_exemplar_producer
        self.repository = repository
        self.book_repository = book_repository
        self.branch_repository = branch_repository

    def execute(self, physical_exemplar: PhysicalExemplar) -> PhysicalExemplar:
        physical_exemplar.book = self.book_repository.get_book_by_id(id=physical_exemplar.book_id)  # type: ignore
        physical_exemplar.branch = self.branch_repository.get_branch_by_id(id=physical_exemplar.branch_id)  # type: ignore

        try:
            old_physical_exemplar = (
                self.repository.get_physical_exemplar_by_book_and_branch(
                    book_id=physical_exemplar.book_id,
                    branch_id=physical_exemplar.branch_id,
                )
            )
            physical_exemplar.created_by = old_physical_exemplar.created_by
            physical_exemplar.created_at = old_physical_exemplar.created_at
            physical_exemplar.id = old_physical_exemplar.id
        except NotFoundException:
            pass

        self.physical_exemplar_producer.upsert_physical_exemplar(physical_exemplar)
        return physical_exemplar
