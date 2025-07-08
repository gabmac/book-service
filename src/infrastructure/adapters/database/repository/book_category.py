from typing import List
from uuid import UUID

from sqlalchemy import func
from sqlalchemy.exc import NoResultFound
from sqlmodel import select

from src.application.exceptions import NotFoundException
from src.application.ports.database.book_category import BookCategoryRepositoryPort
from src.domain.entities.book_category import BookCategory, BookCategoryFilter
from src.infrastructure.adapters.database.db.session import DatabaseSettings
from src.infrastructure.adapters.database.models.book_category import (
    BookCategory as BookCategoryModel,
)


class BookCategoryRepository(BookCategoryRepositoryPort):
    def __init__(self, db: DatabaseSettings) -> None:
        self.db = db

    def upsert_book_category(self, book_category: BookCategory) -> BookCategory:
        with self.db.get_session() as session:
            book_category_model = session.get(BookCategoryModel, book_category.id)
            if book_category_model:
                for k, v in book_category.model_dump().items():
                    if k == "id":
                        continue
                    setattr(book_category_model, k, v)
            else:
                book_category_model = BookCategoryModel.model_validate(book_category)
                session.add(book_category_model)
            session.flush()
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
                    select(BookCategoryModel).where(BookCategory.id == id),
                ).one()
            except NoResultFound:
                raise NotFoundException("Book category not found")
            return BookCategory.model_validate(book_category_model)

    def get_book_category_by_title(self, title: str) -> BookCategory:
        with self.db.get_session(slave=True) as session:
            try:
                book_category_model = session.exec(
                    select(BookCategoryModel).where(BookCategoryModel.title == title),
                ).one()
            except NoResultFound:
                raise NotFoundException("Book category not found")
            return BookCategory.model_validate(book_category_model)

    def get_book_category_by_filter(
        self,
        filter: BookCategoryFilter,
    ) -> List[BookCategory]:
        with self.db.get_session(slave=True) as session:
            statement = select(BookCategoryModel)
            if filter.title:
                statement = statement.where(
                    func.similarity(BookCategoryModel.title, filter.title) > 0.2,
                )
            if filter.description:
                statement = statement.where(
                    BookCategoryModel.description == filter.description,
                )
            return [
                BookCategory.model_validate(book_category_model)
                for book_category_model in session.exec(statement).all()
            ]

    def get_book_categories_by_ids(self, ids: List[UUID]) -> List[BookCategory]:
        with self.db.get_session(slave=True) as session:
            return [
                BookCategory.model_validate(book_category_model)
                for book_category_model in session.exec(
                    select(BookCategoryModel).where(BookCategoryModel.id.in_(ids)),  # type: ignore
                ).all()
            ]
