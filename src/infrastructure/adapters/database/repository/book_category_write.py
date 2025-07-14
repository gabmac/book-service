from uuid import UUID

from sqlmodel import and_, select, update

from src.application.exceptions import OptimisticLockException
from src.application.ports.database.book_category import BookCategoryWriteRepositoryPort
from src.domain.entities.book_category import BookCategory
from src.infrastructure.adapters.database.db.session import DatabaseSettings
from src.infrastructure.adapters.database.models.book_category import (
    BookCategory as BookCategoryModel,
)


class BookCategoryWriteRepository(BookCategoryWriteRepositoryPort):
    def __init__(self, db: DatabaseSettings) -> None:
        self.db = db

    def upsert_book_category(self, book_category: BookCategory) -> BookCategory:
        with self.db.get_session() as session:
            book_category_model = session.get(BookCategoryModel, book_category.id)
            if book_category_model:
                statement = (
                    update(BookCategoryModel)
                    .where(
                        and_(
                            BookCategoryModel.id == book_category.id,
                            BookCategoryModel.version == book_category.version - 1,
                        ),
                    )
                    .values(
                        **book_category.model_dump(
                            exclude_none=True,
                            exclude_unset=True,
                            mode="json",
                        )
                    )
                )
                result = session.exec(statement)  # type: ignore
                if result.rowcount == 0:
                    raise OptimisticLockException(
                        f"""Optimistic lock failed for book category {book_category.id}.
                        Expected version {book_category.version - 1},
                        but data may have been modified by another transaction.""",
                    )
            else:
                book_category_model = BookCategoryModel.model_validate(book_category)
                session.add(book_category_model)
            session.flush()
            session.commit()
            session.refresh(book_category_model)
            return BookCategory.model_validate(book_category_model)

    def delete_book_category(self, id: UUID) -> None:
        with self.db.get_session() as session:
            statement = select(BookCategoryModel).where(BookCategoryModel.id == id)
            result = session.exec(statement).one_or_none()
            if result:
                session.delete(result)
                session.commit()
