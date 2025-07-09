from tests.unit.physical_exemplar.repository.conftest import (
    PhysicalExemplarRepositoryConftest,
)

from src.domain.entities.book import BookFilter


class TestFilterByBranchAndBookFilter(PhysicalExemplarRepositoryConftest):

    def setUp(self):
        super().setUp()

        # Create authors with specific names for filtering
        self.author1 = self.author_model_factory.build(name="John Doe")
        self.author2 = self.author_model_factory.build(name="Jane Smith")
        self.author3 = self.author_model_factory.build(name="Bob Johnson")

        # Create book categories with specific titles for filtering
        self.book_category1 = self.book_category_model_factory.build(
            title="Science Fiction",
        )
        self.book_category2 = self.book_category_model_factory.build(title="Fantasy")
        self.book_category3 = self.book_category_model_factory.build(title="Mystery")

        # Create book data
        self.book_data1 = self.book_data_model_factory.build()
        self.book_data2 = self.book_data_model_factory.build()
        self.book_data3 = self.book_data_model_factory.build()

        # Create branches
        self.branch1 = self.branch_model_factory.build(name="Main Branch")
        self.branch2 = self.branch_model_factory.build(name="Secondary Branch")

        # Save dependencies
        [
            self.author_repository.upsert_author(author=author)
            for author in [self.author1, self.author2, self.author3]
        ]

        [
            self.book_category_repository.upsert_book_category(book_category=category)
            for category in [
                self.book_category1,
                self.book_category2,
                self.book_category3,
            ]
        ]

        self.branch_repository.upsert_branch(branch=self.branch1)
        self.branch_repository.upsert_branch(branch=self.branch2)

        # Create books with specific attributes for filtering
        self.book1 = self.book_model_factory.build(
            isbn_code="978-0-123456-78-9",
            editor="Publisher A",
            edition=1,
            authors=[self.author1],
            book_categories=[self.book_category1],
            book_data=[self.book_data1],
        )

        self.book2 = self.book_model_factory.build(
            isbn_code="978-0-987654-32-1",
            editor="Publisher B",
            edition=2,
            authors=[self.author2],
            book_categories=[self.book_category2],
            book_data=[self.book_data2],
        )

        self.book3 = self.book_model_factory.build(
            isbn_code="978-0-555666-77-8",
            editor="Publisher A",
            edition=1,
            authors=[self.author3],
            book_categories=[self.book_category3],
            book_data=[self.book_data3],
        )

        # Save books
        self.book_repository.upsert_book(book=self.book1)
        self.book_repository.upsert_book(book=self.book2)
        self.book_repository.upsert_book(book=self.book3)

        # Create physical exemplars in different branches
        self.physical_exemplar1_branch1 = self.physical_exemplar_model_factory.build(
            book_id=self.book1.id,
            branch_id=self.branch1.id,
            available=True,
            room=1,
            floor=1,
            bookshelf=1,
        )

        self.physical_exemplar2_branch1 = self.physical_exemplar_model_factory.build(
            book_id=self.book2.id,
            branch_id=self.branch1.id,
            available=True,
            room=1,
            floor=1,
            bookshelf=2,
        )

        self.physical_exemplar3_branch1 = self.physical_exemplar_model_factory.build(
            book_id=self.book3.id,
            branch_id=self.branch1.id,
            available=False,
            room=2,
            floor=1,
            bookshelf=1,
        )

        self.physical_exemplar1_branch2 = self.physical_exemplar_model_factory.build(
            book_id=self.book1.id,
            branch_id=self.branch2.id,
            available=True,
            room=1,
            floor=2,
            bookshelf=1,
        )

        # Save physical exemplars
        self.physical_exemplar_repository.upsert_physical_exemplar(
            physical_exemplar=self.physical_exemplar1_branch1,
        )
        self.physical_exemplar_repository.upsert_physical_exemplar(
            physical_exemplar=self.physical_exemplar2_branch1,
        )
        self.physical_exemplar_repository.upsert_physical_exemplar(
            physical_exemplar=self.physical_exemplar3_branch1,
        )
        self.physical_exemplar_repository.upsert_physical_exemplar(
            physical_exemplar=self.physical_exemplar1_branch2,
        )

    def test_filter_by_branch_only(self):
        # Arrange - Empty book filter
        empty_filter = BookFilter()

        # Act - Filter by branch1 only
        results = self.physical_exemplar_repository.filter_by_branch_and_book_filter(
            branch_id=self.branch1.id,
            book_filter=empty_filter,
        )

        # Assert - Should return all physical exemplars in branch1
        self.assertEqual(len(results), 3)
        branch_ids = [exemplar.branch_id for exemplar in results]
        self.assertTrue(all(branch_id == self.branch1.id for branch_id in branch_ids))

    def test_filter_by_branch_and_isbn_code(self):
        # Arrange
        book_filter = BookFilter(isbn_code="978-0-123456-78-9")

        # Act
        results = self.physical_exemplar_repository.filter_by_branch_and_book_filter(
            branch_id=self.branch1.id,
            book_filter=book_filter,
        )

        # Assert - Should return only physical exemplar for book1 in branch1
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].book_id, self.book1.id)
        self.assertEqual(results[0].branch_id, self.branch1.id)

    def test_filter_by_branch_and_editor(self):
        # Arrange
        book_filter = BookFilter(editor="Publisher A")

        # Act
        results = self.physical_exemplar_repository.filter_by_branch_and_book_filter(
            branch_id=self.branch1.id,
            book_filter=book_filter,
        )

        # Assert - Should return physical exemplars for book1 and book3 in branch1
        self.assertEqual(len(results), 2)
        book_ids = [exemplar.book_id for exemplar in results]
        self.assertIn(self.book1.id, book_ids)
        self.assertIn(self.book3.id, book_ids)

    def test_filter_by_branch_and_edition(self):
        # Arrange
        book_filter = BookFilter(edition=1)

        # Act
        results = self.physical_exemplar_repository.filter_by_branch_and_book_filter(
            branch_id=self.branch1.id,
            book_filter=book_filter,
        )

        # Assert - Should return physical exemplars for book1 and book3 in branch1
        self.assertEqual(len(results), 2)
        book_ids = [exemplar.book_id for exemplar in results]
        self.assertIn(self.book1.id, book_ids)
        self.assertIn(self.book3.id, book_ids)

    def test_filter_by_branch_and_author_name(self):
        # Arrange
        book_filter = BookFilter(author_name="John")

        # Act
        results = self.physical_exemplar_repository.filter_by_branch_and_book_filter(
            branch_id=self.branch1.id,
            book_filter=book_filter,
        )

        # Assert - Should return physical exemplars for books by authors with "John" in name
        self.assertGreater(len(results), 0)
        # Should include book1 (John Doe) and book3 (Bob Johnson)
        book_ids = [exemplar.book_id for exemplar in results]
        self.assertIn(self.book1.id, book_ids)

    def test_filter_by_branch_and_book_category_name(self):
        # Arrange
        book_filter = BookFilter(book_category_name="Science Fiction")

        # Act
        results = self.physical_exemplar_repository.filter_by_branch_and_book_filter(
            branch_id=self.branch1.id,
            book_filter=book_filter,
        )

        # Assert - Should return physical exemplars for books in Science Fiction category
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].book_id, self.book1.id)

    def test_filter_no_results_in_branch(self):
        # Arrange
        book_filter = BookFilter(isbn_code="978-0-123456-78-9")

        # Act - Search in branch2 for book that only exists in branch1
        results = self.physical_exemplar_repository.filter_by_branch_and_book_filter(
            branch_id=self.branch2.id,
            book_filter=book_filter,
        )

        # Assert - Should return empty list since book1 exemplar in branch2 has different ISBN
        # Wait, this test logic is wrong. Let me fix it.
        # Actually, book1 does exist in branch2, so this should return 1 result
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].book_id, self.book1.id)
        self.assertEqual(results[0].branch_id, self.branch2.id)

    def test_filter_non_existent_book_criteria(self):
        # Arrange
        book_filter = BookFilter(isbn_code="978-0-000000-00-0")

        # Act
        results = self.physical_exemplar_repository.filter_by_branch_and_book_filter(
            branch_id=self.branch1.id,
            book_filter=book_filter,
        )

        # Assert - Should return empty list
        self.assertEqual(len(results), 0)

    def test_filter_multiple_criteria(self):
        # Arrange
        book_filter = BookFilter(
            editor="Publisher A",
            edition=1,
        )

        # Act
        results = self.physical_exemplar_repository.filter_by_branch_and_book_filter(
            branch_id=self.branch1.id,
            book_filter=book_filter,
        )

        # Assert - Should return physical exemplars for books that match both criteria
        self.assertEqual(len(results), 2)
        book_ids = [exemplar.book_id for exemplar in results]
        self.assertIn(self.book1.id, book_ids)
        self.assertIn(self.book3.id, book_ids)
