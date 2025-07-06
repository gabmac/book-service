from typing import Annotated, List

from fastapi import Query, status

from src.application.dto.author import AuthorFilter, AuthorResponse
from src.application.usecase.author.filter_author import FilterAuthor
from src.infrastructure.adapters.entrypoints.api.routes.author.author_basic_router import (
    AuthorBasicRouter,
)


class FilterAuthorView(AuthorBasicRouter):
    def __init__(self, use_case: FilterAuthor):
        super().__init__(use_case=use_case)

    def _add_to_router(self) -> None:
        """
        Add to view to router
        """
        if self.router is not None:
            self.router.add_api_route(
                "/",
                self._call_use_case,  # type: ignore
                status_code=status.HTTP_200_OK,
                response_model=List[AuthorResponse],
                response_model_exclude_unset=True,
                response_model_exclude_none=True,
                methods=["GET"],
                description="Get Author by filter",
            )

    def _call_use_case(
        self,
        filter: Annotated[AuthorFilter, Query()],
    ) -> List[AuthorResponse]:
        return self.use_case.execute(filter)  # type: ignore
