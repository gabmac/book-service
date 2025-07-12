from src.application.exceptions import NotFoundException
from src.application.ports.database.author import AuthorRepositoryPort
from src.application.ports.producer.author_producer import AuthorProducerPort
from src.domain.entities.author import Author


class UpsertAuthor:
    def __init__(
        self,
        author_repository: AuthorRepositoryPort,
        author_producer: AuthorProducerPort,
    ):
        self.author_repository = author_repository
        self.author_producer = author_producer

    def execute(self, author: Author) -> Author:
        try:
            old_author = self.author_repository.get_author_by_id(author.id)
            author.created_at = old_author.created_at
            author.created_by = old_author.created_by
        except NotFoundException:
            pass
        finally:
            self.author_producer.notify_external_author_upsert(author)
            author = self.author_repository.upsert_author(author)

        return author
