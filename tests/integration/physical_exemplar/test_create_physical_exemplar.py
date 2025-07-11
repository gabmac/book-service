import json

from tests.integration.physical_exemplar.conftest import PhysicalExemplarViewConfTest

from src.application.dto.physical_exemplar import ProcessingPhysicalExemplar
from src.domain.entities.physical_exemplar import PhysicalExemplar


class TestCreatePhysicalExemplar(PhysicalExemplarViewConfTest):
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

        self.stored_author = self.author_repository.upsert_author(author)
        self.stored_category = self.book_category_repository.upsert_book_category(
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

        self.stored_book = self.book_repository.upsert_book(book)

        # Create branch
        branch = self.branch_model_factory.build(
            name="Test Branch",
            created_by="test_user",
            updated_by="test_user",
        )

        self.stored_branch = self.branch_repository.upsert_branch(branch)

    def test_create_physical_exemplar(self):
        # Scenario: Create a physical exemplar

        # When a request is made to create a physical exemplar
        body = self.physical_exemplar_create_model_factory.build()
        response = self.client.put(
            f"api/physical_exemplar/branch/{self.stored_branch.id}/book/{self.stored_book.id}/",
            json=body.model_dump(),
        )

        # Then the response is a 202 status code
        self.assertEqual(response.status_code, 202)
        response_body = ProcessingPhysicalExemplar.model_validate_json(
            json.dumps(response.json()),
        )

        self.assertEqual(response_body.message, "Task is processing")
        self.assertDictEqual(
            json.loads(
                response_body.physical_exemplar.model_dump_json(
                    exclude_none=True,
                    exclude_unset=True,
                ),
            ),
            json.loads(
                PhysicalExemplar.model_validate(
                    response_body.physical_exemplar,
                ).model_dump_json(exclude_none=True, exclude_unset=True),
            ),
        )

        # And the message is consumed from the queue
        self.consumer.consume("physical_exemplar.upsert")

        # And the physical exemplar is stored in the database
        stored_physical_exemplar = (
            self.physical_exemplar_repository.get_physical_exemplar_by_book_and_branch(
                book_id=self.stored_book.id,
                branch_id=self.stored_branch.id,
            )
        )

        physical_exemplar = PhysicalExemplar(
            available=body.available,
            room=body.room,
            floor=body.floor,
            book=self.stored_book,
            branch=self.stored_branch,
            bookshelf=body.bookshelf,
            book_id=self.stored_book.id,
            branch_id=self.stored_branch.id,
            created_by=body.user,
            updated_by=body.user,
        )

        exclude_fields = {"created_at", "updated_at", "id"}

        self.assertDictEqual(
            json.loads(
                stored_physical_exemplar.model_dump_json(
                    exclude_none=True,
                    exclude_unset=True,
                    exclude=exclude_fields,
                ),
            ),
            json.loads(
                physical_exemplar.model_dump_json(
                    exclude_none=True,
                    exclude_unset=True,
                    exclude=exclude_fields,
                ),
            ),
        )

    def test_create_physical_exemplar_idempotent(self):
        # Scenario: Create the same physical exemplar twice (idempotent behavior)

        # Given a physical exemplar stored in database
        physical_exemplar = self.physical_exemplar_model_factory.build(
            book_id=self.stored_book.id,
            branch_id=self.stored_branch.id,
            book=self.stored_book,
            branch=self.stored_branch,
        )
        self.physical_exemplar_repository.upsert_physical_exemplar(physical_exemplar)

        body = self.physical_exemplar_create_model_factory.build()

        # When the same request is made twice
        response = self.client.put(
            f"api/physical_exemplar/branch/{self.stored_branch.id}/book/{self.stored_book.id}/",
            json=body.model_dump(),
        )

        # Then the response is a 202 status code
        self.assertEqual(response.status_code, 202)
        response_body = ProcessingPhysicalExemplar.model_validate_json(
            json.dumps(response.json()),
        )

        self.assertEqual(response_body.message, "Task is processing")
        self.assertDictEqual(
            json.loads(
                response_body.physical_exemplar.model_dump_json(
                    exclude_none=True,
                    exclude_unset=True,
                ),
            ),
            json.loads(
                PhysicalExemplar.model_validate(
                    response_body.physical_exemplar,
                ).model_dump_json(exclude_none=True, exclude_unset=True),
            ),
        )

        self.consumer.consume("physical_exemplar.upsert")

        # And only one physical exemplar exists in the database
        stored_physical_exemplar = (
            self.physical_exemplar_repository.get_physical_exemplar_by_book_and_branch(
                book_id=self.stored_book.id,
                branch_id=self.stored_branch.id,
            )
        )

        physical_exemplar = PhysicalExemplar(
            available=body.available,
            room=body.room,
            floor=body.floor,
            book=self.stored_book,
            branch=self.stored_branch,
            bookshelf=body.bookshelf,
            book_id=self.stored_book.id,
            branch_id=self.stored_branch.id,
            created_by=physical_exemplar.created_by,
            updated_by=body.user,
        )

        exclude_fields = {"created_at", "updated_at", "id"}

        self.assertDictEqual(
            json.loads(
                stored_physical_exemplar.model_dump_json(
                    exclude_none=True,
                    exclude_unset=True,
                    exclude=exclude_fields,
                ),
            ),
            json.loads(
                physical_exemplar.model_dump_json(
                    exclude_none=True,
                    exclude_unset=True,
                    exclude=exclude_fields,
                ),
            ),
        )

    def test_create_physical_exemplar_branch_not_found(self):
        # Scenario: Try to create a physical exemplar with a non-existent branch

        from uuid6 import uuid7

        body = self.physical_exemplar_create_model_factory.build()
        non_existent_branch_id = uuid7()
        response = self.client.put(
            f"api/physical_exemplar/branch/{non_existent_branch_id}/book/{self.stored_book.id}/",
            json=body.model_dump(),
        )

        # Then the response is a 404 status code
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json().get("detail"), "Branch not found")

    def test_create_physical_exemplar_book_not_found(self):
        # Scenario: Try to create a physical exemplar with a non-existent book

        from uuid6 import uuid7

        body = self.physical_exemplar_create_model_factory.build()
        non_existent_book_id = uuid7()
        response = self.client.put(
            f"api/physical_exemplar/branch/{self.stored_branch.id}/book/{non_existent_book_id}/",
            json=body.model_dump(),
        )

        # Then the response is a 404 status code
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json().get("detail"), "Book not found")
