from src.application.dto.producer import Message
from src.application.ports.database.author import AuthorRepositoryPort


class DeleteAuthor:
    def __init__(self, author_repository: AuthorRepositoryPort):
        self.author_repository = author_repository

    def execute(self, message: Message) -> None:
        self.author_repository.delete_author(message.message)
