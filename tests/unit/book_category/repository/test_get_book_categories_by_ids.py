from typing import List
from uuid import uuid4

from tests.unit.book_category.repository.conftest import BookCategoryRepositoryConftest


class TestGetBookCategoriesByIds(BookCategoryRepositoryConftest):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Arrange - Create and save some book categories
        cls.category1 = cls.book_category_model_factory.build()
        cls.category2 = cls.book_category_model_factory.build()
        cls.category3 = cls.book_category_model_factory.build()

        cls.book_category_repository.upsert_book_category(book_category=cls.category1)
        cls.book_category_repository.upsert_book_category(book_category=cls.category2)
        cls.book_category_repository.upsert_book_category(book_category=cls.category3)

    def test_get_existing_book_categories(self):
        # Act - Request with only some existing IDs
        ids = [self.category1.id, self.category2.id]
        results = self.book_category_repository.get_book_categories_by_ids(ids=ids)

        # Assert - Should return only the requested book categories
        self.assertEqual(
            results.sort(key=lambda x: x.id),
            [self.category1, self.category2].sort(key=lambda x: x.id),
        )

    def test_get_no_existing_book_categories(self):
        # Arrange - Generate non-existent IDs
        non_existent_ids = [uuid4()]

        # Act - Request with non-existing IDs
        results = self.book_category_repository.get_book_categories_by_ids(
            ids=non_existent_ids,
        )

        # Assert - Should return empty list
        self.assertEqual(results, [])

    def test_get_empty_ids_list(self):
        # Arrange - Empty list of IDs
        empty_ids: List = []

        # Act - Request with empty IDs list
        results = self.book_category_repository.get_book_categories_by_ids(
            ids=empty_ids,
        )

        # Assert - Should return empty list
        self.assertEqual(results, [])
