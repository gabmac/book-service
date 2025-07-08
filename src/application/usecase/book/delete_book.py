from src.application.ports.database.book import BookRepositoryPort
from src.domain.entities.base import DeletionEntity


class DeleteBook:
    def __init__(self, book_repository: BookRepositoryPort):
        self.book_repository = book_repository

    def execute(self, deletion_entity: DeletionEntity) -> None:
        self.book_repository.delete_book(deletion_entity.id)
