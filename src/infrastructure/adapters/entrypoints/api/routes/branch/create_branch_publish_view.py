from fastapi import status

from src.application.dto.branch import BranchUpsert, ProcessingBranch
from src.application.usecase.branch.upsert_branch_produce import UpsertBranchProduce
from src.domain.entities.branch import Branch
from src.infrastructure.adapters.entrypoints.api.routes.branch.branch_basic_router import (
    BranchBasicRouter,
)


class PublishCreateBranchView(BranchBasicRouter):
    def __init__(self, use_case: UpsertBranchProduce):
        super().__init__(use_case=use_case)

    def _add_to_router(self) -> None:
        if self.router is not None:
            self.router.add_api_route(
                "/",
                self._call_use_case,
                status_code=status.HTTP_202_ACCEPTED,
                response_model=ProcessingBranch,
                response_model_exclude_none=True,
                response_model_exclude_unset=True,
                methods=["POST"],
                description="Create Branch",
            )

    def _call_use_case(self, payload: BranchUpsert) -> ProcessingBranch:
        branch = Branch(
            name=payload.name,
            created_by=payload.user,
            updated_by=payload.user,
            version=1,
        )
        branch = self.use_case.execute(branch)  # type: ignore
        return ProcessingBranch(branch=branch)
