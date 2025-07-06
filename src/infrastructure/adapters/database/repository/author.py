from typing import List, Optional
from uuid import UUID

from sqlmodel import select

from src.application.exceptions import NotFoundException
from src.application.ports.database.author import AuthorRepositoryPort
from src.domain.entities.author import Author, AuthorFilter
from src.infrastructure.adapters.database.db.session import DatabaseSettings
from src.infrastructure.adapters.database.models.author import Author as AuthorModel


class AuthorRepository(AuthorRepositoryPort):
    def __init__(self, db: DatabaseSettings):
        super().__init__(db=db)

    def upsert_author(self, author: Author) -> Author:
        author_model = AuthorModel.model_validate(author)
        with self.db.get_session() as session:
            session.add(author_model)
            session.commit()

        return Author.model_validate(author_model)

    def get_author_by_id(self, id: UUID) -> Author:
        with self.db.get_session(slave=True) as session:
            author_model = session.get(AuthorModel, id)
            if author_model is None:
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
                        AuthorModel.name.ilike(f"%{filter.name}%"),  # type: ignore
                    )
            authors = session.exec(statement).all()
            return [Author.model_validate(author) for author in authors]
