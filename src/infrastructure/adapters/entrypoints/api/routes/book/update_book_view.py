from uuid import UUID

from fastapi import HTTPException, status

from src.application.dto.book_dto import Book as BookDto
from src.application.dto.book_dto import BookResponse, ProcessingBook
from src.application.exceptions import NotFoundException
from src.application.usecase.book.update_book_produce import UpdateBookProduce
from src.domain.entities.book import Book
from src.infrastructure.adapters.entrypoints.api.routes.book.book_basic_router import (
    BookBasicRouter,
)


class PublishUpdateBookView(BookBasicRouter):
    def __init__(self, use_case: UpdateBookProduce):
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
                response_model=ProcessingBook,
                response_model_exclude_none=True,
                response_model_exclude_unset=True,
                methods=["PUT"],
                description="Update Book",
            )

    async def _call_use_case(self, payload: BookDto, id: UUID) -> ProcessingBook:
        book = Book(
            id=id,
            isbn_code=payload.isbn_code,
            editor=payload.editor,
            edition=payload.edition,
            type=payload.type,
            publish_date=payload.publish_date,
            author_ids=payload.author_ids,
            created_by=payload.user,
            updated_by=payload.user,
        )
        try:
            book = await self.use_case.execute(book)  # type: ignore
        except NotFoundException as e:
            raise HTTPException(status_code=404, detail=e.message)
        return ProcessingBook(book=BookResponse.model_validate(book))  # type: ignore
