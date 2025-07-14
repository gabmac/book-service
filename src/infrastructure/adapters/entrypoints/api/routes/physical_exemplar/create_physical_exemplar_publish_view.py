from uuid import UUID

from fastapi import HTTPException, status

from src.application.dto.physical_exemplar import (
    PhysicalExemplarCreate,
    ProcessingPhysicalExemplar,
)
from src.application.exceptions import NotFoundException
from src.application.usecase.physical_exemplar.upsert_physical_exemplar_produce import (
    UpsertPhysicalExemplarProduce,
)
from src.domain.entities.physical_exemplar import PhysicalExemplar
from src.infrastructure.adapters.entrypoints.api.routes.physical_exemplar.physical_exemplar_basic_router import (
    PhysicalExemplarBasicRouter,
)


class PublishCreatePhysicalExemplarView(PhysicalExemplarBasicRouter):
    def __init__(self, use_case: UpsertPhysicalExemplarProduce):
        super().__init__(use_case=use_case)

    def _add_to_router(self) -> None:
        if self.router is not None:
            self.router.add_api_route(
                "/branch/{branch_id}/book/{book_id}/",
                self._call_use_case,
                status_code=status.HTTP_202_ACCEPTED,
                response_model=ProcessingPhysicalExemplar,
                response_model_exclude_none=True,
                response_model_exclude_unset=True,
                methods=["PUT"],
                description="Create or Update Physical Exemplar (idempotent - one per book and branch)",
            )

    def _call_use_case(
        self,
        branch_id: UUID,
        book_id: UUID,
        payload: PhysicalExemplarCreate,
    ) -> ProcessingPhysicalExemplar:
        physical_exemplar = PhysicalExemplar(
            available=payload.available,
            room=payload.room,
            floor=payload.floor,
            version=1,
            bookshelf=payload.bookshelf,
            book_id=book_id,
            branch_id=branch_id,
            created_by=payload.user,
            updated_by=payload.user,
        )
        try:
            physical_exemplar = self.use_case.execute(physical_exemplar)  # type: ignore
        except NotFoundException as e:
            raise HTTPException(status_code=404, detail=e.message)
        return ProcessingPhysicalExemplar(physical_exemplar=physical_exemplar)
