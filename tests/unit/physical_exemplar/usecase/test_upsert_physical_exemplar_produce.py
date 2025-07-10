from tests.unit.physical_exemplar.usecase.conftest import (
    PhysicalExemplarUseCaseConftest,
)

from src.application.exceptions import NotFoundException
from src.application.usecase.physical_exemplar.upsert_physical_exemplar_produce import (
    UpsertPhysicalExemplarProduce,
)


class TestUpsertPhysicalExemplarProduce(PhysicalExemplarUseCaseConftest):

    def setUp(self):
        super().setUp()
        self.upsert_physical_exemplar_produce = UpsertPhysicalExemplarProduce(
            physical_exemplar_producer=self.mock_physical_exemplar_producer,
            repository=self.mock_physical_exemplar_repository,
            book_repository=self.mock_book_repository,
            branch_repository=self.mock_branch_repository,
        )
        self.mock_book_repository.get_book_by_id.return_value = None
        self.mock_book_repository.get_book_by_id.side_effect = None
        self.mock_branch_repository.get_branch_by_id.return_value = None
        self.mock_branch_repository.get_branch_by_id.side_effect = None
        self.mock_physical_exemplar_producer.upsert_physical_exemplar.return_value = (
            None
        )
        self.mock_physical_exemplar_producer.upsert_physical_exemplar.side_effect = None
        self.mock_physical_exemplar_repository.get_physical_exemplar_by_book_and_branch.return_value = (
            None
        )
        self.mock_physical_exemplar_repository.get_physical_exemplar_by_book_and_branch.side_effect = (
            None
        )

    def tearDown(self):
        super().tearDown()
        self.mock_book_repository.get_book_by_id.reset_mock()
        self.mock_branch_repository.get_branch_by_id.reset_mock()
        self.mock_physical_exemplar_producer.upsert_physical_exemplar.reset_mock()
        self.mock_physical_exemplar_repository.get_physical_exemplar_by_book_and_branch.reset_mock()

    def test_execute_book_not_found(self):
        # Arrange

        physical_exemplar = self.physical_exemplar_model_factory.build()

        # Mock repository responses - book not found
        self.mock_book_repository.get_book_by_id.side_effect = NotFoundException(
            "Book not found",
        )

        # Act & Assert
        with self.assertRaises(NotFoundException) as context:
            self.upsert_physical_exemplar_produce.execute(physical_exemplar)

        self.assertEqual(str(context.exception), "Book not found")
        self.mock_book_repository.get_book_by_id.assert_called_once_with(
            id=physical_exemplar.book_id,
        )
        # Branch repository should not be called if book lookup fails
        self.mock_branch_repository.get_branch_by_id.assert_not_called()
        self.mock_physical_exemplar_producer.upsert_physical_exemplar.assert_not_called()

    def test_execute_branch_not_found(self):
        # Arrange

        book = self.book_model_factory.build()
        physical_exemplar = self.physical_exemplar_model_factory.build(
            book_id=book.id,
        )

        # Mock repository responses - book found, branch not found
        self.mock_book_repository.get_book_by_id.return_value = book
        self.mock_branch_repository.get_branch_by_id.side_effect = NotFoundException(
            "Branch not found",
        )

        # Act & Assert
        with self.assertRaises(NotFoundException) as context:
            self.upsert_physical_exemplar_produce.execute(physical_exemplar)

        self.assertEqual(str(context.exception), "Branch not found")
        self.mock_book_repository.get_book_by_id.assert_called_once_with(
            id=physical_exemplar.book_id,
        )
        self.mock_branch_repository.get_branch_by_id.assert_called_once_with(
            id=physical_exemplar.branch_id,
        )
        # Producer should not be called if branch lookup fails
        self.mock_physical_exemplar_producer.upsert_physical_exemplar.assert_not_called()

    def test_execute_success_new(self):
        # Arrange
        book = self.book_model_factory.build()
        branch = self.branch_model_factory.build()
        physical_exemplar = self.physical_exemplar_model_factory.build(
            book_id=book.id,
            branch_id=branch.id,
        )

        # Mock repository responses - book and branch found
        self.mock_book_repository.get_book_by_id.return_value = book
        self.mock_branch_repository.get_branch_by_id.return_value = branch
        self.mock_physical_exemplar_repository.get_physical_exemplar_by_book_and_branch.side_effect = NotFoundException(
            "Physical exemplar not found",
        )

        # Act
        result = self.upsert_physical_exemplar_produce.execute(physical_exemplar)

        # Assert
        self.assertEqual(result, physical_exemplar)
        self.mock_book_repository.get_book_by_id.assert_called_once_with(
            id=physical_exemplar.book_id,
        )
        self.mock_branch_repository.get_branch_by_id.assert_called_once_with(
            id=physical_exemplar.branch_id,
        )
        self.mock_physical_exemplar_producer.upsert_physical_exemplar.assert_called_once_with(
            physical_exemplar,
        )

    def test_update_physical_exemplar(self):
        # Arrange
        book = self.book_model_factory.build()
        branch = self.branch_model_factory.build()
        physical_exemplar = self.physical_exemplar_model_factory.build(
            book_id=book.id,
            branch_id=branch.id,
        )

        # Mock repository responses - book and branch found
        self.mock_book_repository.get_book_by_id.return_value = book
        self.mock_branch_repository.get_branch_by_id.return_value = branch
        self.mock_physical_exemplar_repository.get_physical_exemplar_by_book_and_branch.return_value = (
            physical_exemplar
        )

        # Act
        result = self.upsert_physical_exemplar_produce.execute(physical_exemplar)

        # Assert
        self.assertEqual(result, physical_exemplar)
        self.mock_book_repository.get_book_by_id.assert_called_once_with(
            id=physical_exemplar.book_id,
        )
        self.mock_branch_repository.get_branch_by_id.assert_called_once_with(
            id=physical_exemplar.branch_id,
        )
        self.mock_physical_exemplar_producer.upsert_physical_exemplar.assert_called_once_with(
            physical_exemplar,
        )
