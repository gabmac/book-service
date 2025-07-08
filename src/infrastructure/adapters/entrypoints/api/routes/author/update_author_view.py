from uuid import UUID

from fastapi import HTTPException, status

from src.application.dto.author import AuthorResponse, AuthorUpsert, ProcessingAuthor
from src.application.exceptions import NotFoundException
from src.application.usecase.author.get_by_id import GetAuthorById
from src.application.usecase.author.update_author_produce import UpdateAuthorProduce
from src.domain.entities.author import Author
from src.infrastructure.adapters.entrypoints.api.routes.author.author_basic_router import (
    AuthorBasicRouter,
)


class PublishUpdateAuthorView(AuthorBasicRouter):
    def __init__(self, use_case: UpdateAuthorProduce, validate_author: GetAuthorById):
        super().__init__(use_case=use_case)
        self.validate_author = validate_author

    def _add_to_router(self) -> None:
        """
        Add to view to router
        """
        if self.router is not None:
            self.router.add_api_route(
                "/{id}",
                self._call_use_case,  # type: ignore
                status_code=status.HTTP_202_ACCEPTED,
                response_model=ProcessingAuthor,
                response_model_exclude_none=True,
                response_model_exclude_unset=True,
                methods=["PUT"],
                description="Update Author",
            )

    async def _call_use_case(self, payload: AuthorUpsert, id: UUID) -> ProcessingAuthor:
        try:
            existing_author = self.validate_author.execute(id)
        except NotFoundException as e:
            raise HTTPException(status_code=404, detail=e.message)

        author = Author(
            id=id,
            name=payload.name,
            created_by=existing_author.created_by,
            updated_by=payload.user,
            created_at=existing_author.created_at,
            updated_at=existing_author.updated_at,
        )
        author = await self.use_case.execute(author)  # type: ignore
        return ProcessingAuthor(author=AuthorResponse.model_validate(author))  # type: ignore
