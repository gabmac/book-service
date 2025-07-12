from tests.unit.book.repository.conftest import BookRepositoryConftest


class TestUpsertBook(BookRepositoryConftest):
    def setUp(self):
        super().setUp()
        self.author1 = self.author_model_factory.build()
        self.author2 = self.author_model_factory.build()
        self.author3 = self.author_model_factory.build()
        self.author4 = self.author_model_factory.build()
        self.book_category1 = self.book_category_model_factory.build()
        self.book_category2 = self.book_category_model_factory.build()
        self.book_category3 = self.book_category_model_factory.build()
        self.book_category4 = self.book_category_model_factory.build()
        self.book_data1 = self.book_data_model_factory.build()
        self.book_data2 = self.book_data_model_factory.build()
        self.book_data3 = self.book_data_model_factory.build()
        self.book_data4 = self.book_data_model_factory.build()

        self.author_write_repository.upsert_author(author=self.author1)
        self.author_write_repository.upsert_author(author=self.author2)
        self.author_write_repository.upsert_author(author=self.author3)
        self.author_write_repository.upsert_author(author=self.author4)
        self.book_category_write_repository.upsert_book_category(
            book_category=self.book_category1,
        )
        self.book_category_write_repository.upsert_book_category(
            book_category=self.book_category2,
        )
        self.book_category_write_repository.upsert_book_category(
            book_category=self.book_category3,
        )
        self.book_category_write_repository.upsert_book_category(
            book_category=self.book_category4,
        )

    def test_new_book_with_authors_categories_and_data(self):
        # Arrange
        authors = [self.author1, self.author2]
        book_categories = [self.book_category1, self.book_category2]
        book_data = [self.book_data1, self.book_data2]
        book = self.book_model_factory.build(
            authors=authors,
            book_categories=book_categories,
            book_data=book_data,
        )

        # Act
        result = self.book_write_repository.upsert_book(book=book)
        self.validate_book([result], [book])

    def test_update_book_with_authors_categories_and_data(self):
        # Arrange - Create and save a book first

        authors = [self.author1, self.author2]
        book_categories = [self.book_category1, self.book_category2]
        book_data = [self.book_data1, self.book_data2]
        book = self.book_model_factory.build(
            authors=authors,
            book_categories=book_categories,
            book_data=book_data,
        )

        # Act
        self.book_write_repository.upsert_book(book=book)

        book_data = [self.book_data_model_factory.build() for _ in range(2)]
        book = self.book_model_factory.build(
            id=book.id,
            authors=[self.author3, self.author4],
            book_categories=[self.book_category3, self.book_category4],
            book_data=book_data,
        )

        # Act - Update the book editor, authors, categories, and book data
        result = self.book_write_repository.upsert_book(book=book)
        self.validate_book([result], [book])
