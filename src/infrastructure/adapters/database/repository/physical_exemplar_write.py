from sqlmodel import and_, select, update

from src.application.exceptions import OptimisticLockException
from src.application.ports.database.physical_exemplar import (
    PhysicalExemplarWriteRepositoryPort,
)
from src.domain.entities.physical_exemplar import PhysicalExemplar
from src.infrastructure.adapters.database.db.session import DatabaseSettings
from src.infrastructure.adapters.database.models.physical_exemplar import (
    PhysicalExemplar as PhysicalExemplarModel,
)


class PhysicalExemplarWriteRepository(PhysicalExemplarWriteRepositoryPort):
    def __init__(self, db: DatabaseSettings) -> None:
        self.db = db

    def upsert_physical_exemplar(
        self,
        physical_exemplar: PhysicalExemplar,
    ) -> PhysicalExemplar:
        with self.db.get_session() as session:
            # First try to find by book_id and branch_id for idempotency
            existing = session.exec(
                select(PhysicalExemplarModel).where(
                    PhysicalExemplarModel.book_id == physical_exemplar.book_id,
                    PhysicalExemplarModel.branch_id == physical_exemplar.branch_id,
                ),
            ).first()

            if existing:
                statement = (
                    update(PhysicalExemplarModel)
                    .where(
                        and_(
                            PhysicalExemplarModel.id == physical_exemplar.id,
                            PhysicalExemplarModel.version
                            == physical_exemplar.version - 1,
                        ),
                    )
                    .values(
                        **physical_exemplar.model_dump(
                            exclude={"book", "branch"},
                            exclude_none=True,
                            exclude_unset=True,
                            mode="json",
                        )
                    )
                )
                result = session.exec(statement)  # type: ignore
                if result.rowcount == 0:  # type: ignore
                    raise OptimisticLockException(
                        f"""Optimistic lock failed for physical exemplar {physical_exemplar.id}.
                        Expected version {physical_exemplar.version - 1},
                        but data may have been modified by another transaction.""",
                    )
                return physical_exemplar
            else:
                # Create new record
                physical_exemplar_model = PhysicalExemplarModel(
                    id=physical_exemplar.id,
                    available=physical_exemplar.available,
                    room=physical_exemplar.room,
                    floor=physical_exemplar.floor,
                    bookshelf=physical_exemplar.bookshelf,
                    book_id=physical_exemplar.book_id,
                    version=physical_exemplar.version,
                    branch_id=physical_exemplar.branch_id,
                    created_at=physical_exemplar.created_at,
                    created_by=physical_exemplar.created_by,
                    updated_at=physical_exemplar.updated_at,
                    updated_by=physical_exemplar.updated_by,
                )

            session.add(physical_exemplar_model)
            session.flush()
            session.commit()
            session.refresh(physical_exemplar_model)
            return PhysicalExemplar.model_validate(physical_exemplar_model)
