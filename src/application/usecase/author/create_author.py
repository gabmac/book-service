from src.application.dto.author import AuthorCreate
from src.application.ports.producer.author_producer import AuthorProducerPort
from src.domain.entities.author import Author


class CreateAuthorProduce:
    def __init__(self, producer: AuthorProducerPort):
        self.producer = producer

    async def execute(self, payload: AuthorCreate) -> None:
        author = Author(
            name=payload.name,
            created_by=payload.user,
            updated_by=payload.user,
        )
        self.producer.upsert_author(author)
