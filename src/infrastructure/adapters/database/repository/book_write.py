from typing import Any, Dict

from sqlalchemy.exc import NoResultFound
from sqlmodel import delete, select

from src.application.ports.database.book import BookWriteRepositoryPort
from src.domain.entities.book import Book
from src.infrastructure.adapters.database.db.session import DatabaseSettings
from src.infrastructure.adapters.database.elasticsearch.client import (
    ElasticsearchClient,
)
from src.infrastructure.adapters.database.models.author_book_link import (
    AuthorBookLink as AuthorBookLinkModel,
)
from src.infrastructure.adapters.database.models.book import Book as BookModel
from src.infrastructure.adapters.database.models.book_book_category_link import (
    BookBookCategoryLink as BookCategoryBookLinkModel,
)
from src.infrastructure.adapters.database.models.book_data import (
    BookData as BookDataModel,
)
from src.infrastructure.settings.config import ElasticsearchIndexConfig


class BookWriteRepository(BookWriteRepositoryPort):
    def __init__(self, db: DatabaseSettings, elasticsearch_client: ElasticsearchClient):
        super().__init__(db=db)
        self.es_client = elasticsearch_client
        self.es_config = ElasticsearchIndexConfig()
        self.es_index = self.es_config.books_index

    def _book_to_elasticsearch_document(self, book: Book) -> Dict[str, Any]:
        """Convert Book entity to Elasticsearch document"""
        doc = {
            "id": str(book.id),
            "isbn_code": book.isbn_code,
            "editor": book.editor,
            "edition": book.edition,
            "type": book.type,
            "publish_date": (
                book.publish_date.isoformat() if book.publish_date else None
            ),
            "created_at": book.created_at.strftime("%Y-%m-%dT%H:%M:%S")
            + f".{book.created_at.microsecond // 1000:03d}Z",
            "updated_at": book.updated_at.strftime("%Y-%m-%dT%H:%M:%S")
            + f".{book.updated_at.microsecond // 1000:03d}Z",
            "created_by": book.created_by,
            "updated_by": book.updated_by,
            "author_ids": (
                [str(author_id) for author_id in book.author_ids]
                if book.author_ids
                else []
            ),
            "category_ids": (
                [str(cat_id) for cat_id in book.category_ids]
                if book.category_ids
                else []
            ),
        }

        # Add nested objects for search
        if book.authors:
            doc["authors"] = [
                {
                    "id": str(author.id),
                    "name": author.name,
                }
                for author in book.authors
            ]

        if book.book_categories:
            doc["book_categories"] = [
                {
                    "id": str(category.id),
                    "title": category.title,
                    "description": category.description,
                }
                for category in book.book_categories
            ]

        if book.book_data:
            doc["book_data"] = [
                {
                    "id": str(data.id),
                    "title": data.title,
                    "summary": data.summary,
                    "language": data.language,
                }
                for data in book.book_data
            ]

        return doc

    def upsert_book(self, book: Book) -> Book:
        # Save to PostgreSQL first (source of truth)
        book_entity = self._upsert_book_postgresql(book)

        # Index in Elasticsearch
        self._upsert_book_elasticsearch(book_entity)

        return book_entity

    def _upsert_book_postgresql(self, book: Book) -> Book:
        """Upsert book in PostgreSQL database"""
        author_link_models = [
            AuthorBookLinkModel(
                author_id=author.id,
                book_id=book.id,
                created_by=book.created_by,
                created_at=book.created_at,
                updated_by=book.updated_by,
                updated_at=book.updated_at,
            )
            for author in book.authors  # type: ignore
        ]
        book_category_link_models = [
            BookCategoryBookLinkModel(
                book_category_id=book_category.id,
                book_id=book.id,
                created_by=book.created_by,
                created_at=book.created_at,
                updated_by=book.updated_by,
                updated_at=book.updated_at,
            )
            for book_category in book.book_categories  # type: ignore
        ]
        book_data_models = [
            BookDataModel(
                id=book_data.id,
                summary=book_data.summary,
                title=book_data.title,
                language=book_data.language,
                book_id=book.id,
                created_by=book.created_by,
                created_at=book.created_at,
                updated_by=book.updated_by,
                updated_at=book.updated_at,
            )
            for book_data in book.book_data  # type: ignore
        ]

        with self.db.get_session() as session:
            existing_book = session.get(BookModel, book.id)
            if existing_book:
                # Update fields
                for key, value in book.model_dump(
                    exclude={
                        "authors",
                        "book_categories",
                        "book_data",
                        "physical_exemplars",
                        "author_ids",
                        "category_ids",
                        "created_at",
                        "created_by",
                    },
                ).items():
                    setattr(existing_book, key, value)
            else:
                existing_book = BookModel(
                    id=book.id,
                    isbn_code=book.isbn_code,
                    editor=book.editor,
                    edition=book.edition,
                    type=book.type,
                    publish_date=book.publish_date,
                    created_by=book.created_by,
                    created_at=book.created_at,
                    updated_by=book.updated_by,
                    updated_at=book.updated_at,
                )
            session.add(existing_book)
            session.flush()

            session.exec(delete(AuthorBookLinkModel).where(AuthorBookLinkModel.book_id == book.id))  # type: ignore
            session.exec(delete(BookDataModel).where(BookDataModel.book_id == book.id))  # type: ignore
            session.exec(delete(BookCategoryBookLinkModel).where(BookCategoryBookLinkModel.book_id == book.id))  # type: ignore
            session.flush()
            session.add_all(author_link_models)
            session.add_all(book_category_link_models)
            session.add_all(book_data_models)
            session.commit()
            session.refresh(existing_book)

            return Book.model_validate(existing_book)

    def _upsert_book_elasticsearch(self, book: Book) -> None:
        """Index book in Elasticsearch"""
        es_document = self._book_to_elasticsearch_document(book)

        self.es_client.client.index(  # type: ignore
            index=self.es_index,
            id=str(book.id),
            body=es_document,
            refresh="wait_for",
        )

    def delete_book(self, id: str) -> None:
        # Delete from PostgreSQL first (source of truth)
        try:
            self._delete_book_postgresql(id)

            # Delete from Elasticsearch
            self._delete_book_elasticsearch(id)
        except NoResultFound:
            pass

    def _delete_book_postgresql(self, id: str) -> None:
        """Delete book from PostgreSQL database"""
        with self.db.get_session() as session:
            statement = select(BookModel).where(BookModel.id == id)
            book = session.exec(statement).one()  # type: ignore
            session.delete(book)
            session.commit()

    def _delete_book_elasticsearch(self, id: str) -> None:
        """Delete book from Elasticsearch"""
        self.es_client.client.delete(  # type: ignore
            index=self.es_index,
            id=id,
        )
