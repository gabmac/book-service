from fastapi import APIRouter

from src.application.usecase.author.create_author import CreateAuthorProduce
from src.application.usecase.author.filter_author import FilterAuthor
from src.application.usecase.author.get_by_id import GetAuthorById
from src.application.usecase.book.create_book_produce import CreateBookProduce
from src.application.usecase.book.filter_book import FilterBook
from src.application.usecase.book.get_book_by_id import GetBookById
from src.application.usecase.book.update_book_produce import UpdateBookProduce
from src.infrastructure.adapters.database.repository.author import AuthorRepository
from src.infrastructure.adapters.database.repository.book import BookRepository
from src.infrastructure.adapters.entrypoints.api.monitoring import (
    router as monitoring_router,
)
from src.infrastructure.adapters.entrypoints.api.routes.author.create_author import (
    PublishCreateAuthorView,
)
from src.infrastructure.adapters.entrypoints.api.routes.author.filter_author_view import (
    FilterAuthorView,
)
from src.infrastructure.adapters.entrypoints.api.routes.author.get_by_id_view import (
    GetAuthorView,
)
from src.infrastructure.adapters.entrypoints.api.routes.book.create_book_view import (
    PublishCreateBookView,
)
from src.infrastructure.adapters.entrypoints.api.routes.book.filter_book import (
    FilterBookView,
)
from src.infrastructure.adapters.entrypoints.api.routes.book.get_book_view import (
    GetBookView,
)
from src.infrastructure.adapters.entrypoints.api.routes.book.update_book_view import (
    PublishUpdateBookView,
)
from src.infrastructure.adapters.entrypoints.producer import Producer
from src.infrastructure.adapters.producer.author_producer import AuthorProducerAdapter
from src.infrastructure.adapters.producer.book_producer import BookProducerAdapter


class Initializer:
    def __init__(
        self,
        producer: Producer,
        book_repository: BookRepository,
        author_repository: AuthorRepository,
    ):
        self.api_router = APIRouter(prefix="/api")
        self.api_router.include_router(monitoring_router)

        self.book_producer = BookProducerAdapter(producer=producer)

        self.create_book_use_case = CreateBookProduce(
            producer=self.book_producer,
            author_repository=author_repository,
        )
        self.publish_create_book_view = PublishCreateBookView(self.create_book_use_case)
        self.api_router.include_router(self.publish_create_book_view.router)  # type: ignore

        self.get_book_by_id_use_case = GetBookById(book_repository=book_repository)
        self.get_book_by_id_view = GetBookView(self.get_book_by_id_use_case)
        self.api_router.include_router(self.get_book_by_id_view.router)  # type: ignore

        self.filter_book_use_case = FilterBook(book_repository=book_repository)
        self.filter_book_view = FilterBookView(self.filter_book_use_case)  # type: ignore
        self.api_router.include_router(self.filter_book_view.router)  # type: ignore

        self.author_producer = AuthorProducerAdapter(producer=producer)

        self.create_author_use_case = CreateAuthorProduce(producer=self.author_producer)
        self.publish_create_author_view = PublishCreateAuthorView(
            self.create_author_use_case,
        )
        self.api_router.include_router(self.publish_create_author_view.router)  # type: ignore

        self.get_author_by_id_use_case = GetAuthorById(
            author_repository=author_repository,
        )
        self.get_author_by_id_view = GetAuthorView(self.get_author_by_id_use_case)
        self.api_router.include_router(self.get_author_by_id_view.router)  # type: ignore

        self.filter_author_use_case = FilterAuthor(author_repository=author_repository)
        self.filter_author_view = FilterAuthorView(self.filter_author_use_case)
        self.api_router.include_router(self.filter_author_view.router)  # type: ignore

        self.update_book_use_case = UpdateBookProduce(
            producer=self.book_producer,
            book_repository=book_repository,
            author_repository=author_repository,
        )
        self.publish_update_book_view = PublishUpdateBookView(self.update_book_use_case)
        self.api_router.include_router(self.publish_update_book_view.router)  # type: ignore
