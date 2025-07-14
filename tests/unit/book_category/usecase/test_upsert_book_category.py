from tests.unit.book_category.usecase.conftest import BookCategoryUseCaseConftest

from src.application.exceptions import OptimisticLockException
from src.application.usecase.book_category.upsert_book_category import (
    UpsertBookCategory,
)


class TestUpsertBookCategory(BookCategoryUseCaseConftest):

    def setUp(self):
        super().setUp()
        self.upsert_book_category = UpsertBookCategory(
            repository=self.mock_book_category_repository,
        )
        self.mock_book_category_repository.upsert_book_category.return_value = None
        self.mock_book_category_repository.upsert_book_category.side_effect = None

    def tearDown(self):
        super().tearDown()
        self.mock_book_category_repository.upsert_book_category.reset_mock()

    def test_execute_successful_upsert(self):
        # Arrange
        book_category = self.book_category_model_factory.build()

        # Mock repository response
        self.mock_book_category_repository.upsert_book_category.return_value = (
            book_category
        )

        # Act
        result = self.upsert_book_category.execute(book_category)

        # Assert
        self.mock_book_category_repository.upsert_book_category.assert_called_once_with(
            book_category,
        )
        self.assertEqual(result, book_category)

    def test_execute_optimistic_lock_exception(self):
        # Arrange
        book_category = self.book_category_model_factory.build()
        self.mock_book_category_repository.upsert_book_category.side_effect = (
            OptimisticLockException
        )

        # Act
        result = self.upsert_book_category.execute(book_category)

        # Assert
        self.assertIsNone(result)
