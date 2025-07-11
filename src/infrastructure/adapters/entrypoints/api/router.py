from fastapi import APIRouter

from src.application.usecase.author.create_author import CreateAuthorProduce
from src.application.usecase.author.delete_author_publish import DeleteAuthorPublish
from src.application.usecase.author.filter_author import FilterAuthor
from src.application.usecase.author.get_by_id import GetAuthorById
from src.application.usecase.author.update_author_produce import UpdateAuthorProduce
from src.application.usecase.book.delete_book_publish import DeleteBookPublish
from src.application.usecase.book.filter_book import FilterBook
from src.application.usecase.book.get_book_by_id import GetBookById
from src.application.usecase.book.upsert_book_produce import UpsertBookProduce
from src.application.usecase.book_category.book_category_filter import (
    FilterBookCategory,
)
from src.application.usecase.book_category.book_category_publish import (
    CreateBookCategoryProduce,
)
from src.application.usecase.branch.filter_branch import FilterBranch
from src.application.usecase.branch.upsert_branch_produce import UpsertBranchProduce
from src.application.usecase.physical_exemplar.upsert_physical_exemplar_produce import (
    UpsertPhysicalExemplarProduce,
)
from src.infrastructure.adapters.database.repository.author import AuthorRepository
from src.infrastructure.adapters.database.repository.book import BookRepository
from src.infrastructure.adapters.database.repository.book_category import (
    BookCategoryRepository,
)
from src.infrastructure.adapters.database.repository.branch import BranchRepository
from src.infrastructure.adapters.database.repository.physical_exemplar import (
    PhysicalExemplarRepository,
)
from src.infrastructure.adapters.entrypoints.api.monitoring import (
    router as monitoring_router,
)
from src.infrastructure.adapters.entrypoints.api.routes.author.create_author import (
    PublishCreateAuthorView,
)
from src.infrastructure.adapters.entrypoints.api.routes.author.delete_publish_view import (
    PublishDeleteAuthorView,
)
from src.infrastructure.adapters.entrypoints.api.routes.author.filter_author_view import (
    FilterAuthorView,
)
from src.infrastructure.adapters.entrypoints.api.routes.author.get_by_id_view import (
    GetAuthorView,
)
from src.infrastructure.adapters.entrypoints.api.routes.author.update_author_view import (
    PublishUpdateAuthorView,
)
from src.infrastructure.adapters.entrypoints.api.routes.book.create_book_view import (
    PublishCreateBookView,
)
from src.infrastructure.adapters.entrypoints.api.routes.book.delete_publish_view import (
    PublishDeleteBookView,
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
from src.infrastructure.adapters.entrypoints.api.routes.book_category.create_book_category_publish_view import (
    UpsertBookCategoryPublishView,
)
from src.infrastructure.adapters.entrypoints.api.routes.book_category.filter_book_category_view import (
    FilterBookCategoryView,
)
from src.infrastructure.adapters.entrypoints.api.routes.branch.create_branch_publish_view import (
    PublishCreateBranchView,
)
from src.infrastructure.adapters.entrypoints.api.routes.branch.filter_branch_view import (
    FilterBranchView,
)
from src.infrastructure.adapters.entrypoints.api.routes.physical_exemplar.create_physical_exemplar_publish_view import (
    PublishCreatePhysicalExemplarView,
)
from src.infrastructure.adapters.entrypoints.producer import Producer
from src.infrastructure.adapters.producer.author_producer import AuthorProducerAdapter
from src.infrastructure.adapters.producer.book_category_producer import (
    BookCategoryProducerAdapter,
)
from src.infrastructure.adapters.producer.book_producer import BookProducerAdapter
from src.infrastructure.adapters.producer.branch_producer import BranchProducerAdapter
from src.infrastructure.adapters.producer.physical_exemplar_producer import (
    PhysicalExemplarProducerAdapter,
)


class Initializer:
    def __init__(
        self,
        producer: Producer,
        book_repository: BookRepository,
        author_repository: AuthorRepository,
        book_category_repository: BookCategoryRepository,
    ):
        self.api_router = APIRouter(prefix="/api")
        self.api_router.include_router(monitoring_router)

        self.book_producer = BookProducerAdapter(producer=producer)

        self.upsert_book_use_case = UpsertBookProduce(
            producer=self.book_producer,
            author_repository=author_repository,
            book_category_repository=book_category_repository,
        )
        self.publish_create_book_view = PublishCreateBookView(self.upsert_book_use_case)
        self.api_router.include_router(self.publish_create_book_view.router)  # type: ignore

        self.get_book_by_id_use_case = GetBookById(book_repository=book_repository)
        self.get_book_by_id_view = GetBookView(self.get_book_by_id_use_case)
        self.api_router.include_router(self.get_book_by_id_view.router)  # type: ignore

        self.filter_book_use_case = FilterBook(book_repository=book_repository)
        self.filter_book_view = FilterBookView(self.filter_book_use_case)
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

        self.update_author_use_case = UpdateAuthorProduce(producer=self.author_producer)
        self.publish_update_author_view = PublishUpdateAuthorView(
            self.update_author_use_case,
            self.get_author_by_id_use_case,
        )
        self.api_router.include_router(self.publish_update_author_view.router)  # type: ignore

        self.get_book_by_id_use_case = GetBookById(book_repository=book_repository)
        self.publish_update_book_view = PublishUpdateBookView(
            self.upsert_book_use_case,
            self.get_book_by_id_use_case,
        )
        self.api_router.include_router(self.publish_update_book_view.router)  # type: ignore

        self.delete_author_use_case_publish = DeleteAuthorPublish(
            author_producer=self.author_producer,
        )
        self.publish_delete_author_view = PublishDeleteAuthorView(
            self.delete_author_use_case_publish,
        )
        self.api_router.include_router(self.publish_delete_author_view.router)  # type: ignore

        self.delete_book_use_case_publish = DeleteBookPublish(
            book_producer=self.book_producer,
        )
        self.publish_delete_book_view = PublishDeleteBookView(
            self.delete_book_use_case_publish,
        )
        self.api_router.include_router(self.publish_delete_book_view.router)  # type: ignore

        self.book_category_producer = BookCategoryProducerAdapter(producer=producer)

        self.create_book_category_use_case = CreateBookCategoryProduce(
            book_category_producer=self.book_category_producer,
            repository=book_category_repository,
        )
        self.publish_create_book_category_view = UpsertBookCategoryPublishView(
            self.create_book_category_use_case,
        )
        self.api_router.include_router(self.publish_create_book_category_view.router)  # type: ignore

        self.filter_book_category_use_case = FilterBookCategory(
            repository=book_category_repository,
        )
        self.filter_book_category_view = FilterBookCategoryView(
            self.filter_book_category_use_case,
        )
        self.api_router.include_router(self.filter_book_category_view.router)  # type: ignore

        self.branch_repository = BranchRepository(db=book_repository.db)
        self.filter_branch_use_case = FilterBranch(repository=self.branch_repository)
        self.filter_branch_view = FilterBranchView(self.filter_branch_use_case)
        self.api_router.include_router(self.filter_branch_view.router)  # type: ignore

        self.branch_producer = BranchProducerAdapter(producer=producer)
        self.upsert_branch_use_case = UpsertBranchProduce(
            branch_producer=self.branch_producer,
            repository=self.branch_repository,
        )
        self.publish_create_branch_view = PublishCreateBranchView(
            self.upsert_branch_use_case,
        )
        self.api_router.include_router(self.publish_create_branch_view.router)  # type: ignore

        self.physical_exemplar_repository = PhysicalExemplarRepository(
            db=book_repository.db,
        )
        self.physical_exemplar_producer = PhysicalExemplarProducerAdapter(
            producer=producer,
        )
        self.upsert_physical_exemplar_use_case = UpsertPhysicalExemplarProduce(
            physical_exemplar_producer=self.physical_exemplar_producer,
            repository=self.physical_exemplar_repository,
            book_repository=book_repository,
            branch_repository=self.branch_repository,
        )
        self.publish_create_physical_exemplar_view = PublishCreatePhysicalExemplarView(
            self.upsert_physical_exemplar_use_case,
        )
        self.api_router.include_router(self.publish_create_physical_exemplar_view.router)  # type: ignore
