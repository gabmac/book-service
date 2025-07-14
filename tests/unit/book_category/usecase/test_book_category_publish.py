from tests.unit.book_category.usecase.conftest import BookCategoryUseCaseConftest

from src.application.exceptions import NotFoundException
from src.application.usecase.book_category.book_category_publish import (
    CreateBookCategoryProduce,
)
from src.domain.entities.book_category import BookCategory


class TestCreateBookCategoryProduce(BookCategoryUseCaseConftest):

    def setUp(self):
        super().setUp()
        self.create_book_category_produce = CreateBookCategoryProduce(
            book_category_producer=self.mock_book_category_producer,
            repository=self.mock_book_category_repository,
        )
        self.mock_book_category_repository.get_book_category_by_title.return_value = (
            None
        )
        self.mock_book_category_repository.get_book_category_by_title.side_effect = None
        self.mock_book_category_producer.upsert_book_category.return_value = None
        self.mock_book_category_producer.upsert_book_category.side_effect = None

    def tearDown(self):
        super().tearDown()
        self.mock_book_category_repository.get_book_category_by_title.reset_mock()
        self.mock_book_category_producer.upsert_book_category.reset_mock()

    def test_execute_new_book_category(self):
        # Arrange
        book_category = self.book_category_model_factory.build(title="Science Fiction")

        # Mock repository response - category not found (new category)
        self.mock_book_category_repository.get_book_category_by_title.side_effect = (
            NotFoundException(
                "Book category not found",
            )
        )

        # Act
        result = self.create_book_category_produce.execute(book_category)

        # Assert
        self.mock_book_category_repository.get_book_category_by_title.assert_called_once_with(
            book_category.title,
        )
        self.mock_book_category_producer.upsert_book_category.assert_called_once()

        # Verify the result has the expected fields for new category
        self.assertEqual(result, book_category)

    def test_execute_existing_book_category(self):
        # Arrange
        existing_category = self.book_category_model_factory.build()
        new_category = self.book_category_model_factory.build(
            title=existing_category.title,
            description=existing_category.description,
            updated_by=existing_category.updated_by,
        )
        updated_category = BookCategory.model_validate(new_category)
        updated_category.created_by = existing_category.created_by
        updated_category.created_at = existing_category.created_at
        updated_category.id = existing_category.id
        updated_category.updated_at = existing_category.updated_at
        updated_category.version = existing_category.version + 1

        # Mock repository response - category found (update)
        self.mock_book_category_repository.get_book_category_by_title.return_value = (
            existing_category
        )

        # Act
        result = self.create_book_category_produce.execute(updated_category)

        # Assert
        self.mock_book_category_repository.get_book_category_by_title.assert_called_once_with(
            updated_category.title,
        )
        self.mock_book_category_producer.upsert_book_category.assert_called_once()

        # Verify the result preserves existing category data
        self.assertEqual(result, updated_category)
