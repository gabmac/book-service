from fastapi import APIRouter

from src.application.usecase.create_book import CreateBookProduce
from src.infrastructure.adapters.entrypoints.api.monitoring import (
    router as monitoring_router,
)
from src.infrastructure.adapters.entrypoints.api.routes.book.create_book_view import (
    CreateBookView,
)
from src.infrastructure.adapters.entrypoints.producer import Producer


class Initializer:
    def __init__(self, producer: Producer):
        self.api_router = APIRouter(prefix="/api")
        self.api_router.include_router(monitoring_router)

        self.create_book_use_case = CreateBookProduce(producer=producer)
        self.create_book_view = CreateBookView(self.create_book_use_case)
        self.api_router.include_router(self.create_book_view.router)
