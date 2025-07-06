from typing import List, Optional
from uuid import UUID

from sqlmodel import and_, select

from src.application.dto.book_dto import BookFilter
from src.application.exceptions import NotFoundException
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

    def get_book_by_id(self, id: UUID) -> Book:
        with self.db.get_session(slave=True) as session:
            book_model = session.get(BookModel, id)
            if book_model is None:
                raise NotFoundException("Book not found")
            return Book.model_validate(book_model)

    def get_book_by_filter(self, filter: Optional[BookFilter] = None) -> List[Book]:
        with self.db.get_session(slave=True) as session:
            wheres_clause = []
            statement = select(BookModel)
            if filter:
                if filter.isbn_code:
                    wheres_clause.append(BookModel.isbn_code == filter.isbn_code)
                if filter.editor:
                    wheres_clause.append(BookModel.editor == filter.editor)
                if filter.edition:
                    wheres_clause.append(BookModel.edition == filter.edition)
                if filter.type:
                    wheres_clause.append(BookModel.type == filter.type)
                if filter.publish_date:
                    wheres_clause.append(
                        and_(  # type: ignore
                            BookModel.publish_date <= filter.publish_date,
                            BookModel.publish_date >= filter.publish_date,
                        ),
                    )
            statement = statement.where(*wheres_clause)
            books = session.exec(statement).all()
            return [Book.model_validate(book) for book in books]
