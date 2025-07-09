from tests.unit.author.usecase.conftest import AuthorUseCaseConftest

from src.application.usecase.author.update_author_produce import UpdateAuthorProduce


class TestUpdateAuthorProduce(AuthorUseCaseConftest):

    def setUp(self):
        super().setUp()
        self.update_author_produce = UpdateAuthorProduce(
            producer=self.mock_author_producer,
        )
        self.mock_author_producer.upsert_author.return_value = None
        self.mock_author_producer.upsert_author.side_effect = None

    def tearDown(self):
        super().tearDown()
        self.mock_author_producer.upsert_author.reset_mock()

    async def test_execute_successful_update(self):
        # Arrange
        author_payload = self.author_model_factory.build()

        # Act
        result = await self.update_author_produce.execute(author_payload)

        # Assert
        self.mock_author_producer.upsert_author.assert_called_once()
        self.assertEqual(result, author_payload)
