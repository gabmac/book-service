from uuid import UUID

from src.application.ports.database.book import BookRepositoryPort
from src.domain.entities.book import Book
from src.infrastructure.adapters.database.db.session import DatabaseSettings
from src.infrastructure.adapters.database.exceptions import NotFoundException
from src.infrastructure.adapters.database.models.book import Book as BookModel


class BookRepository(BookRepositoryPort):
    def __init__(self, db: DatabaseSettings):
        super().__init__(db=db)

    def upsert_book(self, book: Book) -> None:
        book_model = BookModel.model_validate(book)
        with self.db.get_session() as session:
            session.add(book_model)

    def get_book_by_id(self, id: UUID) -> Book:
        with self.db.get_session() as session:
            book_model = session.get(BookModel, id)
            if book_model is None:
                raise NotFoundException("Book not found")
            return Book.model_validate(book_model)
