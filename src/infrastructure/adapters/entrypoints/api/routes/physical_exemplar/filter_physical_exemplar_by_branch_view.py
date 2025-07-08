from typing import Annotated, List
from uuid import UUID

from fastapi import Path, Query, status

from src.application.dto.book_dto import BookFilter
from src.application.dto.physical_exemplar import PhysicalExemplarResponse
from src.application.usecase.physical_exemplar.filter_physical_exemplar_by_branch import (
    FilterPhysicalExemplarByBranch,
)
from src.domain.entities.book import BookFilter as BookFilterEntity
from src.infrastructure.adapters.entrypoints.api.routes.physical_exemplar.physical_exemplar_basic_router import (
    PhysicalExemplarBasicRouter,
)


class FilterPhysicalExemplarByBranchView(PhysicalExemplarBasicRouter):
    def __init__(self, use_case: FilterPhysicalExemplarByBranch):
        super().__init__(use_case=use_case)

    def _add_to_router(self) -> None:
        """
        Add filter by branch route to router
        """
        if self.router is not None:
            self.router.add_api_route(
                "/branch/{branch_id}",
                self._call_use_case,
                status_code=status.HTTP_200_OK,
                response_model=List[PhysicalExemplarResponse],
                response_model_exclude_unset=True,
                response_model_exclude_none=True,
                methods=["GET"],
                description="Filter Physical Exemplars by Branch and Book Filters",
            )

    def _call_use_case(
        self,
        branch_id: Annotated[UUID, Path(description="Branch ID")],
        book_filter: Annotated[BookFilter, Query()],
    ) -> List[PhysicalExemplarResponse]:
        # Convert DTO to entity
        book_filter_entity = BookFilterEntity.model_validate(book_filter.model_dump())

        # Execute use case
        physical_exemplars = self.use_case.execute(  # type: ignore
            branch_id=branch_id,
            book_filter=book_filter_entity,
        )

        # Convert entities to response DTOs
        return [
            PhysicalExemplarResponse.model_validate(exemplar.model_dump())
            for exemplar in physical_exemplars
        ]
