from typing import List, Optional
from uuid import UUID

from sqlalchemy.exc import NoResultFound
from sqlmodel import and_, select

from src.application.exceptions import NotFoundException
from src.application.ports.database.book import BookRepositoryPort
from src.domain.entities.book import Book, BookFilter
from src.infrastructure.adapters.database.db.session import DatabaseSettings
from src.infrastructure.adapters.database.models.author import Author as AuthorModel
from src.infrastructure.adapters.database.models.author_book_link import (
    AuthorBookLink as AuthorBookLinkModel,
)
from src.infrastructure.adapters.database.models.book import Book as BookModel


class BookRepository(BookRepositoryPort):
    def __init__(self, db: DatabaseSettings):
        super().__init__(db=db)

    def upsert_book(self, book: Book) -> Book:
        book_model = BookModel(
            id=book.id,
            isbn_code=book.isbn_code,
            editor=book.editor,
            edition=book.edition,
            type=book.type,
            publish_date=book.publish_date,
            created_by=book.created_by,
            created_at=book.created_at,
            updated_by=book.updated_by,
            updated_at=book.updated_at,
        )

        link_models = [
            AuthorBookLinkModel(
                author_id=author.id,
                book_id=book.id,
                created_by=book.created_by,
                created_at=book.created_at,
                updated_by=book.updated_by,
                updated_at=book.updated_at,
            )
            for author in book.authors  # type: ignore
        ]
        with self.db.get_session() as session:
            statement = select(AuthorBookLinkModel).filter(
                AuthorBookLinkModel.book_id == book.id,  # type: ignore
            )
            book_statement = select(BookModel).where(BookModel.id == book.id)
            authors_relations = session.exec(statement).all()
            try:
                book = session.exec(book_statement).one()  # type: ignore
                session.delete(book)
            except NoResultFound:
                pass
            for author_relation in authors_relations:
                session.delete(author_relation)
            session.add(book_model)
            session.flush()
            session.add_all(link_models)
            session.commit()
            session.refresh(book_model)
            return Book.model_validate(book_model)

    def get_book_by_id(self, id: UUID) -> Book:
        with self.db.get_session(slave=True) as session:
            try:
                book_model = session.exec(
                    select(BookModel).where(BookModel.id == id),
                ).one()
            except NoResultFound:
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
                if filter.author_name:
                    wheres_clause.append(
                        and_(
                            BookModel.authors.any(  # type: ignore
                                AuthorModel.name.ilike(f"%{filter.author_name}%"),  # type: ignore
                            ),
                        ),
                    )
            statement = statement.where(*wheres_clause)
            books = session.exec(statement).all()
            return [Book.model_validate(book) for book in books]

    def delete_book(self, id: str) -> None:
        with self.db.get_session() as session:
            statement = select(BookModel).where(BookModel.id == id)
            try:
                book = session.exec(statement).one()  # type: ignore
            except NoResultFound:
                pass
            else:
                session.delete(book)
                session.commit()
