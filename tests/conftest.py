import json
from typing import List
from unittest import IsolatedAsyncioTestCase
from unittest.mock import Mock, patch

from polyfactory.factories.pydantic_factory import ModelFactory
from sqlmodel import text

from src.application.dto.author import AuthorUpsert
from src.application.dto.book_category import BookCategoryUpsert
from src.application.dto.book_dto import Book as BookDto
from src.application.dto.branch import BranchUpsert
from src.application.dto.physical_exemplar import PhysicalExemplarCreate
from src.domain.entities.author import Author
from src.domain.entities.book import Book, BookSearchFilter
from src.domain.entities.book_category import BookCategory
from src.domain.entities.book_data import BookData
from src.domain.entities.branch import Branch
from src.domain.entities.physical_exemplar import PhysicalExemplar
from src.infrastructure.adapters.database.db.session import DatabaseSettings
from src.infrastructure.adapters.database.elasticsearch.client import (
    ElasticsearchClient,
)
from src.infrastructure.adapters.database.repository.author_read import (
    AuthorReadRepository,
)
from src.infrastructure.adapters.database.repository.author_write import (
    AuthorWriteRepository,
)
from src.infrastructure.adapters.database.repository.book_category_read import (
    BookCategoryReadRepository,
)
from src.infrastructure.adapters.database.repository.book_category_write import (
    BookCategoryWriteRepository,
)
from src.infrastructure.adapters.database.repository.book_read import BookReadRepository
from src.infrastructure.adapters.database.repository.book_write import (
    BookWriteRepository,
)
from src.infrastructure.adapters.database.repository.branch_read import (
    BranchReadRepository,
)
from src.infrastructure.adapters.database.repository.branch_write import (
    BranchWriteRepository,
)
from src.infrastructure.adapters.database.repository.physical_exemplar_read import (
    PhysicalExemplarReadRepository,
)
from src.infrastructure.adapters.database.repository.physical_exemplar_write import (
    PhysicalExemplarWriteRepository,
)
from src.infrastructure.settings.config import (
    ElasticsearchConfig,
    ElasticsearchIndexConfig,
)


class BookModelFactory(ModelFactory):
    __model__ = Book


class AuthorModelFactory(ModelFactory):
    __model__ = Author


class BranchModelFactory(ModelFactory):
    __model__ = Branch


class BookCategoryModelFactory(ModelFactory):
    __model__ = BookCategory


class BookDataModelFactory(ModelFactory):
    __model__ = BookData


class PhysicalExemplarModelFactory(ModelFactory):
    __model__ = PhysicalExemplar


class BookFilterModelFactory(ModelFactory):
    __model__ = BookSearchFilter


class BookDtoModelFactory(ModelFactory):
    __model__ = BookDto


class AuthorUpsertModelFactory(ModelFactory):
    __model__ = AuthorUpsert


class BookCategoryUpsertModelFactory(ModelFactory):
    __model__ = BookCategoryUpsert


class BranchUpsertModelFactory(ModelFactory):
    __model__ = BranchUpsert


class PhysicalExemplarCreateModelFactory(ModelFactory):
    __model__ = PhysicalExemplarCreate


class BaseConfTest(IsolatedAsyncioTestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.maxDiff = None
        cls.addClassCleanup(patch.stopall)
        cls.book_model_factory = BookModelFactory
        cls.book_dto_model_factory = BookDtoModelFactory
        cls.book_filter_model_factory = BookFilterModelFactory
        cls.author_model_factory = AuthorModelFactory
        cls.author_upsert_model_factory = AuthorUpsertModelFactory
        cls.branch_model_factory = BranchModelFactory
        cls.book_category_model_factory = BookCategoryModelFactory
        cls.book_category_upsert_model_factory = BookCategoryUpsertModelFactory
        cls.book_data_model_factory = BookDataModelFactory
        cls.physical_exemplar_model_factory = PhysicalExemplarModelFactory
        cls.branch_upsert_model_factory = BranchUpsertModelFactory
        cls.physical_exemplar_create_model_factory = PhysicalExemplarCreateModelFactory

        super().setUpClass()

    def validate_book(self, books: List[Book], expected_book: List[Book]) -> None:
        exclude_book = {
            "book_data",
            "authors",
            "book_categories",
            "created_at",
            "updated_at",
            "author_ids",
            "category_ids",
            "created_by",
            "updated_by",
        }
        results = sorted(expected_book, key=lambda x: x.id)
        books = sorted(books, key=lambda x: x.id)

        for result, book in zip(results, books):
            self.assertDictEqual(
                result.model_dump(
                    mode="json",
                    exclude_none=True,
                    exclude_unset=True,
                    exclude=exclude_book,
                ),
                book.model_dump(
                    mode="json",
                    exclude_none=True,
                    exclude_unset=True,
                    exclude=exclude_book,
                ),
            )

            exclude_book_data = {"created_at", "created_by", "updated_at", "updated_by"}

            self.assertListEqual(
                sorted(
                    (
                        book_data.model_dump(exclude=exclude_book_data, mode="json")  # type: ignore
                        for book_data in result.book_data  # type: ignore
                    ),
                    key=lambda x: x["id"],
                ),  # type: ignore
                sorted(
                    (
                        book_data.model_dump(exclude=exclude_book_data, mode="json")  # type: ignore
                        for book_data in book.book_data  # type: ignore
                    ),
                    key=lambda x: x["id"],
                ),
            )

            exclude_book_category = {
                "created_at",
                "created_by",
                "updated_at",
                "updated_by",
            }
            self.assertListEqual(
                sorted(
                    (
                        book_category.model_dump(exclude=exclude_book_category, mode="json")  # type: ignore
                        for book_category in result.book_categories  # type: ignore
                    ),
                    key=lambda x: x["id"],
                ),
                sorted(
                    (
                        book_category.model_dump(exclude=exclude_book_category, mode="json")  # type: ignore
                        for book_category in book.book_categories
                    ),
                    key=lambda x: x["id"],
                ),
            )

            exclude_author = {"created_at", "created_by", "updated_at", "updated_by"}
            self.assertListEqual(
                sorted(
                    (
                        author.model_dump(exclude=exclude_author, mode="json")  # type: ignore
                        for author in result.authors  # type: ignore
                    ),
                    key=lambda x: x["id"],
                ),
                sorted(
                    (
                        author.model_dump(exclude=exclude_author, mode="json")  # type: ignore
                        for author in book.authors
                    ),
                    key=lambda x: x["id"],
                ),
            )


class BasePostgresRepositoryConfTest(BaseConfTest):
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.db = DatabaseSettings(
            host="localhost",
            password="123456",
            port=5432,
            user="postgres",
            slave_host="localhost",
            slave_port=5433,
        )
        # cls.db.init_db()
        cls.db._pg_trgm_install()

    def tearDown(self):
        super().tearDown()
        with self.db.get_session() as session:
            session.exec(text("DELETE FROM author_book_link"))  # type: ignore
            session.exec(text("DELETE FROM author"))  # type: ignore
            session.exec(text("DELETE FROM physical_exemplar"))  # type: ignore
            session.exec(text("DELETE FROM branch"))  # type: ignore
            session.exec(text("DELETE FROM book_book_category_link"))  # type: ignore
            session.exec(text("DELETE FROM book_category"))  # type: ignore
            session.exec(text("DELETE FROM book_data"))  # type: ignore
            session.exec(text("DELETE FROM book"))  # type: ignore
            session.commit()


class BaseProducerConfTest(BaseConfTest):
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.mock_producer = Mock()


class BaseElasticsearchConfTest(BaseConfTest):
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        # Test Elasticsearch configuration
        cls.elasticsearch_config = ElasticsearchConfig()
        cls.elasticsearch_index_config = ElasticsearchIndexConfig()

        # Create real Elasticsearch client for tests
        cls.elasticsearch_client = ElasticsearchClient(cls.elasticsearch_config)

    def setUp(self):
        super().setUp()
        # Set up test index if using real Elasticsearch
        test_index = self.elasticsearch_index_config.books_index
        if not self.elasticsearch_client.client.indices.exists(index=test_index):
            # Load mappings from file and create index with proper mappings
            with open(self.elasticsearch_index_config.mappings_file_path) as f:
                mappings_data = json.load(f)

            # Extract the books index configuration
            books_config = mappings_data.get("books", {})

            # Create test index with proper mappings
            self.elasticsearch_client.client.indices.create(
                index=test_index,
                body={
                    "settings": books_config.get(
                        "settings",
                        {
                            "number_of_shards": self.elasticsearch_index_config.number_of_shards,
                            "number_of_replicas": self.elasticsearch_index_config.number_of_replicas,
                            "refresh_interval": self.elasticsearch_index_config.refresh_interval,
                        },
                    ),
                    "mappings": books_config.get("mappings", {}),
                },
            )

    def tearDown(self):
        super().tearDown()
        # Clean up Elasticsearch test data
        # Delete test index if it exists
        test_index = self.elasticsearch_index_config.books_index
        if self.elasticsearch_client.client.indices.exists(index=test_index):
            self.elasticsearch_client.client.indices.delete(index=test_index)


class BaseRepositoryConfTest(BasePostgresRepositoryConfTest, BaseElasticsearchConfTest):
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()

        # Initialize read repositories with both PostgreSQL and Elasticsearch
        cls.book_read_repository = BookReadRepository(db=cls.db, elasticsearch_client=cls.elasticsearch_client)  # type: ignore
        cls.book_write_repository = BookWriteRepository(db=cls.db, elasticsearch_client=cls.elasticsearch_client)  # type: ignore
        # Override the Elasticsearch index name for tests
        cls.book_read_repository.es_index = cls.elasticsearch_index_config.books_index
        cls.book_write_repository.es_index = cls.elasticsearch_index_config.books_index

        cls.author_read_repository = AuthorReadRepository(db=cls.db)  # type: ignore
        cls.author_write_repository = AuthorWriteRepository(db=cls.db)  # type: ignore
        cls.branch_read_repository = BranchReadRepository(db=cls.db)  # type: ignore
        cls.branch_write_repository = BranchWriteRepository(db=cls.db)  # type: ignore
        cls.book_category_read_repository = BookCategoryReadRepository(db=cls.db)  # type: ignore
        cls.book_category_write_repository = BookCategoryWriteRepository(db=cls.db)  # type: ignore
        cls.physical_exemplar_read_repository = PhysicalExemplarReadRepository(db=cls.db)  # type: ignore
        cls.physical_exemplar_write_repository = PhysicalExemplarWriteRepository(db=cls.db)  # type: ignore


class BaseUseCaseConfTest(BaseConfTest):
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        # Mock the read repository dependencies
        cls.mock_book_read_repository = Mock()
        cls.mock_author_read_repository = Mock()
        cls.mock_book_category_read_repository = Mock()
        cls.mock_branch_read_repository = Mock()
        cls.mock_physical_exemplar_read_repository = Mock()

        # Mock the write repository dependencies
        cls.mock_book_write_repository = Mock()
        cls.mock_author_write_repository = Mock()
        cls.mock_book_category_write_repository = Mock()
        cls.mock_branch_write_repository = Mock()
        cls.mock_physical_exemplar_write_repository = Mock()

        # Keep the original mocks for backward compatibility during migration
        cls.mock_book_repository = Mock()
        cls.mock_author_repository = Mock()
        cls.mock_book_category_repository = Mock()
        cls.mock_branch_repository = Mock()
        cls.mock_physical_exemplar_repository = Mock()

        # Mock the producer dependencies
        cls.mock_book_producer = Mock()
        cls.mock_author_producer = Mock()
        cls.mock_book_category_producer = Mock()
        cls.mock_branch_producer = Mock()
        cls.mock_physical_exemplar_producer = Mock()

    def tearDown(self):
        super().tearDown()
        # Reset read repository mocks for each test
        self.mock_book_read_repository.reset_mock()
        self.mock_author_read_repository.reset_mock()
        self.mock_book_category_read_repository.reset_mock()
        self.mock_branch_read_repository.reset_mock()
        self.mock_physical_exemplar_read_repository.reset_mock()

        # Reset write repository mocks for each test
        self.mock_book_write_repository.reset_mock()
        self.mock_author_write_repository.reset_mock()
        self.mock_book_category_write_repository.reset_mock()
        self.mock_branch_write_repository.reset_mock()
        self.mock_physical_exemplar_write_repository.reset_mock()

        # Reset original mocks for backward compatibility
        self.mock_book_repository.reset_mock()
        self.mock_author_repository.reset_mock()
        self.mock_book_category_repository.reset_mock()
        self.mock_branch_repository.reset_mock()
        self.mock_physical_exemplar_repository.reset_mock()

        # Reset producer mocks
        self.mock_book_producer.reset_mock()
        self.mock_author_producer.reset_mock()
        self.mock_book_category_producer.reset_mock()
        self.mock_branch_producer.reset_mock()
        self.mock_physical_exemplar_producer.reset_mock()
