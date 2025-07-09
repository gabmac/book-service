from unittest import IsolatedAsyncioTestCase
from unittest.mock import patch

from polyfactory.factories.pydantic_factory import ModelFactory

from src.domain.entities.author import Author
from src.domain.entities.book import Book
from src.infrastructure.adapters.database.db.session import DatabaseSettings
from src.infrastructure.adapters.database.models.base_model import Base
from src.infrastructure.adapters.database.repository.author import AuthorRepository
from src.infrastructure.adapters.database.repository.book import BookRepository


class BookModelFactory(ModelFactory):
    __model__ = Book


class AuthorModelFactory(ModelFactory):
    __model__ = Author


class BaseConfTest(IsolatedAsyncioTestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.addClassCleanup(patch.stopall)
        cls.book_model_factory = BookModelFactory
        cls.author_model_factory = AuthorModelFactory

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
        Base.metadata.create_all(bind=cls.db.engine)
        cls.book_repository = BookRepository(db=cls.db)
        cls.author_repository = AuthorRepository(db=cls.db)


class BaseUseCaseConfTest(BaseConfTest):
    pass
