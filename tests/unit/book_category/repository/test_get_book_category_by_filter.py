from tests.unit.book_category.repository.conftest import BookCategoryRepositoryConftest

from src.domain.entities.book_category import BookCategoryFilter


class TestGetBookCategoryByFilter(BookCategoryRepositoryConftest):

    def setUp(self):
        super().setUp()
        self.category1 = self.book_category_model_factory.build(
            title="Science Fiction",
            description="Books about space",
        )
        self.category2 = self.book_category_model_factory.build(
            title="Science Fiction 2",
            description="Books about future",
        )
        self.category3 = self.book_category_model_factory.build(
            title="Fantasy",
            description="Books about space",
        )

        self.book_category_repository.upsert_book_category(book_category=self.category1)
        self.book_category_repository.upsert_book_category(book_category=self.category2)
        self.book_category_repository.upsert_book_category(book_category=self.category3)

    def test_filter_by_title_and_description(self):
        # Arrange - Create and save book categories

        # Act - Filter by both title and description
        filter_criteria = BookCategoryFilter(
            title=self.category1.title,
            description=self.category1.description,
        )
        results = self.book_category_repository.get_book_category_by_filter(
            filter=filter_criteria,
        )

        # Assert - Should return only category1 that matches both criteria
        self.assertEqual(results, [self.category1])

    def test_no_filter_returns_all(self):
        # Arrange - Create and save multiple book categories

        # Act - Call with filter that has no criteria
        empty_filter = BookCategoryFilter(title=None, description=None)
        results = self.book_category_repository.get_book_category_by_filter(
            filter=empty_filter,
        )

        # Assert - Should return all book categories
        self.assertEqual(
            results.sort(key=lambda x: x.id),
            [self.category1, self.category2, self.category3].sort(key=lambda x: x.id),
        )
