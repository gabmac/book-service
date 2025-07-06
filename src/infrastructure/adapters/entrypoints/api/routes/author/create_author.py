from fastapi import status

from src.application.usecase.author.create_author import CreateAuthorProduce
from src.infrastructure.adapters.entrypoints.api.routes.author.author_basic_router import (
    AuthorBasicRouter,
)


class PublishCreateAuthorView(AuthorBasicRouter):
    def __init__(self, use_case: CreateAuthorProduce):
        super().__init__(use_case=use_case)

    def _add_to_router(self) -> None:
        """
        Add to view to router
        """
        if self.router is not None:
            self.router.add_api_route(
                "/",
                self.use_case.execute,  # type: ignore
                status_code=status.HTTP_202_ACCEPTED,
                methods=["POST"],
                description="Create Author",
            )
