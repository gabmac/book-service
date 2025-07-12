from typing import List, Optional

from src.application.ports.database.author import AuthorReadRepositoryPort
from src.domain.entities.author import Author, AuthorFilter


class FilterAuthor:
    def __init__(self, author_repository: AuthorReadRepositoryPort):
        self.author_repository = author_repository

    def execute(self, filter: Optional[AuthorFilter] = None) -> List[Author]:
        authors = self.author_repository.get_author_by_filter(filter)
        return [Author.model_validate(author) for author in authors]
