from fastapi import status

from src.application.dto.book_category import BookCategoryUpsert, ProcessingBookCategory
from src.application.usecase.book_category.book_category_publish import (
    CreateBookCategoryProduce,
)
from src.domain.entities.book_category import BookCategory
from src.infrastructure.adapters.entrypoints.api.routes.book_category.book_category_basic_router import (
    BookCategoryBasicRouter,
)


class UpsertBookCategoryPublishView(BookCategoryBasicRouter):
    def __init__(self, use_case: CreateBookCategoryProduce) -> None:
        super().__init__(use_case=use_case)

    def _add_to_router(self) -> None:
        if self.router is not None:
            self.router.add_api_route(
                "/",
                self._call_use_case,
                status_code=status.HTTP_202_ACCEPTED,
                response_model=ProcessingBookCategory,
                response_model_exclude_none=True,
                response_model_exclude_unset=True,
                methods=["PUT"],
                description="Upsert Book Category",
            )

    def _call_use_case(self, payload: BookCategoryUpsert) -> ProcessingBookCategory:
        new_book_category = BookCategory(
            title=payload.title,
            description=payload.description,
            created_by=payload.user,
            updated_by=payload.user,
        )
        book_category = self.use_case.execute(new_book_category)  # type: ignore
        return ProcessingBookCategory(book_category=book_category)
