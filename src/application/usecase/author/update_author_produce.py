from src.application.exceptions import NotFoundException
from src.application.ports.database.author import AuthorReadRepositoryPort
from src.application.ports.producer.author_producer import AuthorProducerPort
from src.domain.entities.author import Author


class UpdateAuthorProduce:
    def __init__(
        self,
        producer: AuthorProducerPort,
        author_read_repository: AuthorReadRepositoryPort,
    ):
        self.producer = producer
        self.author_read_repository = author_read_repository

    async def execute(self, payload: Author) -> Author:
        try:
            old_author = self.author_read_repository.get_author_by_id(payload.id)
            if old_author:
                payload.created_at = old_author.created_at
                payload.created_by = old_author.created_by
        except NotFoundException:
            pass

        self.producer.upsert_author(payload)
        return payload
