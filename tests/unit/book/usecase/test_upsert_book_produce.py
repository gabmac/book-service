from tests.unit.book.usecase.conftest import BookUseCaseConftest

from src.application.exceptions import NotFoundException
from src.application.usecase.book.upsert_book_produce import UpsertBookProduce
from src.domain.entities.book import Book


class TestUpsertBookProduce(BookUseCaseConftest):

    def setUp(self):
        super().setUp()
        self.upsert_book_produce = UpsertBookProduce(
            producer=self.mock_book_producer,
            author_repository=self.mock_author_repository,
            book_category_repository=self.mock_book_category_repository,
        )
        self.mock_author_repository.get_authors_by_ids.return_value = None
        self.mock_book_category_repository.get_book_categories_by_ids.return_value = (
            None
        )
        self.mock_author_repository.get_authors_by_ids.side_effect = None
        self.mock_book_category_repository.get_book_categories_by_ids.side_effect = None
        self.mock_book_producer.upsert_book.return_value = None
        self.mock_book_producer.upsert_book.side_effect = None

    def tearDown(self):
        super().tearDown()
        self.mock_author_repository.get_authors_by_ids.reset_mock()
        self.mock_book_category_repository.get_book_categories_by_ids.reset_mock()
        self.mock_book_producer.upsert_book.reset_mock()

    async def test_execute_successful_upsert(self):
        # Arrange
        author1 = self.author_model_factory.build()
        author2 = self.author_model_factory.build()
        book_category1 = self.book_category_model_factory.build()
        book_category2 = self.book_category_model_factory.build()

        book = self.book_model_factory.build(
            author_ids=[author1.id, author2.id],
            category_ids=[book_category1.id, book_category2.id],
            authors=None,
            book_categories=None,
        )

        # Mock repository responses
        self.mock_author_repository.get_authors_by_ids.return_value = [author1, author2]
        self.mock_book_category_repository.get_book_categories_by_ids.return_value = [
            book_category1,
            book_category2,
        ]

        # Act
        result = await self.upsert_book_produce.execute(book)
        response = Book(
            id=book.id,
            isbn_code=book.isbn_code,
            editor=book.editor,
            edition=book.edition,
            type=book.type,
            publish_date=book.publish_date,
            book_data=book.book_data,
            authors=[author1, author2],
            book_categories=[book_category1, book_category2],
            created_by=book.created_by,
            updated_by=book.updated_by,
            created_at=book.created_at,
            updated_at=book.updated_at,
        )
        # Assert
        self.mock_author_repository.get_authors_by_ids.assert_called_once_with(
            [author1.id, author2.id],
        )
        self.mock_book_category_repository.get_book_categories_by_ids.assert_called_once_with(
            [book_category1.id, book_category2.id],
        )
        self.mock_book_producer.upsert_book.assert_called_once()
        self.assertEqual(result, response)

    async def test_execute_author_not_found(self):
        # Arrange
        author1 = self.author_model_factory.build()
        author2 = self.author_model_factory.build()
        book_category1 = self.book_category_model_factory.build()

        book = self.book_model_factory.build(
            author_ids=[author1.id, author2.id],
            category_ids=[book_category1.id],
        )

        # Mock repository responses - only one author found
        self.mock_author_repository.get_authors_by_ids.return_value = [author1]
        self.mock_book_category_repository.get_book_categories_by_ids.return_value = [
            book_category1,
        ]

        # Act & Assert
        with self.assertRaises(NotFoundException) as context:
            await self.upsert_book_produce.execute(book)

        self.assertEqual(str(context.exception), "Some authors not found")
        self.mock_author_repository.get_authors_by_ids.assert_called_once_with(
            [author1.id, author2.id],
        )
        self.mock_book_producer.upsert_book.assert_not_called()
        self.mock_book_category_repository.get_book_categories_by_ids.assert_not_called()

    async def test_execute_book_category_not_found(self):
        # Arrange
        author1 = self.author_model_factory.build()
        book_category1 = self.book_category_model_factory.build()
        book_category2 = self.book_category_model_factory.build()

        book = self.book_model_factory.build(
            author_ids=[author1.id],
            category_ids=[book_category1.id, book_category2.id],
        )

        # Mock repository responses - only one book category found
        self.mock_author_repository.get_authors_by_ids.return_value = [author1]
        self.mock_book_category_repository.get_book_categories_by_ids.return_value = [
            book_category1,
        ]

        # Act & Assert
        with self.assertRaises(NotFoundException) as context:
            await self.upsert_book_produce.execute(book)

        self.assertEqual(str(context.exception), "Some book categories not found")
        self.mock_author_repository.get_authors_by_ids.assert_called_once_with(
            [author1.id],
        )
        self.mock_book_category_repository.get_book_categories_by_ids.assert_called_once_with(
            [book_category1.id, book_category2.id],
        )
        self.mock_book_producer.upsert_book.assert_not_called()
