from tests.unit.author.usecase.conftest import AuthorUseCaseConftest

from src.application.usecase.author.update_author_produce import UpdateAuthorProduce


class TestUpdateAuthorProduce(AuthorUseCaseConftest):

    def setUp(self):
        super().setUp()
        self.update_author_produce = UpdateAuthorProduce(
            producer=self.mock_author_producer,
            author_read_repository=self.mock_author_read_repository,
        )
        self.mock_author_producer.upsert_author.return_value = None
        self.mock_author_producer.upsert_author.side_effect = None

    def tearDown(self):
        super().tearDown()
        self.mock_author_producer.upsert_author.reset_mock()
        self.mock_author_read_repository.get_author_by_id.reset_mock()

    async def test_execute_successful_update(self):
        # Arrange
        author_payload = self.author_model_factory.build()
        existing_author = self.author_model_factory.build(
            id=author_payload.id,
            created_at=author_payload.created_at,
            created_by=author_payload.created_by,
        )

        # Mock repository response - existing author found
        self.mock_author_read_repository.get_author_by_id.return_value = existing_author

        # Act
        result = await self.update_author_produce.execute(author_payload)

        # Assert
        self.mock_author_read_repository.get_author_by_id.assert_called_once_with(
            author_payload.id,
        )
        self.mock_author_producer.upsert_author.assert_called_once_with(author_payload)
        self.assertEqual(result, author_payload)
        # Verify that created_at and created_by are preserved from existing author
        self.assertEqual(result.created_at, existing_author.created_at)
        self.assertEqual(result.created_by, existing_author.created_by)

    async def test_execute_author_create(self):
        # Arrange
        author_payload = self.author_model_factory.build()

        # Mock repository response - existing author found
        self.mock_author_read_repository.get_author_by_id.return_value = None

        # Act
        result = await self.update_author_produce.execute(author_payload)

        # Assert
        self.mock_author_read_repository.get_author_by_id.assert_called_once_with(
            author_payload.id,
        )
        self.mock_author_producer.upsert_author.assert_called_once_with(author_payload)
        self.assertEqual(result, author_payload)
