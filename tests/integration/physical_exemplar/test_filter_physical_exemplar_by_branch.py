import json

from tests.integration.physical_exemplar.conftest import PhysicalExemplarViewConfTest

from src.domain.entities.physical_exemplar import PhysicalExemplar


class TestFilterPhysicalExemplarByBranch(PhysicalExemplarViewConfTest):
    def setUp(self):
        super().setUp()

        # Create authors
        author1 = self.author_model_factory.build(
            name="John Doe",
            created_by="test_user",
            updated_by="test_user",
        )
        author2 = self.author_model_factory.build(
            name="Jane Smith",
            created_by="test_user",
            updated_by="test_user",
        )

        self.stored_author1 = self.author_repository.upsert_author(author1)
        self.stored_author2 = self.author_repository.upsert_author(author2)

        # Create categories
        category1 = self.book_category_model_factory.build(
            title="Fiction",
            description="Fiction books",
            created_by="test_user",
            updated_by="test_user",
        )
        category2 = self.book_category_model_factory.build(
            title="Science",
            description="Science books",
            created_by="test_user",
            updated_by="test_user",
        )

        self.stored_category1 = self.book_category_repository.upsert_book_category(
            category1,
        )
        self.stored_category2 = self.book_category_repository.upsert_book_category(
            category2,
        )

        # Create books
        book_data1 = [
            self.book_data_model_factory.build(
                title="The Great Novel",
                language="en",
                created_by="test_user",
                updated_by="test_user",
            ),
        ]
        book1 = self.book_model_factory.build(
            isbn_code="978-0-123456-78-9",
            editor="Fiction Editor",
            authors=[self.stored_author1],
            book_categories=[self.stored_category1],
            book_data=book_data1,
            created_by="test_user",
            updated_by="test_user",
        )

        book_data2 = [
            self.book_data_model_factory.build(
                title="Science Handbook",
                language="en",
                created_by="test_user",
                updated_by="test_user",
            ),
        ]
        book2 = self.book_model_factory.build(
            isbn_code="978-0-987654-32-1",
            editor="Science Editor",
            authors=[self.stored_author2],
            book_categories=[self.stored_category2],
            book_data=book_data2,
            created_by="test_user",
            updated_by="test_user",
        )

        self.stored_book1 = self.book_repository.upsert_book(book1)
        self.stored_book2 = self.book_repository.upsert_book(book2)

        # Create branches
        branch1 = self.branch_model_factory.build(
            name="Main Library",
            created_by="test_user",
            updated_by="test_user",
        )
        branch2 = self.branch_model_factory.build(
            name="Downtown Branch",
            created_by="test_user",
            updated_by="test_user",
        )

        self.stored_branch1 = self.branch_repository.upsert_branch(branch1)
        self.stored_branch2 = self.branch_repository.upsert_branch(branch2)

        # Create physical exemplars
        physical_exemplar1 = PhysicalExemplar(
            available=True,
            room=1,
            floor=2,
            bookshelf=3,
            book_id=self.stored_book1.id,
            branch_id=self.stored_branch1.id,
            created_by="test_user",
            updated_by="test_user",
        )
        physical_exemplar2 = PhysicalExemplar(
            available=False,
            room=2,
            floor=1,
            bookshelf=1,
            book_id=self.stored_book2.id,
            branch_id=self.stored_branch1.id,
            created_by="test_user",
            updated_by="test_user",
        )
        physical_exemplar3 = PhysicalExemplar(
            available=True,
            room=1,
            floor=1,
            bookshelf=2,
            book_id=self.stored_book1.id,
            branch_id=self.stored_branch2.id,
            created_by="test_user",
            updated_by="test_user",
        )

        self.stored_physical_exemplar1 = (
            self.physical_exemplar_repository.upsert_physical_exemplar(
                physical_exemplar1,
            )
        )
        self.stored_physical_exemplar2 = (
            self.physical_exemplar_repository.upsert_physical_exemplar(
                physical_exemplar2,
            )
        )
        self.stored_physical_exemplar3 = (
            self.physical_exemplar_repository.upsert_physical_exemplar(
                physical_exemplar3,
            )
        )

    def test_filter_physical_exemplar_by_branch_with_all_filters(self):
        # Scenario: Filter physical exemplars by branch with all book filters applied

        # When a request is made to filter physical exemplars with all filters
        response = self.client.get(
            f"api/physical_exemplar/branch/{self.stored_branch1.id}",
            params={
                "isbn_code": "978-0-123456-78-9",
                "editor": "Fiction Editor",
                "author_name": "John Doe",
                "book_category_name": "Fiction",
            },
        )

        # Then the response is a 200 status code
        self.assertEqual(response.status_code, 200)
        response_data = response.json()

        # And the response should contain only the matching physical exemplar
        expected_physical_exemplar = json.loads(
            self.stored_physical_exemplar1.model_dump_json(
                exclude_none=True,
                exclude_unset=True,
            ),
        )

        self.assertDictEqual(response_data[0], expected_physical_exemplar)

    def test_filter_physical_exemplar_by_branch_no_filters(self):
        # Scenario: Filter physical exemplars by branch without any book filters

        # When a request is made to filter physical exemplars without book filters
        response = self.client.get(
            f"api/physical_exemplar/branch/{self.stored_branch1.id}",
        )

        # Then the response is a 200 status code
        self.assertEqual(response.status_code, 200)
        response_data = response.json()

        # And the response should contain all physical exemplars for the branch
        expected_physical_exemplars = [
            json.loads(
                self.stored_physical_exemplar1.model_dump_json(
                    exclude_none=True,
                    exclude_unset=True,
                ),
            ),
            json.loads(
                self.stored_physical_exemplar2.model_dump_json(
                    exclude_none=True,
                    exclude_unset=True,
                ),
            ),
        ]

        self.assertEqual(
            sorted(response_data, key=lambda x: x["id"]),
            sorted(expected_physical_exemplars, key=lambda x: x["id"]),
        )

    def test_filter_physical_exemplar_by_branch_no_results(self):
        # Scenario: Filter physical exemplars by branch with filters that match no results

        # When a request is made to filter physical exemplars with non-matching filters
        response = self.client.get(
            f"api/physical_exemplar/branch/{self.stored_branch1.id}",
            params={
                "isbn_code": "978-0-000000-00-0",  # Non-existent ISBN
                "editor": "Non-existent Editor",
            },
        )

        # Then the response is a 200 status code
        self.assertEqual(response.status_code, 200)
        response_data = response.json()

        # And the response should be empty
        self.assertEqual(len(response_data), 0)
