from uuid import uuid4

from tests.unit.physical_exemplar.usecase.conftest import (
    PhysicalExemplarUseCaseConftest,
)

from src.application.usecase.physical_exemplar.filter_physical_exemplar_by_branch import (
    FilterPhysicalExemplarByBranch,
)
from src.domain.entities.book import BookFilter


class TestFilterPhysicalExemplarByBranch(PhysicalExemplarUseCaseConftest):

    def setUp(self):
        super().setUp()
        self.filter_physical_exemplar_by_branch = FilterPhysicalExemplarByBranch(
            physical_exemplar_repository=self.mock_physical_exemplar_repository,
        )
        self.mock_physical_exemplar_repository.filter_by_branch_and_book_filter.return_value = (
            None
        )
        self.mock_physical_exemplar_repository.filter_by_branch_and_book_filter.side_effect = (
            None
        )

    def tearDown(self):
        super().tearDown()
        self.mock_physical_exemplar_repository.filter_by_branch_and_book_filter.reset_mock()

    def test_execute_with_filter(self):
        branch_id = uuid4()
        physical_exemplar1 = self.physical_exemplar_model_factory.build()
        physical_exemplar2 = self.physical_exemplar_model_factory.build()
        physical_exemplars = [physical_exemplar1, physical_exemplar2]

        book_filter = BookFilter(isbn_code="123456789")

        # Mock repository response
        self.mock_physical_exemplar_repository.filter_by_branch_and_book_filter.return_value = (
            physical_exemplars
        )

        # Act
        result = self.filter_physical_exemplar_by_branch.execute(
            branch_id=branch_id,
            book_filter=book_filter,
        )

        # Assert
        self.mock_physical_exemplar_repository.filter_by_branch_and_book_filter.assert_called_once_with(
            branch_id=branch_id,
            book_filter=book_filter,
        )
        self.assertEqual(result, physical_exemplars)

    def test_execute_empty_result(self):
        # Arrange
        branch_id = uuid4()
        book_filter = BookFilter(isbn_code="Non-existent Book")

        # Mock repository response - no physical exemplars found
        self.mock_physical_exemplar_repository.filter_by_branch_and_book_filter.return_value = (
            []
        )

        # Act
        result = self.filter_physical_exemplar_by_branch.execute(
            branch_id=branch_id,
            book_filter=book_filter,
        )

        # Assert
        self.mock_physical_exemplar_repository.filter_by_branch_and_book_filter.assert_called_once_with(
            branch_id=branch_id,
            book_filter=book_filter,
        )
        self.assertEqual(result, [])
