from typing import List
from uuid import UUID

from sqlalchemy import func
from sqlmodel import select

from src.application.ports.database.physical_exemplar import (
    PhysicalExemplarRepositoryPort,
)
from src.domain.entities.book import BookFilter
from src.domain.entities.physical_exemplar import PhysicalExemplar
from src.infrastructure.adapters.database.db.session import DatabaseSettings
from src.infrastructure.adapters.database.models.author import Author as AuthorModel
from src.infrastructure.adapters.database.models.author_book_link import (
    AuthorBookLink as AuthorBookLinkModel,
)
from src.infrastructure.adapters.database.models.book import Book as BookModel
from src.infrastructure.adapters.database.models.book_book_category_link import (
    BookBookCategoryLink as BookCategoryBookLinkModel,
)
from src.infrastructure.adapters.database.models.book_category import (
    BookCategory as BookCategoryModel,
)
from src.infrastructure.adapters.database.models.physical_exemplar import (
    PhysicalExemplar as PhysicalExemplarModel,
)


class PhysicalExemplarRepository(PhysicalExemplarRepositoryPort):
    def __init__(self, db: DatabaseSettings) -> None:
        self.db = db

    def upsert_physical_exemplar(
        self,
        physical_exemplar: PhysicalExemplar,
    ) -> PhysicalExemplar:
        with self.db.get_session() as session:
            # First try to find by book_id and branch_id for idempotency
            existing = session.exec(
                select(PhysicalExemplarModel).where(
                    PhysicalExemplarModel.book_id == physical_exemplar.book_id,
                    PhysicalExemplarModel.branch_id == physical_exemplar.branch_id,
                ),
            ).first()

            if existing:
                # Update existing record
                for k, v in physical_exemplar.model_dump().items():
                    if k not in [
                        "id",
                        "created_at",
                        "created_by",
                    ]:  # Preserve creation metadata
                        setattr(existing, k, v)
                physical_exemplar_model = existing
            else:
                # Create new record
                physical_exemplar_model = PhysicalExemplarModel.model_validate(
                    physical_exemplar,
                )
                session.add(physical_exemplar_model)

            session.flush()
            session.commit()
            session.refresh(physical_exemplar_model)
            return PhysicalExemplar.model_validate(physical_exemplar_model)

    def filter_by_branch_and_book_filter(
        self,
        branch_id: UUID,
        book_filter: BookFilter,
    ) -> List[PhysicalExemplar]:
        with self.db.get_session(slave=True) as session:
            # Start with physical exemplars in the specified branch
            statement = select(PhysicalExemplarModel).where(
                PhysicalExemplarModel.branch_id == branch_id,
            )

            # Join with book table to apply book filters
            statement = statement.join(BookModel)

            # Apply basic book filters
            if book_filter.isbn_code:
                statement = statement.where(
                    BookModel.isbn_code == book_filter.isbn_code,
                )
            if book_filter.editor:
                statement = statement.where(BookModel.editor == book_filter.editor)
            if book_filter.edition:
                statement = statement.where(BookModel.edition == book_filter.edition)
            if book_filter.type:
                statement = statement.where(BookModel.type == book_filter.type)
            if book_filter.publish_date:
                statement = statement.where(
                    BookModel.publish_date == book_filter.publish_date,
                )

            # For author name filter, join through the many-to-many relationship
            if book_filter.author_name:
                statement = (
                    statement.join(AuthorBookLinkModel)
                    .join(AuthorModel)
                    .where(
                        AuthorModel.name.ilike(f"%{book_filter.author_name}%"),  # type: ignore
                    )
                )

            # For book category filter, join through the many-to-many relationship
            if book_filter.book_category_name:
                statement = (
                    statement.join(BookCategoryBookLinkModel)
                    .join(BookCategoryModel)
                    .where(
                        func.similarity(
                            BookCategoryModel.title,
                            book_filter.book_category_name,
                        )
                        > 0.2,
                    )
                )

            physical_exemplars = session.exec(statement).all()
            return [
                PhysicalExemplar.model_validate(exemplar)
                for exemplar in physical_exemplars
            ]
