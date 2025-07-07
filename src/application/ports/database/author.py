from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID

from src.domain.entities.author import Author, AuthorFilter
from src.infrastructure.adapters.database.db.session import DatabaseSettings


class AuthorRepositoryPort(ABC):
    def __init__(self, db: DatabaseSettings) -> None:
        self.db = db

    @abstractmethod
    def upsert_author(self, author: Author) -> Author:
        pass

    @abstractmethod
    def get_author_by_id(self, id: UUID) -> Author:
        pass

    @abstractmethod
    def get_author_by_filter(
        self,
        filter: Optional[AuthorFilter] = None,
    ) -> List[Author]:
        pass

    @abstractmethod
    def get_authors_by_ids(self, ids: List[UUID]) -> List[Author]:
        pass

    @abstractmethod
    def delete_author(self, id: str) -> None:
        pass
