from src.application.dto.producer import Message
from src.application.ports.database.book import BookRepositoryPort


class DeleteBook:
    def __init__(self, book_repository: BookRepositoryPort):
        self.book_repository = book_repository

    def execute(self, message: Message) -> None:
        self.book_repository.delete_book(message.message)
