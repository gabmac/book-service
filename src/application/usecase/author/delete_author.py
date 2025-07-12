from uuid import UUID

from src.application.ports.database.author import AuthorRepositoryPort
from src.application.ports.producer.author_producer import AuthorProducerPort
from src.domain.entities.base import DeletionEntity


class DeleteAuthor:
    def __init__(
        self,
        author_repository: AuthorRepositoryPort,
        author_producer: AuthorProducerPort,
    ):
        self.author_repository = author_repository
        self.author_producer = author_producer

    def execute(self, deletion_entity: DeletionEntity) -> None:
        self.author_producer.notify_external_author_deletion(UUID(deletion_entity.id))
        self.author_repository.delete_author(deletion_entity.id)
