from src.application.exceptions import OptimisticLockException
from src.application.ports.database.author import (
    AuthorWriteRepositoryPort,
)
from src.application.ports.producer.author_producer import AuthorProducerPort
from src.domain.entities.author import Author


class UpsertAuthor:
    def __init__(
        self,
        author_write_repository: AuthorWriteRepositoryPort,
        author_producer: AuthorProducerPort,
    ):
        self.author_write_repository = author_write_repository
        self.author_producer = author_producer

    def execute(self, author: Author) -> Author | None:

        self.author_producer.notify_external_author_upsert(author)
        try:
            author = self.author_write_repository.upsert_author(author)
        except OptimisticLockException:
            return None

        return author
