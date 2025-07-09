from unittest import IsolatedAsyncioTestCase
from unittest.mock import patch

from polyfactory.factories.pydantic_factory import ModelFactory

from src.domain.entities.author import Author
from src.domain.entities.book import Book
from src.domain.entities.book_category import BookCategory
from src.domain.entities.branch import Branch
from src.infrastructure.adapters.database.db.session import DatabaseSettings
from src.infrastructure.adapters.database.repository.author import AuthorRepository
from src.infrastructure.adapters.database.repository.book import BookRepository
from src.infrastructure.adapters.database.repository.book_category import (
    BookCategoryRepository,
)
from src.infrastructure.adapters.database.repository.branch import BranchRepository


class BookModelFactory(ModelFactory):
    __model__ = Book


class AuthorModelFactory(ModelFactory):
    __model__ = Author


class BranchModelFactory(ModelFactory):
    __model__ = Branch


class BookCategoryModelFactory(ModelFactory):
    __model__ = BookCategory


class BaseConfTest(IsolatedAsyncioTestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.addClassCleanup(patch.stopall)
        cls.book_model_factory = BookModelFactory
        cls.author_model_factory = AuthorModelFactory
        cls.branch_model_factory = BranchModelFactory
        cls.book_category_model_factory = BookCategoryModelFactory

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
        cls.book_repository = BookRepository(db=cls.db)
        cls.author_repository = AuthorRepository(db=cls.db)
        cls.branch_repository = BranchRepository(db=cls.db)
        cls.book_category_repository = BookCategoryRepository(db=cls.db)


class BaseUseCaseConfTest(BaseConfTest):
    pass
