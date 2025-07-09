from uuid import uuid4

from tests.unit.book.usecase.conftest import BookUseCaseConftest

from src.application.usecase.book.delete_book import DeleteBook
from src.domain.entities.base import DeletionEntity


class TestDeleteBook(BookUseCaseConftest):

    def setUp(self):
        super().setUp()
        self.delete_book = DeleteBook(
            book_repository=self.mock_book_repository,
        )

    def test_execute_successful_deletion(self):
        # Arrange
        book_id = uuid4()
        deletion_entity = DeletionEntity(id=str(book_id))

        # Mock repository response
        self.mock_book_repository.delete_book.return_value = None

        # Act
        result = self.delete_book.execute(deletion_entity)

        # Assert
        self.mock_book_repository.delete_book.assert_called_once_with(str(book_id))
        self.assertIsNone(result)
