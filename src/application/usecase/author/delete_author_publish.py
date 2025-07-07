from uuid import UUID

from src.application.ports.producer.author_producer import AuthorProducerPort


class DeleteAuthorPublish:
    def __init__(self, author_producer: AuthorProducerPort):
        self.author_producer = author_producer

    def execute(self, id: UUID) -> None:
        self.author_producer.delete_author(id)
