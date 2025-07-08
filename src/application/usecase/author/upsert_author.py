from src.application.exceptions import NotFoundException
from src.application.ports.database.author import AuthorRepositoryPort
from src.domain.entities.author import Author


class UpsertAuthor:
    def __init__(self, author_repository: AuthorRepositoryPort):
        self.author_repository = author_repository

    def execute(self, author: Author) -> Author:
        try:
            old_author = self.author_repository.get_author_by_id(author.id)
            author.created_at = old_author.created_at
            author.created_by = old_author.created_by
        except NotFoundException:
            pass
        finally:
            author = self.author_repository.upsert_author(author)

        return author
