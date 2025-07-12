from uuid import UUID

from sqlalchemy.exc import NoResultFound
from sqlmodel import select

from src.application.exceptions import NotFoundException
from src.application.ports.database.physical_exemplar import (
    PhysicalExemplarReadRepositoryPort,
)
from src.domain.entities.physical_exemplar import PhysicalExemplar
from src.infrastructure.adapters.database.db.session import DatabaseSettings
from src.infrastructure.adapters.database.models.physical_exemplar import (
    PhysicalExemplar as PhysicalExemplarModel,
)


class PhysicalExemplarReadRepository(PhysicalExemplarReadRepositoryPort):
    def __init__(self, db: DatabaseSettings) -> None:
        self.db = db

    def get_physical_exemplar_by_book_and_branch(
        self,
        book_id: UUID,
        branch_id: UUID,
    ) -> PhysicalExemplar:
        with self.db.get_session(slave=True) as session:
            try:
                physical_exemplar_model = session.exec(
                    select(PhysicalExemplarModel).where(
                        PhysicalExemplarModel.book_id == book_id,
                        PhysicalExemplarModel.branch_id == branch_id,
                    ),
                ).one()
            except NoResultFound:
                raise NotFoundException("Physical exemplar not found")
            return PhysicalExemplar.model_validate(physical_exemplar_model)
