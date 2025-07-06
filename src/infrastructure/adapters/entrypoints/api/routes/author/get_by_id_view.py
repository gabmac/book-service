from uuid import UUID

from fastapi import HTTPException, status

from src.application.dto.author import AuthorResponse
from src.application.exceptions import NotFoundException
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
                self._call_use_case,  # type: ignore
                status_code=status.HTTP_200_OK,
                response_model=AuthorResponse,
                response_model_exclude_unset=True,
                response_model_exclude_none=True,
                methods=["GET"],
                description="Get Author by ID",
            )

    async def _call_use_case(self, id: UUID) -> AuthorResponse:
        try:
            author = self.use_case.execute(id)  # type: ignore
            return AuthorResponse.model_validate(author)  # type: ignore
        except NotFoundException as e:
            raise HTTPException(status_code=404, detail=e.message)
