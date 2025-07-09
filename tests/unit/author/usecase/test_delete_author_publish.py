from uuid import uuid4

from tests.unit.author.usecase.conftest import AuthorUseCaseConftest

from src.application.usecase.author.delete_author_publish import DeleteAuthorPublish


class TestDeleteAuthorPublish(AuthorUseCaseConftest):

    def setUp(self):
        super().setUp()
        self.delete_author_publish = DeleteAuthorPublish(
            author_producer=self.mock_author_producer,
        )
        self.mock_author_producer.delete_author.return_value = None
        self.mock_author_producer.delete_author.side_effect = None

    def tearDown(self):
        super().tearDown()
        self.mock_author_producer.delete_author.reset_mock()

    def test_execute_successful_delete(self):
        # Arrange
        author_id = uuid4()

        # Act
        result = self.delete_author_publish.execute(author_id)

        # Assert
        self.mock_author_producer.delete_author.assert_called_once_with(author_id)
        self.assertIsNone(result)
