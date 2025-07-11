from uuid import UUID

from tests.unit.physical_exemplar.usecase.conftest import (
    PhysicalExemplarUseCaseConftest,
)
from uuid6 import uuid7

from src.application.exceptions import NotFoundException
from src.application.usecase.physical_exemplar.get_physical_exemplar_by_book_and_branch import (
    GetPhysicalExemplarByBookAndBranch,
)


class TestGetPhysicalExemplarByBookAndBranch(PhysicalExemplarUseCaseConftest):

    def setUp(self):
        super().setUp()
        self.get_physical_exemplar_by_book_and_branch = (
            GetPhysicalExemplarByBookAndBranch(
                repository=self.mock_physical_exemplar_repository,
            )
        )
        self.mock_physical_exemplar_repository.get_physical_exemplar_by_book_and_branch.return_value = (
            None
        )
        self.mock_physical_exemplar_repository.get_physical_exemplar_by_book_and_branch.side_effect = (
            None
        )

    def tearDown(self):
        super().tearDown()
        self.mock_physical_exemplar_repository.get_physical_exemplar_by_book_and_branch.reset_mock()

    def test_execute_successful_get(self):
        # Arrange
        book_id: UUID = uuid7()
        branch_id: UUID = uuid7()
        physical_exemplar = self.physical_exemplar_model_factory.build(
            book_id=book_id,
            branch_id=branch_id,
        )

        # Mock repository response
        self.mock_physical_exemplar_repository.get_physical_exemplar_by_book_and_branch.return_value = (
            physical_exemplar
        )

        # Act
        result = self.get_physical_exemplar_by_book_and_branch.execute(
            book_id=book_id,
            branch_id=branch_id,
        )

        # Assert
        self.mock_physical_exemplar_repository.get_physical_exemplar_by_book_and_branch.assert_called_once_with(
            book_id=book_id,
            branch_id=branch_id,
        )
        self.assertEqual(result, physical_exemplar)

    def test_execute_physical_exemplar_not_found(self):
        # Arrange
        book_id: UUID = uuid7()
        branch_id: UUID = uuid7()

        # Mock repository response - physical exemplar not found
        self.mock_physical_exemplar_repository.get_physical_exemplar_by_book_and_branch.side_effect = NotFoundException(
            "Physical exemplar not found",
        )

        # Act & Assert
        with self.assertRaises(NotFoundException) as context:
            self.get_physical_exemplar_by_book_and_branch.execute(
                book_id=book_id,
                branch_id=branch_id,
            )

        self.assertEqual(str(context.exception), "Physical exemplar not found")
        self.mock_physical_exemplar_repository.get_physical_exemplar_by_book_and_branch.assert_called_once_with(
            book_id=book_id,
            branch_id=branch_id,
        )
