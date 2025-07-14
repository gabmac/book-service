from sqlalchemy.exc import NoResultFound
from sqlmodel import and_, select, update

from src.application.exceptions import OptimisticLockException
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
                statement = (
                    update(AuthorModel)
                    .where(
                        and_(
                            AuthorModel.id == author.id,
                            AuthorModel.version == author.version - 1,
                        ),
                    )
                    .values(
                        **author.model_dump(
                            exclude_none=True,
                            exclude_unset=True,
                            mode="json",
                        )
                    )
                )
                result = session.exec(statement)  # type: ignore
                if result.rowcount == 0:
                    raise OptimisticLockException(
                        f"""Optimistic lock failed for author {author.id}.
                        Expected version {author.version - 1},
                        but data may have been modified by another transaction.""",
                    )
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
