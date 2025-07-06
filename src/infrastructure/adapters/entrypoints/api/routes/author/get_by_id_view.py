from fastapi import status

from src.application.dto.author import AuthorResponse
from src.application.usecase.author.get_by_id import GetAuthorById
from src.infrastructure.adapters.entrypoints.api.routes.author.author_basic_router import (
    AuthorBasicRouter,
)


class GetAuthorView(AuthorBasicRouter):
    def __init__(self, use_case: GetAuthorById):
        super().__init__(use_case=use_case)

    def _add_to_router(self) -> None:
        """
        Add to view to router
        """
        if self.router is not None:
            self.router.add_api_route(
                "/{id}",
                self.use_case.execute,  # type: ignore
                status_code=status.HTTP_200_OK,
                response_model=AuthorResponse,
                response_model_exclude_unset=True,
                response_model_exclude_none=True,
                methods=["GET"],
                description="Get Author by ID",
            )
