from sqlalchemy.exc import NoResultFound
from sqlmodel import select

from src.application.ports.database.author import AuthorWriteRepositoryPort
from src.domain.entities.author import Author
from src.infrastructure.adapters.database.db.session import DatabaseSettings
from src.infrastructure.adapters.database.models.author import Author as AuthorModel


class AuthorWriteRepository(AuthorWriteRepositoryPort):
    def __init__(self, db: DatabaseSettings):
        super().__init__(db=db)

    def upsert_author(self, author: Author) -> Author:
        with self.db.get_session() as session:
            # First try to find by ID for idempotency
            existing = session.exec(
                select(AuthorModel).where(AuthorModel.id == author.id),
            ).first()

            if existing:
                # Update existing record
                for k, v in author.model_dump().items():
                    if k not in [
                        "id",
                        "created_at",
                        "created_by",
                    ]:
                        setattr(existing, k, v)
            else:
                existing = AuthorModel.model_validate(author)
                session.add(existing)
            session.commit()
            session.flush()
            session.refresh(existing)
            return Author.model_validate(existing)

    def delete_author(self, id: str) -> None:
        with self.db.get_session() as session:
            statement = select(AuthorModel).where(AuthorModel.id == id)
            try:
                author = session.exec(statement).one()  # type: ignore
            except NoResultFound:
                pass
            else:
                session.delete(author)
                session.commit()
