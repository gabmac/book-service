from fastapi import status

from src.application.dto.author import AuthorResponse, AuthorUpsert, ProcessingAuthor
from src.application.usecase.author.create_author import CreateAuthorProduce
from src.domain.entities.author import Author
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
                self._call_use_case,  # type: ignore
                status_code=status.HTTP_202_ACCEPTED,
                methods=["POST"],
                description="Create Author",
            )

    async def _call_use_case(self, payload: AuthorUpsert) -> ProcessingAuthor:
        author = Author(
            name=payload.name,
            created_by=payload.user,
            updated_by=payload.user,
        )
        author = await self.use_case.execute(author)  # type: ignore
        return ProcessingAuthor(author=AuthorResponse.model_validate(author))  # type: ignore
