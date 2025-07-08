from src.application.ports.database.author import AuthorRepositoryPort
from src.domain.entities.base import DeletionEntity


class DeleteAuthor:
    def __init__(self, author_repository: AuthorRepositoryPort):
        self.author_repository = author_repository

    def execute(self, deletion_entity: DeletionEntity) -> None:
        self.author_repository.delete_author(deletion_entity.id)
