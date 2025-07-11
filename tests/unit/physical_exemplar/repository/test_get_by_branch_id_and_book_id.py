from tests.unit.physical_exemplar.repository.conftest import (
    PhysicalExemplarRepositoryConftest,
)
from uuid6 import uuid7

from src.application.exceptions import NotFoundException


class TestGetByBranchIdAndBookId(PhysicalExemplarRepositoryConftest):

    def setUp(self):
        super().setUp()

        # Create authors with specific names for filtering
        self.author1 = self.author_model_factory.build(name="John Doe")

        # Create book categories with specific titles for filtering
        self.book_category1 = self.book_category_model_factory.build(
            title="Science Fiction",
        )
        # Create book data
        self.book_data1 = self.book_data_model_factory.build()

        # Create branches
        self.branch1 = self.branch_model_factory.build(name="Main Branch")

        # Save dependencies
        self.author_repository.upsert_author(author=self.author1)

        self.book_category_repository.upsert_book_category(
            book_category=self.book_category1,
        )

        self.branch_repository.upsert_branch(branch=self.branch1)

        # Create books with specific attributes for filtering
        self.book1 = self.book_model_factory.build(
            isbn_code="978-0-123456-78-9",
            editor="Publisher A",
            edition=1,
            authors=[self.author1],
            book_categories=[self.book_category1],
            book_data=[self.book_data1],
        )

        # Save books
        self.book_repository.upsert_book(book=self.book1)

        # Create physical exemplars in different branches
        self.physical_exemplar1_branch1 = self.physical_exemplar_model_factory.build(
            book_id=self.book1.id,
            branch_id=self.branch1.id,
            available=True,
            room=1,
            floor=1,
            bookshelf=1,
        )
        # Save physical exemplars
        self.physical_exemplar_repository.upsert_physical_exemplar(
            physical_exemplar=self.physical_exemplar1_branch1,
        )

    def test_get_by_branch_id_and_book_id(self):
        # Arrange
        physical_exemplar = (
            self.physical_exemplar_repository.get_physical_exemplar_by_book_and_branch(
                branch_id=self.branch1.id,
                book_id=self.book1.id,
            )
        )

        # Assert
        self.assertEqual(physical_exemplar.id, self.physical_exemplar1_branch1.id)

    def test_get_by_branch_id_and_book_id_not_found(self):
        # Arrange
        with self.assertRaises(NotFoundException):
            self.physical_exemplar_repository.get_physical_exemplar_by_book_and_branch(
                branch_id=uuid7(),
                book_id=uuid7(),
            )
