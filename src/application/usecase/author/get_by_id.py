from uuid import UUID

from src.application.ports.database.author import AuthorRepositoryPort
from src.domain.entities.author import Author


class GetAuthorById:
    def __init__(self, author_repository: AuthorRepositoryPort):
        self.author_repository = author_repository

    def execute(self, id: UUID) -> Author:
        author = self.author_repository.get_author_by_id(id)
        return Author.model_validate(author)
