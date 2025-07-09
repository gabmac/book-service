from src.application.ports.producer.author_producer import AuthorProducerPort
from src.domain.entities.author import Author


class CreateAuthorProduce:
    def __init__(self, producer: AuthorProducerPort):
        self.producer = producer

    async def execute(self, payload: Author) -> Author:
        self.producer.upsert_author(payload)
        return payload
