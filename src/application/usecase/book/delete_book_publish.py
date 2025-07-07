from uuid import UUID

from src.application.ports.producer.book_producer import BookProducerPort


class DeleteBookPublish:
    def __init__(self, book_producer: BookProducerPort):
        self.book_producer = book_producer

    def execute(self, id: UUID) -> None:
        self.book_producer.delete_book(id)
