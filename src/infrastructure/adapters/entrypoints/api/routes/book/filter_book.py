from typing import Annotated, List

from fastapi import Query, status

from src.application.dto.book_dto import BookFilter, BookResponse
from src.application.usecase.book.filter_book import FilterBook
from src.infrastructure.adapters.entrypoints.api.routes.book.book_basic_router import (
    BookBasicRouter,
)


class FilterBookView(BookBasicRouter):
    def __init__(self, use_case: FilterBook):
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
                response_model=List[BookResponse],
                response_model_exclude_unset=True,
                response_model_exclude_none=True,
                methods=["GET"],
                description="Filter Books",
            )

    def _call_use_case(
        self,
        filter: Annotated[BookFilter, Query()],
    ) -> List[BookResponse]:
        books = self.use_case.execute(filter)  # type: ignore
        return [BookResponse.model_validate(book) for book in books]
