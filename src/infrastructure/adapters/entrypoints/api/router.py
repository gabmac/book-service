from fastapi import APIRouter

from src.application.usecase.book.create_book_produce import CreateBookProduce
from src.application.usecase.book.get_book_by_id import GetBookById
from src.infrastructure.adapters.database.repository.book import BookRepository
from src.infrastructure.adapters.entrypoints.api.monitoring import (
    router as monitoring_router,
)
from src.infrastructure.adapters.entrypoints.api.routes.book.create_book_view import (
    PublishCreateBookView,
)
from src.infrastructure.adapters.entrypoints.api.routes.book.get_book_view import (
    GetBookView,
)
from src.infrastructure.adapters.entrypoints.producer import Producer


class Initializer:
    def __init__(self, producer: Producer, book_repository: BookRepository):
        self.api_router = APIRouter(prefix="/api")
        self.api_router.include_router(monitoring_router)

        self.create_book_use_case = CreateBookProduce(producer=producer)
        self.publish_create_book_view = PublishCreateBookView(self.create_book_use_case)
        self.api_router.include_router(self.publish_create_book_view.router)  # type: ignore

        self.get_book_by_id_use_case = GetBookById(book_repository=book_repository)
        self.get_book_by_id_view = GetBookView(self.get_book_by_id_use_case)
        self.api_router.include_router(self.get_book_by_id_view.router)  # type: ignore
