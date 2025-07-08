from src.application.ports.producer.author_producer import AuthorProducerPort
from src.domain.entities.author import Author


class UpdateAuthorProduce:
    def __init__(self, producer: AuthorProducerPort):
        self.producer = producer

    async def execute(self, payload: Author) -> Author:
        author = Author(
            id=payload.id,
            name=payload.name,
            created_by=payload.created_by,
            updated_by=payload.updated_by,
            created_at=payload.created_at,
            updated_at=payload.updated_at,
        )
        self.producer.upsert_author(author)
        return author
