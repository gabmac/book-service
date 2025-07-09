from tests.unit.book_category.usecase.conftest import BookCategoryUseCaseConftest

from src.application.usecase.book_category.book_category_filter import (
    FilterBookCategory,
)
from src.domain.entities.book_category import BookCategoryFilter


class TestFilterBookCategory(BookCategoryUseCaseConftest):

    def setUp(self):
        super().setUp()
        self.filter_book_category = FilterBookCategory(
            repository=self.mock_book_category_repository,
        )
        self.mock_book_category_repository.get_book_category_by_filter.return_value = (
            None
        )
        self.mock_book_category_repository.get_book_category_by_filter.side_effect = (
            None
        )

    def tearDown(self):
        super().tearDown()
        self.mock_book_category_repository.get_book_category_by_filter.reset_mock()

    def test_execute_with_filter(self):
        # Arrange
        book_category1 = self.book_category_model_factory.build(title="Fiction")
        book_category2 = self.book_category_model_factory.build(title="Fantasy")
        book_categories = [book_category1, book_category2]

        filter_obj = BookCategoryFilter(title="Fiction")

        # Mock repository response
        self.mock_book_category_repository.get_book_category_by_filter.return_value = (
            book_categories
        )

        # Act
        result = self.filter_book_category.execute(filter_obj)

        # Assert
        self.mock_book_category_repository.get_book_category_by_filter.assert_called_once_with(
            filter_obj,
        )
        self.assertEqual(result, book_categories)

    def test_execute_empty_result(self):
        # Arrange
        filter_obj = BookCategoryFilter(title="Non-existent Category")

        # Mock repository response - no categories found
        self.mock_book_category_repository.get_book_category_by_filter.return_value = []

        # Act
        result = self.filter_book_category.execute(filter_obj)

        # Assert
        self.mock_book_category_repository.get_book_category_by_filter.assert_called_once_with(
            filter_obj,
        )
        self.assertEqual(result, [])
