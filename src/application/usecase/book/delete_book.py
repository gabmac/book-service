from uuid import UUID

from src.application.ports.database.book import BookRepositoryPort
from src.application.ports.producer.book_producer import BookProducerPort
from src.domain.entities.base import DeletionEntity


class DeleteBook:
    def __init__(
        self,
        book_repository: BookRepositoryPort,
        book_producer: BookProducerPort,
    ):
        self.book_repository = book_repository
        self.book_producer = book_producer

    def execute(self, deletion_entity: DeletionEntity) -> None:
        self.book_producer.notify_external_book_deletion(UUID(deletion_entity.id))
        self.book_repository.delete_book(deletion_entity.id)
