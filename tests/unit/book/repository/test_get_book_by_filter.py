from tests.unit.book.repository.conftest import BookRepositoryConftest

from src.domain.entities.book import BookFilter


class TestGetBookByFilter(BookRepositoryConftest):

    def setUp(self):
        super().setUp()
        self.author1 = self.author_model_factory.build()
        self.author2 = self.author_model_factory.build()
        self.author3 = self.author_model_factory.build()
        self.author4 = self.author_model_factory.build()
        self.author5 = self.author_model_factory.build()
        self.author6 = self.author_model_factory.build()

        self.book_category1 = self.book_category_model_factory.build()
        self.book_category2 = self.book_category_model_factory.build()
        self.book_category3 = self.book_category_model_factory.build()
        self.book_category4 = self.book_category_model_factory.build()
        self.book_category5 = self.book_category_model_factory.build()
        self.book_category6 = self.book_category_model_factory.build()

        self.book_data1 = self.book_data_model_factory.build()
        self.book_data2 = self.book_data_model_factory.build()
        self.book_data3 = self.book_data_model_factory.build()
        self.book_data4 = self.book_data_model_factory.build()
        self.book_data5 = self.book_data_model_factory.build()
        self.book_data6 = self.book_data_model_factory.build()
        [
            self.author_repository.upsert_author(author=author)
            for author in [
                self.author1,
                self.author2,
                self.author3,
                self.author4,
                self.author5,
                self.author6,
            ]
        ]

        [
            self.book_category_repository.upsert_book_category(book_category=category)
            for category in [
                self.book_category1,
                self.book_category2,
                self.book_category3,
                self.book_category4,
                self.book_category5,
                self.book_category6,
            ]
        ]

        authors1 = [self.author1, self.author2]
        book_categories1 = [self.book_category1, self.book_category2]
        book_data1 = [self.book_data1, self.book_data2]
        self.book1 = self.book_model_factory.build(
            authors=authors1,
            book_categories=book_categories1,
            book_data=book_data1,
        )

        authors2 = [self.author3, self.author4]
        book_categories2 = [self.book_category3, self.book_category4]
        book_data2 = [self.book_data3, self.book_data4]
        self.book2 = self.book_model_factory.build(
            authors=authors2,
            book_categories=book_categories2,
            book_data=book_data2,
        )

        authors3 = [self.author5, self.author6]
        book_categories3 = [self.book_category5, self.book_category6]
        book_data3 = [self.book_data5, self.book_data6]
        self.book3 = self.book_model_factory.build(
            authors=authors3,
            book_categories=book_categories3,
            book_data=book_data3,
        )

        self.book_repository.upsert_book(book=self.book1)
        self.book_repository.upsert_book(book=self.book2)
        self.book_repository.upsert_book(book=self.book3)

    def test_filter_not_found(self):
        # Act - Filter by non-existent ISBN
        filter_criteria = BookFilter(isbn_code="978-0-000000-00-0")
        results = self.book_repository.get_book_by_filter(filter=filter_criteria)

        # Assert - Should return empty list
        self.assertEqual(results, [])

    def test_no_filter_returns_all(self):
        # Act - Call with no filter
        results = self.book_repository.get_book_by_filter(filter=None)

        # Assert - Should return all books
        self.assertEqual(
            results.sort(key=lambda x: x.id),
            [self.book1, self.book2, self.book3].sort(key=lambda x: x.id),
        )

    def test_empty_filter_returns_all(self):
        # Act - Call with empty filter
        empty_filter = BookFilter()
        results = self.book_repository.get_book_by_filter(filter=empty_filter)

        # Assert - Should return all books
        self.assertEqual(
            results.sort(key=lambda x: x.id),
            [self.book1, self.book2, self.book3].sort(key=lambda x: x.id),
        )
