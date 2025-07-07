from typing import List
from uuid import UUID

from src.application.exceptions import NotFoundException
from src.application.ports.database.author import AuthorRepositoryPort
from src.application.ports.database.book import BookRepositoryPort
from src.application.ports.producer.book_producer import BookProducerPort
from src.domain.entities.author import Author
from src.domain.entities.book import Book


class UpdateBookProduce:
    def __init__(
        self,
        producer: BookProducerPort,
        book_repository: BookRepositoryPort,
        author_repository: AuthorRepositoryPort,
    ):
        self.producer = producer
        self.author_repository = author_repository
        self.book_repository = book_repository

    async def execute(self, payload: Book) -> Book:
        authors = self._validate_authors_exist(payload.author_ids)  # type: ignore
        book = self.book_repository.get_book_by_id(payload.id)
        book = Book(
            id=payload.id,
            isbn_code=payload.isbn_code,
            editor=payload.editor,
            edition=payload.edition,
            type=payload.type,
            publish_date=payload.publish_date,
            authors=authors,
            created_by=payload.created_by,
            updated_by=payload.updated_by,
        )
        self.producer.upsert_book(book)

        return book

    def _validate_authors_exist(self, author_ids: List[UUID]) -> List[Author]:
        authors = self.author_repository.get_authors_by_ids(author_ids)
        if len(authors) != len(author_ids):
            raise NotFoundException("Some authors not found")
        return authors
