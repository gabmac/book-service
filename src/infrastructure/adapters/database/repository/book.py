from src.application.ports.database.book import BookRepositoryPort
from src.domain.entities.book import Book
from src.infrastructure.adapters.database.db.session import DatabaseSettings
from src.infrastructure.adapters.database.models.book import Book as BookModel


class BookRepository(BookRepositoryPort):
    def __init__(self, db: DatabaseSettings):
        super().__init__(db=db)

    def upsert_book(self, book: Book) -> None:
        book_model = BookModel.model_validate(book)
        with self.db.get_session() as session:
            session.add(book_model)
