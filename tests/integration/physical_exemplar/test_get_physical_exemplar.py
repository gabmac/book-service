import json

from tests.integration.physical_exemplar.conftest import PhysicalExemplarViewConfTest
from uuid6 import uuid7

from src.application.dto.physical_exemplar import PhysicalExemplarResponse


class TestGetPhysicalExemplar(PhysicalExemplarViewConfTest):
    def setUp(self):
        super().setUp()

        # Create author and category for book
        author = self.author_model_factory.build(
            name="Test Author",
            created_by="test_user",
            updated_by="test_user",
        )
        category = self.book_category_model_factory.build(
            title="Test Category",
            description="Test description",
            created_by="test_user",
            updated_by="test_user",
        )

        self.stored_author = self.author_write_repository.upsert_author(author)
        self.stored_category = self.book_category_write_repository.upsert_book_category(
            category,
        )

        # Create book
        book_data = [
            self.book_data_model_factory.build(
                title="Test Book Data",
                language="en",
                created_by="test_user",
                updated_by="test_user",
            ),
        ]
        book = self.book_model_factory.build(
            isbn_code="978-0-123456-78-9",
            editor="Test Editor",
            authors=[self.stored_author],
            book_categories=[self.stored_category],
            book_data=book_data,
            created_by="test_user",
            updated_by="test_user",
        )

        self.stored_book = self.book_write_repository.upsert_book(book)

        # Create branch
        branch = self.branch_model_factory.build(
            name="Test Branch",
            created_by="test_user",
            updated_by="test_user",
        )

        self.stored_branch = self.branch_write_repository.upsert_branch(branch)

        # Create physical exemplar
        physical_exemplar = self.physical_exemplar_model_factory.build(
            book_id=self.stored_book.id,
            branch_id=self.stored_branch.id,
            book=self.stored_book,
            branch=self.stored_branch,
            available=True,
            room=1,
            floor=2,
            bookshelf=3,
            created_by="test_user",
            updated_by="test_user",
        )

        self.stored_physical_exemplar = (
            self.physical_exemplar_write_repository.upsert_physical_exemplar(
                physical_exemplar,
            )
        )

    def test_get_physical_exemplar_success(self):
        # Scenario: Successfully get a physical exemplar by book and branch ID

        # Given a book and branch that have a physical exemplar

        # When a request is made to get the physical exemplar by book and branch ID
        response = self.client.get(
            f"api/physical_exemplar/branch/{self.stored_branch.id}/book/{self.stored_book.id}/",
        )

        # Then the response is a 200 status code
        self.assertEqual(response.status_code, 200)
        response_body = PhysicalExemplarResponse.model_validate_json(
            json.dumps(response.json()),
        )

        # Verify specific fields
        self.assertEqual(response_body.id, self.stored_physical_exemplar.id)
        self.assertEqual(response_body.book_id, self.stored_book.id)
        self.assertEqual(response_body.branch_id, self.stored_branch.id)
        self.assertEqual(
            response_body.available,
            self.stored_physical_exemplar.available,
        )
        self.assertEqual(response_body.room, self.stored_physical_exemplar.room)
        self.assertEqual(response_body.floor, self.stored_physical_exemplar.floor)
        self.assertEqual(
            response_body.bookshelf,
            self.stored_physical_exemplar.bookshelf,
        )
        self.assertEqual(
            response_body.created_by,
            self.stored_physical_exemplar.created_by,
        )
        self.assertEqual(
            response_body.updated_by,
            self.stored_physical_exemplar.updated_by,
        )

        # Verify nested book data
        self.assertEqual(response_body.book.id, self.stored_book.id)
        self.assertEqual(response_body.book.isbn_code, self.stored_book.isbn_code)
        self.assertEqual(response_body.book.editor, self.stored_book.editor)
        self.assertEqual(response_body.book.edition, self.stored_book.edition)
        self.assertEqual(response_body.book.type, self.stored_book.type)
        self.assertEqual(response_body.book.publish_date, self.stored_book.publish_date)

        # Verify nested branch data
        self.assertEqual(response_body.branch.id, self.stored_branch.id)
        self.assertEqual(response_body.branch.name, self.stored_branch.name)

    def test_get_physical_exemplar_not_found(self):
        # Scenario: Attempt to get a physical exemplar that doesn't exist

        # Given book and branch IDs that don't have a physical exemplar
        non_existent_book_id = uuid7()
        non_existent_branch_id = uuid7()

        # When a request is made to get the physical exemplar by non-existent book and branch ID
        response = self.client.get(
            f"api/physical_exemplar/branch/{non_existent_branch_id}/book/{non_existent_book_id}/",
        )

        # Then the response is a 404 status code
        self.assertEqual(response.status_code, 404)
        response_data = response.json()
        self.assertEqual(response_data["detail"], "Physical exemplar not found")

    def test_get_physical_exemplar_existing_book_and_branch_but_no_physical_exemplar(
        self,
    ):
        # Scenario: Attempt to get a physical exemplar with valid book and branch but no physical exemplar exists

        # Given a different book and branch that exist but have no physical exemplar
        another_book = self.book_model_factory.build(
            isbn_code="978-0-987654-32-1",
            editor="Another Editor",
            authors=[self.stored_author],
            book_categories=[self.stored_category],
            book_data=[
                self.book_data_model_factory.build(
                    title="Another Book Data",
                    language="en",
                    created_by="test_user",
                    updated_by="test_user",
                ),
            ],
            created_by="test_user",
            updated_by="test_user",
        )
        stored_another_book = self.book_write_repository.upsert_book(another_book)

        another_branch = self.branch_model_factory.build(
            name="Another Branch",
            created_by="test_user",
            updated_by="test_user",
        )
        stored_another_branch = self.branch_write_repository.upsert_branch(
            another_branch,
        )

        # When a request is made to get the physical exemplar by existing book and branch ID
        response = self.client.get(
            f"api/physical_exemplar/branch/{stored_another_branch.id}/book/{stored_another_book.id}/",
        )

        # Then the response is a 404 status code
        self.assertEqual(response.status_code, 404)
        response_data = response.json()
        self.assertEqual(response_data["detail"], "Physical exemplar not found")
