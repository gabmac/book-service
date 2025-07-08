from typing import Annotated, List

from fastapi import Query, status

from src.application.dto.book_category import BookCategoryResponse
from src.application.usecase.book_category.book_category_filter import (
    FilterBookCategory,
)
from src.domain.entities.book_category import BookCategoryFilter
from src.infrastructure.adapters.entrypoints.api.routes.book_category.book_category_basic_router import (
    BookCategoryBasicRouter,
)


class FilterBookCategoryView(BookCategoryBasicRouter):
    def __init__(self, use_case: FilterBookCategory):
        super().__init__(use_case=use_case)

    def _add_to_router(self) -> None:
        if self.router is not None:
            self.router.add_api_route(
                "/",
                self._call_use_case,
                status_code=status.HTTP_200_OK,
                response_model=List[BookCategoryResponse],
                response_model_exclude_unset=True,
                response_model_exclude_none=True,
                methods=["GET"],
                description="Get Book Category by ID",
            )

    def _call_use_case(
        self,
        filter: Annotated[BookCategoryFilter, Query()],
    ) -> List[BookCategoryResponse]:
        return [
            BookCategoryResponse.model_validate(book_category)
            for book_category in self.use_case.execute(filter)  # type: ignore
        ]
