from unittest import IsolatedAsyncioTestCase
from unittest.mock import Mock, patch

from polyfactory.factories.pydantic_factory import ModelFactory
from sqlmodel import text

from src.application.dto.author import AuthorUpsert
from src.application.dto.book_category import BookCategoryUpsert
from src.application.dto.branch import BranchUpsert
from src.domain.entities.author import Author
from src.domain.entities.book import Book, BookFilter
from src.domain.entities.book_category import BookCategory
from src.domain.entities.book_data import BookData
from src.domain.entities.branch import Branch
from src.domain.entities.physical_exemplar import PhysicalExemplar
from src.infrastructure.adapters.database.db.session import DatabaseSettings
from src.infrastructure.adapters.database.repository.author import AuthorRepository
from src.infrastructure.adapters.database.repository.book import BookRepository
from src.infrastructure.adapters.database.repository.book_category import (
    BookCategoryRepository,
)
from src.infrastructure.adapters.database.repository.branch import BranchRepository
from src.infrastructure.adapters.database.repository.physical_exemplar import (
    PhysicalExemplarRepository,
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
    __model__ = BookFilter


class AuthorUpsertModelFactory(ModelFactory):
    __model__ = AuthorUpsert


class BookCategoryUpsertModelFactory(ModelFactory):
    __model__ = BookCategoryUpsert


class BranchUpsertModelFactory(ModelFactory):
    __model__ = BranchUpsert


class BaseConfTest(IsolatedAsyncioTestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.maxDiff = None
        cls.addClassCleanup(patch.stopall)
        cls.book_model_factory = BookModelFactory
        cls.book_filter_model_factory = BookFilterModelFactory
        cls.author_model_factory = AuthorModelFactory
        cls.author_upsert_model_factory = AuthorUpsertModelFactory
        cls.branch_model_factory = BranchModelFactory
        cls.book_category_model_factory = BookCategoryModelFactory
        cls.book_category_upsert_model_factory = BookCategoryUpsertModelFactory
        cls.book_data_model_factory = BookDataModelFactory
        cls.physical_exemplar_model_factory = PhysicalExemplarModelFactory
        cls.branch_upsert_model_factory = BranchUpsertModelFactory

        super().setUpClass()


class BaseRepositoryConfTest(BaseConfTest):
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
        cls.book_repository = BookRepository(db=cls.db)  # type: ignore
        cls.author_repository = AuthorRepository(db=cls.db)  # type: ignore
        cls.branch_repository = BranchRepository(db=cls.db)  # type: ignore
        cls.book_category_repository = BookCategoryRepository(db=cls.db)  # type: ignore
        cls.physical_exemplar_repository = PhysicalExemplarRepository(db=cls.db)  # type: ignore

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


class BaseUseCaseConfTest(BaseConfTest):
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        # Mock the repository dependencies
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
        # Reset mocks for each test
        self.mock_book_repository.reset_mock()
        self.mock_author_repository.reset_mock()
        self.mock_book_category_repository.reset_mock()
        self.mock_branch_repository.reset_mock()
        self.mock_physical_exemplar_repository.reset_mock()
        self.mock_book_producer.reset_mock()
        self.mock_author_producer.reset_mock()
        self.mock_book_category_producer.reset_mock()
        self.mock_branch_producer.reset_mock()
        self.mock_physical_exemplar_producer.reset_mock()
