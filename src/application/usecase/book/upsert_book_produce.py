from typing import List
from uuid import UUID

from src.application.exceptions import NotFoundException
from src.application.ports.database.author import AuthorReadRepositoryPort
from src.application.ports.database.book_category import BookCategoryReadRepositoryPort
from src.application.ports.producer.book_producer import BookProducerPort
from src.domain.entities.author import Author
from src.domain.entities.book import Book
from src.domain.entities.book_category import BookCategory


class UpsertBookProduce:
    def __init__(
        self,
        producer: BookProducerPort,
        author_repository: AuthorReadRepositoryPort,
        book_category_repository: BookCategoryReadRepositoryPort,
    ):
        self.producer = producer
        self.author_repository = author_repository
        self.book_category_repository = book_category_repository

    async def execute(self, payload: Book) -> Book:
        authors = self._validate_authors_exist(payload.author_ids)  # type: ignore
        book_categories = self._validate_book_categories_exist(payload.category_ids)  # type: ignore
        payload.author_ids = None
        payload.category_ids = None
        payload.authors = authors
        payload.book_categories = book_categories
        self.producer.upsert_book(payload)

        return payload

    def _validate_authors_exist(self, author_ids: List[UUID]) -> List[Author]:
        authors = self.author_repository.get_authors_by_ids(author_ids)
        if len(authors) != len(author_ids):
            raise NotFoundException("Some authors not found")
        return authors

    def _validate_book_categories_exist(
        self,
        book_category_ids: List[UUID],
    ) -> List[BookCategory]:
        book_categories = self.book_category_repository.get_book_categories_by_ids(
            book_category_ids,
        )
        if len(book_categories) != len(book_category_ids):
            raise NotFoundException("Some book categories not found")
        return book_categories
