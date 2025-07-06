from src.application.ports.producer.author_producer import AuthorProducerPort
from src.domain.entities.author import Author


class CreateAuthorProduce:
    def __init__(self, producer: AuthorProducerPort):
        self.producer = producer

    async def execute(self, payload: Author) -> Author:
        author = Author(
            name=payload.name,
            created_by=payload.created_by,
            updated_by=payload.updated_by,
        )
        self.producer.upsert_author(author)
        return author
