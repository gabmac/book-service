from uuid import UUID

from fastapi import HTTPException, status

from src.application.dto.book_dto import BookResponse
from src.application.exceptions import NotFoundException
from src.application.usecase.book.get_book_by_id import GetBookById
from src.infrastructure.adapters.entrypoints.api.routes.book.book_basic_router import (
    BookBasicRouter,
)


class GetBookView(BookBasicRouter):
    def __init__(self, use_case: GetBookById):
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
                response_model=BookResponse,
                response_model_exclude_unset=True,
                response_model_exclude_none=True,
                methods=["GET"],
                description="Get Book by ID",
            )

    def _call_use_case(self, id: UUID) -> BookResponse:
        try:
            book = self.use_case.execute(id)  # type: ignore
            return BookResponse.model_validate(book)
        except NotFoundException as e:
            raise HTTPException(status_code=404, detail=e.message)
