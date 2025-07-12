from tests.unit.physical_exemplar.repository.conftest import (
    PhysicalExemplarRepositoryConftest,
)


class TestUpsertPhysicalExemplar(PhysicalExemplarRepositoryConftest):

    def setUp(self):
        super().setUp()

        # Create authors, categories, book data, branches first
        self.author1 = self.author_model_factory.build()
        self.author2 = self.author_model_factory.build()

        self.book_category1 = self.book_category_model_factory.build()
        self.book_category2 = self.book_category_model_factory.build()

        self.book_data1 = self.book_data_model_factory.build()
        self.book_data2 = self.book_data_model_factory.build()
        self.book_data3 = self.book_data_model_factory.build()
        self.book_data4 = self.book_data_model_factory.build()

        self.branch1 = self.branch_model_factory.build()
        self.branch2 = self.branch_model_factory.build()

        # Save dependencies
        self.author_write_repository.upsert_author(author=self.author1)
        self.author_write_repository.upsert_author(author=self.author2)

        self.book_category_write_repository.upsert_book_category(
            book_category=self.book_category1,
        )
        self.book_category_write_repository.upsert_book_category(
            book_category=self.book_category2,
        )

        self.branch_write_repository.upsert_branch(branch=self.branch1)
        self.branch_write_repository.upsert_branch(branch=self.branch2)

        # Create books with relationships
        authors = [self.author1, self.author2]
        book_categories = [self.book_category1, self.book_category2]
        book_data = [self.book_data1, self.book_data2]
        book_data2 = [self.book_data3, self.book_data4]

        self.book1 = self.book_model_factory.build(
            authors=authors,
            book_categories=book_categories,
            book_data=book_data,
        )

        self.book2 = self.book_model_factory.build(
            authors=authors,
            book_categories=book_categories,
            book_data=book_data2,
        )

        # Save books
        self.book_write_repository.upsert_book(book=self.book1)
        self.book_write_repository.upsert_book(book=self.book2)

    def test_new_physical_exemplar(self):
        # Arrange
        physical_exemplar = self.physical_exemplar_model_factory.build(
            book_id=self.book1.id,
            branch_id=self.branch1.id,
            book=self.book1,
            branch=self.branch1,
            available=True,
            room=1,
            floor=2,
            bookshelf=3,
        )

        # Act
        result = self.physical_exemplar_write_repository.upsert_physical_exemplar(
            physical_exemplar=physical_exemplar,
        )

        # Assert
        exclude_fields = [
            "updated_at",
            "updated_by",
            "created_at",
            "created_by",
            "book",
        ]
        self.assertEqual(
            result.model_dump(exclude=exclude_fields),  # type: ignore
            physical_exemplar.model_dump(exclude=exclude_fields),
        )

    def test_update_physical_exemplar(self):
        # Arrange - Create and save a physical exemplar first
        physical_exemplar = self.physical_exemplar_model_factory.build(
            book_id=self.book1.id,
            branch_id=self.branch1.id,
            book=self.book1,
            branch=self.branch1,
            available=True,
            room=1,
            floor=2,
            bookshelf=3,
        )

        self.physical_exemplar_write_repository.upsert_physical_exemplar(
            physical_exemplar=physical_exemplar,
        )

        result = self.physical_exemplar_write_repository.upsert_physical_exemplar(
            physical_exemplar=physical_exemplar,
        )

        # Assert
        exclude_fields = [
            "updated_at",
            "updated_by",
            "created_at",
            "created_by",
            "book",
        ]
        self.assertEqual(
            result.model_dump(exclude=exclude_fields),  # type: ignore
            physical_exemplar.model_dump(exclude=exclude_fields),
        )
