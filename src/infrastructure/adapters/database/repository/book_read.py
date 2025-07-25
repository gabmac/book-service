from datetime import datetime
from typing import Any, Dict, List, Optional
from uuid import UUID

from elasticsearch.exceptions import ConnectionError as ESConnectionError
from sqlalchemy.exc import NoResultFound
from sqlmodel import and_, func, select

from src.application.exceptions import NotFoundException
from src.application.ports.database.book import BookReadRepositoryPort
from src.domain.entities.book import Book, BookSearchFilter
from src.domain.enums.book_type import BookType
from src.infrastructure.adapters.database.db.session import DatabaseSettings
from src.infrastructure.adapters.database.elasticsearch.client import (
    ElasticsearchClient,
)
from src.infrastructure.adapters.database.models.author import Author as AuthorModel
from src.infrastructure.adapters.database.models.book import Book as BookModel
from src.infrastructure.adapters.database.models.book_category import (
    BookCategory as BookCategoryModel,
)
from src.infrastructure.settings.config import ElasticsearchIndexConfig


class BookReadRepository(BookReadRepositoryPort):
    def __init__(self, db: DatabaseSettings, elasticsearch_client: ElasticsearchClient):
        super().__init__(db=db)
        self.es_client = elasticsearch_client
        self.es_config = ElasticsearchIndexConfig()
        self.es_index = self.es_config.books_index

    def _book_to_elasticsearch_document(self, book: Book) -> Dict[str, Any]:
        """Convert Book entity to Elasticsearch document"""
        doc = {
            "id": str(book.id),
            "version": book.version,
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

        # Add nested authors
        if book.authors:
            doc["authors"] = [
                {
                    "id": str(author.id),
                    "name": author.name,
                    "created_at": author.created_at.strftime("%Y-%m-%dT%H:%M:%S")
                    + f".{author.created_at.microsecond // 1000:03d}Z",
                    "updated_at": author.updated_at.strftime("%Y-%m-%dT%H:%M:%S")
                    + f".{author.updated_at.microsecond // 1000:03d}Z",
                    "created_by": author.created_by,
                    "updated_by": author.updated_by,
                }
                for author in book.authors
            ]

        # Add nested book_data
        if book.book_data:
            doc["book_data"] = [
                {
                    "id": str(data.id),
                    "summary": data.summary,
                    "title": data.title,
                    "language": data.language,
                    "created_at": data.created_at.strftime("%Y-%m-%dT%H:%M:%S")
                    + f".{data.created_at.microsecond // 1000:03d}Z",
                    "updated_at": data.updated_at.strftime("%Y-%m-%dT%H:%M:%S")
                    + f".{data.updated_at.microsecond // 1000:03d}Z",
                    "created_by": data.created_by,
                    "updated_by": data.updated_by,
                }
                for data in book.book_data
            ]

        # Add nested book_categories
        if book.book_categories:
            doc["book_categories"] = [
                {
                    "id": str(category.id),
                    "title": category.title,
                    "description": category.description,
                    "created_at": category.created_at.strftime("%Y-%m-%dT%H:%M:%S")
                    + f".{category.created_at.microsecond // 1000:03d}Z",
                    "updated_at": category.updated_at.strftime("%Y-%m-%dT%H:%M:%S")
                    + f".{category.updated_at.microsecond // 1000:03d}Z",
                    "created_by": category.created_by,
                    "updated_by": category.updated_by,
                }
                for category in book.book_categories
            ]

        return doc

    def _elasticsearch_document_to_book(self, doc: Dict[str, Any]) -> Book:
        """Convert Elasticsearch document back to Book entity"""
        # This is a simplified conversion - in practice, you might need to fetch
        # related data from PostgreSQL for complete object reconstruction
        # Handle type conversion properly
        book_type = doc.get("type")
        if book_type:
            try:
                book_type = BookType(book_type)
            except ValueError:
                # If the type value is not valid, set to None
                book_type = None

        book_data = {
            "id": UUID(doc["id"]),
            "isbn_code": doc.get("isbn_code", ""),
            "version": doc.get("version", 1),
            "editor": doc.get("editor", ""),
            "edition": doc.get("edition", 1),
            "type": book_type,
            "publish_date": (
                datetime.fromisoformat(doc["publish_date"]).date()
                if doc.get("publish_date")
                else None
            ),
            "created_at": (
                datetime.fromisoformat(doc["created_at"])
                if doc.get("created_at")
                else None
            ),
            "updated_at": (
                datetime.fromisoformat(doc["updated_at"])
                if doc.get("updated_at")
                else None
            ),
            "created_by": doc.get("created_by", ""),
            "updated_by": doc.get("updated_by", ""),
            "authors": doc.get("authors", []),
            "book_data": doc.get("book_data", []),
            "book_categories": doc.get("book_categories", []),
        }

        return Book.model_validate(book_data)

    def _build_elasticsearch_query(self, filter: BookSearchFilter) -> Dict[str, Any]:
        """Build Elasticsearch query from BookSearchFilter"""
        query: Dict[str, Any] = {"bool": {"must": []}}

        for k, v in filter.model_dump(exclude_unset=True, exclude_none=True).items():
            if k in filter._basic_filters:
                query["bool"]["must"].append({"term": {k: v}})

        # Date range filters
        if filter.publish_date_from or filter.publish_date_to:
            date_range = {}
            if filter.publish_date_from:
                date_range["gte"] = filter.publish_date_from.isoformat()
            if filter.publish_date_to:
                date_range["lte"] = filter.publish_date_to.isoformat()
            query["bool"]["must"].append({"range": {"publish_date": date_range}})

        # Full-text search queries

        if filter.isbn_code:
            # Use match_phrase query for isbn_code (exact phrase matching)
            query["bool"]["must"].append(
                {
                    "match_phrase": {
                        "isbn_code": filter.isbn_code,
                    },
                },
            )
        if filter.editor:
            # Use match_phrase query for editor (exact phrase matching)
            query["bool"]["must"].append(
                {
                    "match_phrase": {
                        "editor": filter.editor,
                    },
                },
            )
        if filter.text_query:
            query["bool"]["must"].append(
                {
                    "multi_match": {
                        "query": filter.text_query,
                        "fields": [
                            "book_data.title^2",
                            "book_data.summary",
                            "authors.name",
                            "book_categories.title",
                        ],
                        "type": "best_fields",
                        "fuzziness": "AUTO" if filter.fuzzy_search else "0",
                    },
                },
            )

        if filter.title_query:
            query["bool"]["must"].append(
                {
                    "nested": {
                        "path": "book_data",
                        "query": {
                            "match": {
                                "book_data.title": {
                                    "query": filter.title_query,
                                    "fuzziness": "AUTO" if filter.fuzzy_search else "0",
                                },
                            },
                        },
                    },
                },
            )

        if filter.summary_query:
            query["bool"]["must"].append(
                {
                    "nested": {
                        "path": "book_data",
                        "query": {
                            "match": {
                                "book_data.summary": {
                                    "query": filter.summary_query,
                                    "fuzziness": "AUTO" if filter.fuzzy_search else "0",
                                },
                            },
                        },
                    },
                },
            )

        # Author filters
        if filter.author_name:
            query["bool"]["must"].append(
                {
                    "nested": {
                        "path": "authors",
                        "query": {
                            "match": {
                                "authors.name": {
                                    "query": filter.author_name,
                                    "fuzziness": "AUTO" if filter.fuzzy_search else "0",
                                },
                            },
                        },
                    },
                },
            )

        # Category filters
        if filter.category_title:
            query["bool"]["must"].append(
                {
                    "nested": {
                        "path": "book_categories",
                        "query": {
                            "match": {
                                "book_categories.title": {
                                    "query": filter.category_title,
                                    "fuzziness": "AUTO" if filter.fuzzy_search else "0",
                                },
                            },
                        },
                    },
                },
            )

        # Language filters
        if filter.languages:
            query["bool"]["must"].append(
                {
                    "nested": {
                        "path": "book_data",
                        "query": {
                            "terms": {"book_data.language": filter.languages},
                        },
                    },
                },
            )

        # If no filters are specified, match all
        if not query["bool"]["must"]:
            query = {"match_all": {}}

        return query

    def get_book_by_id(self, id: UUID) -> Book:
        with self.db.get_session(slave=True) as session:
            try:
                book_model = session.exec(
                    select(BookModel).where(BookModel.id == id),
                ).one()
            except NoResultFound:
                raise NotFoundException("Book not found")
            return Book.model_validate(book_model)

    def get_book_by_filter(
        self,
        filter: BookSearchFilter,
    ) -> List[Book]:
        try:
            return self._search_books_elasticsearch(filter)
        except (ESConnectionError, Exception):
            # Fallback to PostgreSQL if Elasticsearch is not available or fails
            return self._search_books_postgresql(filter)

    def _search_books_elasticsearch(self, filter: BookSearchFilter) -> List[Book]:
        """Search books using Elasticsearch"""
        if not self.es_client:
            raise ESConnectionError("Elasticsearch client not available")

        # Build query from filter
        query = self._build_elasticsearch_query(filter)

        # Add pagination
        from_offset = (filter.page - 1) * filter.size

        # Add sorting
        sort = []
        if filter.sort_by:
            sort_order = (
                filter.sort_order if filter.sort_order in ["asc", "desc"] else "asc"
            )
            sort.append({filter.sort_by: {"order": sort_order}})
        else:
            sort.append({"created_at": {"order": "desc"}})

        body = {
            "query": query,
            "from": from_offset,
            "size": filter.size,
            "sort": sort,
        }

        # Add highlighting if requested
        if filter.highlight_fields:
            body["highlight"] = {
                "fields": {field: {} for field in filter.highlight_fields},
            }

        # Execute search
        response = self.es_client.client.search(
            index=self.es_index,
            body=body,
        )

        # Convert results to Book entities
        books = []
        for hit in response["hits"]["hits"]:
            book = self._elasticsearch_document_to_book(hit["_source"])
            books.append(book)

        return books

    def _search_books_postgresql(
        self,
        filter: Optional[BookSearchFilter] = None,
    ) -> List[Book]:
        """Search books using PostgreSQL (fallback method)"""
        with self.db.get_session(slave=True) as session:
            statement = select(BookModel)
            if filter:
                if filter.isbn_code:
                    statement = statement.where(BookModel.isbn_code == filter.isbn_code)
                if filter.editor:
                    statement = statement.where(BookModel.editor == filter.editor)
                if filter.edition:
                    statement = statement.where(BookModel.edition == filter.edition)
                if filter.type:
                    statement = statement.where(BookModel.type == filter.type)
                if filter.publish_date_from or filter.publish_date_to:
                    if filter.publish_date_from:
                        statement = statement.where(
                            BookModel.publish_date >= filter.publish_date_from,
                        )
                    if filter.publish_date_to:
                        statement = statement.where(
                            BookModel.publish_date <= filter.publish_date_to,
                        )
                if filter.author_name:
                    statement = statement.where(
                        and_(
                            BookModel.authors.any(  # type: ignore
                                AuthorModel.name.ilike(f"%{filter.author_name}%"),  # type: ignore
                            ),
                        ),
                    )
                if filter.category_title:
                    statement = statement.where(
                        func.similarity(
                            BookCategoryModel.title,
                            filter.category_title,
                        )
                        > 0.2,
                    )

                # Add pagination
                offset = (filter.page - 1) * filter.size
                statement = statement.offset(offset).limit(filter.size)

            books = session.exec(statement).all()
            return [Book.model_validate(book) for book in books]
