from typing import List, Optional
from uuid import UUID

from sqlalchemy import func
from sqlalchemy.exc import NoResultFound
from sqlmodel import select

from src.application.exceptions import NotFoundException
from src.application.ports.database.author import AuthorReadRepositoryPort
from src.domain.entities.author import Author, AuthorFilter
from src.infrastructure.adapters.database.db.session import DatabaseSettings
from src.infrastructure.adapters.database.models.author import Author as AuthorModel


class AuthorReadRepository(AuthorReadRepositoryPort):
    def __init__(self, db: DatabaseSettings):
        super().__init__(db=db)

    def get_author_by_id(self, id: UUID) -> Author:
        with self.db.get_session(slave=True) as session:
            try:
                author_model = session.exec(
                    select(AuthorModel).where(AuthorModel.id == id),
                ).one()
            except NoResultFound:
                raise NotFoundException("Author not found")
            return Author.model_validate(author_model)

    def get_author_by_filter(
        self,
        filter: Optional[AuthorFilter] = None,
    ) -> List[Author]:
        with self.db.get_session(slave=True) as session:
            statement = select(AuthorModel)
            if filter is not None:
                if filter.name:
                    statement = statement.where(
                        func.similarity(AuthorModel.name, filter.name) > 0.2,
                    )
            authors = session.exec(statement).all()
            return [Author.model_validate(author) for author in authors]

    def get_authors_by_ids(self, ids: List[UUID]) -> List[Author]:
        with self.db.get_session(slave=True) as session:
            statement = select(AuthorModel).where(AuthorModel.id.in_(ids))  # type: ignore
            authors = session.exec(statement).all()
            return [Author.model_validate(author) for author in authors]
