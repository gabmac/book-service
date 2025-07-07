from uuid import UUID

from fastapi import status

from src.application.usecase.book.delete_book_publish import DeleteBookPublish
from src.infrastructure.adapters.entrypoints.api.routes.book.book_basic_router import (
    BookBasicRouter,
)


class PublishDeleteBookView(BookBasicRouter):
    def __init__(self, use_case: DeleteBookPublish):
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
                response_model_exclude_none=True,
                response_model_exclude_unset=True,
                methods=["DELETE"],
                description="Delete Book",
            )

    async def _call_use_case(self, id: UUID) -> None:
        self.use_case.execute(id)  # type: ignore
