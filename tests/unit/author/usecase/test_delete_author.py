from uuid import uuid4

from tests.unit.author.usecase.conftest import AuthorUseCaseConftest

from src.application.usecase.author.delete_author import DeleteAuthor
from src.domain.entities.base import DeletionEntity


class TestDeleteAuthor(AuthorUseCaseConftest):

    def setUp(self):
        super().setUp()
        self.delete_author = DeleteAuthor(
            author_repository=self.mock_author_repository,
        )
        self.mock_author_repository.delete_author.return_value = None
        self.mock_author_repository.delete_author.side_effect = None

    def tearDown(self):
        super().tearDown()
        self.mock_author_repository.delete_author.reset_mock()

    def test_execute_successful_delete(self):
        # Arrange
        author_id = uuid4()
        deletion_entity = DeletionEntity(id=str(author_id))

        # Act
        result = self.delete_author.execute(deletion_entity)

        # Assert
        self.mock_author_repository.delete_author.assert_called_once_with(
            str(author_id),
        )
        self.assertIsNone(result)
