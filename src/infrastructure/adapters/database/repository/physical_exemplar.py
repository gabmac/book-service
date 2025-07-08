from sqlmodel import select

from src.application.ports.database.physical_exemplar import (
    PhysicalExemplarRepositoryPort,
)
from src.domain.entities.physical_exemplar import PhysicalExemplar
from src.infrastructure.adapters.database.db.session import DatabaseSettings
from src.infrastructure.adapters.database.models.physical_exemplar import (
    PhysicalExemplar as PhysicalExemplarModel,
)


class PhysicalExemplarRepository(PhysicalExemplarRepositoryPort):
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
                    ]:  # Preserve creation metadata
                        setattr(existing, k, v)
                physical_exemplar_model = existing
            else:
                # Create new record
                physical_exemplar_model = PhysicalExemplarModel.model_validate(
                    physical_exemplar,
                )
                session.add(physical_exemplar_model)

            session.flush()
            session.commit()
            session.refresh(physical_exemplar_model)
            return PhysicalExemplar.model_validate(physical_exemplar_model)
