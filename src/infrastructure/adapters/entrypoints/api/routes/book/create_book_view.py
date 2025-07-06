from fastapi import status

from src.application.usecase.create_book import CreateBookProduce
from src.infrastructure.adapters.entrypoints.api.routes.book.book_basic_router import (
    BookBasicRouter,
)


class CreateBookView(BookBasicRouter):
    def __init__(self, use_case: CreateBookProduce):
        super().__init__(use_case=use_case)

    def _add_to_router(self) -> None:
        """
        Add to view to router
        """
        if self.router is not None:
            self.router.add_api_route(
                "/",
                self.use_case.execute,  # type: ignore
                status_code=status.HTTP_202_ACCEPTED,
                methods=["POST"],
                description="Create Book",
            )
