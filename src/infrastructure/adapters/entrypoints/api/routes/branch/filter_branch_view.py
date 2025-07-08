from typing import Annotated, List

from fastapi import Query, status

from src.application.dto.branch import BranchFilter, BranchResponse
from src.application.usecase.branch.filter_branch import FilterBranch
from src.domain.entities.branch import BranchFilter as BranchFilterEntity
from src.infrastructure.adapters.entrypoints.api.routes.branch.branch_basic_router import (
    BranchBasicRouter,
)


class FilterBranchView(BranchBasicRouter):
    def __init__(self, use_case: FilterBranch):
        super().__init__(use_case=use_case)

    def _add_to_router(self) -> None:
        if self.router is not None:
            self.router.add_api_route(
                "/",
                self._call_use_case,
                status_code=status.HTTP_200_OK,
                response_model=List[BranchResponse],
                response_model_exclude_unset=True,
                response_model_exclude_none=True,
                methods=["GET"],
                description="Get Branch by filter",
            )

    def _call_use_case(
        self,
        filter: Annotated[BranchFilter, Query()],
    ) -> List[BranchResponse]:
        filter_entity = BranchFilterEntity.model_validate(filter)
        branches = self.use_case.execute(filter_entity)  # type: ignore
        return [BranchResponse.model_validate(branch) for branch in branches]
