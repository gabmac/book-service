from uuid import UUID

from fastapi import status

from src.application.usecase.author.delete_author_publish import DeleteAuthorPublish
from src.infrastructure.adapters.entrypoints.api.routes.author.author_basic_router import (
    AuthorBasicRouter,
)


class PublishDeleteAuthorView(AuthorBasicRouter):
    def __init__(self, use_case: DeleteAuthorPublish):
        super().__init__(use_case=use_case)

    def _add_to_router(self) -> None:
        """
        Add to view to router
        """
        if self.router is not None:
            self.router.add_api_route(
                "/",
                self._call_use_case,  # type: ignore
                status_code=status.HTTP_202_ACCEPTED,
                response_model_exclude_none=True,
                response_model_exclude_unset=True,
                methods=["DELETE"],
                description="Delete Author",
            )

    async def _call_use_case(self, id: UUID) -> None:
        self.use_case.execute(id)  # type: ignore
