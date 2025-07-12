from sqlmodel import select

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
                # Update existing record
                for k, v in physical_exemplar.model_dump().items():
                    if k not in [
                        "id",
                        "created_at",
                        "created_by",
                        "branch_id",
                        "book_id",
                        "branch",
                        "book",
                    ]:  # Preserve creation metadata
                        setattr(existing, k, v)
                physical_exemplar_model = existing
            else:
                # Create new record
                physical_exemplar_model = PhysicalExemplarModel(
                    id=physical_exemplar.id,
                    available=physical_exemplar.available,
                    room=physical_exemplar.room,
                    floor=physical_exemplar.floor,
                    bookshelf=physical_exemplar.bookshelf,
                    book_id=physical_exemplar.book_id,
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
