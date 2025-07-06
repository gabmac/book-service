from typing import Annotated, List

from fastapi import Query, status

from src.application.dto.book_dto import BookFilter, BookResponse
from src.application.usecase.book.get_book_by_id import GetBookById
from src.domain.entities.book import BookFilter as BookFilterEntity
from src.infrastructure.adapters.entrypoints.api.routes.book.book_basic_router import (
    BookBasicRouter,
)


class FilterBookView(BookBasicRouter):
    def __init__(self, use_case: GetBookById):
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
                description="Get Book by ID",
            )

    def _call_use_case(
        self,
        filter: Annotated[BookFilter, Query()],
    ) -> List[BookResponse]:
        filter_entity = BookFilterEntity(
            isbn_code=filter.isbn_code,
            editor=filter.editor,
            edition=filter.edition,
            type=filter.type,
            publish_date=filter.publish_date,
        )
        books = self.use_case.execute(filter_entity)  # type: ignore
        return [BookResponse.model_validate(book) for book in books]
