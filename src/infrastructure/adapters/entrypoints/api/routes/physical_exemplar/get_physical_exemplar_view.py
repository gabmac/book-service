from uuid import UUID

from fastapi import HTTPException, status

from src.application.dto.physical_exemplar import PhysicalExemplarResponse
from src.application.exceptions import NotFoundException
from src.application.usecase.physical_exemplar.get_physical_exemplar_by_book_and_branch import (
    GetPhysicalExemplarByBookAndBranch,
)
from src.infrastructure.adapters.entrypoints.api.routes.physical_exemplar.physical_exemplar_basic_router import (
    PhysicalExemplarBasicRouter,
)


class GetPhysicalExemplarView(PhysicalExemplarBasicRouter):
    def __init__(self, use_case: GetPhysicalExemplarByBookAndBranch):
        super().__init__(use_case=use_case)

    def _add_to_router(self) -> None:
        """
        Add to view to router
        """
        if self.router is not None:
            self.router.add_api_route(
                "/branch/{branch_id}/book/{book_id}/",
                self._call_use_case,
                status_code=status.HTTP_200_OK,
                response_model=PhysicalExemplarResponse,
                response_model_exclude_unset=True,
                response_model_exclude_none=True,
                methods=["GET"],
                description="Get Physical Exemplar by Book and Branch ID",
            )

    def _call_use_case(
        self,
        book_id: UUID,
        branch_id: UUID,
    ) -> PhysicalExemplarResponse:
        try:
            physical_exemplar = self.use_case.execute(  # type: ignore
                book_id=book_id,
                branch_id=branch_id,
            )
            return PhysicalExemplarResponse.model_validate(physical_exemplar)
        except NotFoundException as e:
            raise HTTPException(status_code=404, detail=e.message)
