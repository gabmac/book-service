from uuid import UUID

from fastapi import HTTPException, status

from src.application.dto.book_dto import Book as BookDto
from src.application.dto.book_dto import BookResponse, ProcessingBook
from src.application.exceptions import NotFoundException
from src.application.usecase.book.get_book_by_id import GetBookById
from src.application.usecase.book.upsert_book_produce import UpsertBookProduce
from src.domain.entities.book import Book
from src.domain.entities.book_data import BookData
from src.infrastructure.adapters.entrypoints.api.routes.book.book_basic_router import (
    BookBasicRouter,
)


class PublishUpdateBookView(BookBasicRouter):
    def __init__(self, use_case: UpsertBookProduce, validate_book: GetBookById):
        super().__init__(use_case=use_case)
        self.validate_book = validate_book

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
        user = payload.user
        try:
            old_book = self.validate_book.execute(id)
            user = old_book.created_by
        except NotFoundException as e:
            raise HTTPException(status_code=404, detail=e.message)

        book_data = [
            BookData(
                summary=book_data.summary,
                title=book_data.title,
                language=book_data.language,
                created_by=payload.user,
                updated_by=payload.user,
            )
            for book_data in payload.book_data
        ]
        book = Book(
            id=id,
            isbn_code=payload.isbn_code,
            editor=payload.editor,
            edition=payload.edition,
            type=payload.type,
            publish_date=payload.publish_date,
            author_ids=payload.author_ids,
            category_ids=payload.category_ids,
            book_data=book_data,
            updated_by=payload.user,
            created_by=user,
        )
        try:
            book = await self.use_case.execute(book)  # type: ignore
        except NotFoundException as e:
            raise HTTPException(status_code=404, detail=e.message)
        return ProcessingBook(book=BookResponse.model_validate(book))  # type: ignore
