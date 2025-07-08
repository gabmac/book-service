from uuid import UUID

from sqlalchemy.exc import NoResultFound
from sqlmodel import select

from src.application.exceptions import NotFoundException
from src.application.ports.database.book_category import BookCategoryRepositoryPort
from src.domain.entities.book_category import BookCategory
from src.infrastructure.adapters.database.db.session import DatabaseSettings


class BookCategoryRepository(BookCategoryRepositoryPort):
    def __init__(self, db: DatabaseSettings) -> None:
        self.db = db

    def upsert_book_category(self, book_category: BookCategory) -> BookCategory:
        book_category_model = BookCategory.model_validate(book_category)
        with self.db.get_session() as session:
            session.add(book_category_model)
            session.commit()
            session.refresh(book_category_model)
            return BookCategory.model_validate(book_category_model)

    def delete_book_category(self, id: UUID) -> None:
        with self.db.get_session() as session:
            session.delete(id)
            session.commit()

    def get_book_category_by_id(self, id: UUID) -> BookCategory:
        with self.db.get_session(slave=True) as session:
            try:
                book_category_model = session.exec(
                    select(BookCategory).where(BookCategory.id == id),
                ).one()
            except NoResultFound:
                raise NotFoundException("Book category not found")
            return BookCategory.model_validate(book_category_model)

    def get_book_category_by_title(self, title: str) -> BookCategory:
        with self.db.get_session(slave=True) as session:
            try:
                book_category_model = session.exec(
                    select(BookCategory).where(BookCategory.title == title),
                ).one()
            except NoResultFound:
                raise NotFoundException("Book category not found")
            return BookCategory.model_validate(book_category_model)
