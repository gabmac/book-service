from tests.unit.author.usecase.conftest import AuthorUseCaseConftest

from src.application.usecase.author.create_author import CreateAuthorProduce


class TestCreateAuthorProduce(AuthorUseCaseConftest):

    def setUp(self):
        super().setUp()
        self.create_author_produce = CreateAuthorProduce(
            producer=self.mock_author_producer,
        )
        self.mock_author_producer.upsert_author.return_value = None
        self.mock_author_producer.upsert_author.side_effect = None

    def tearDown(self):
        super().tearDown()
        self.mock_author_producer.upsert_author.reset_mock()

    async def test_execute_successful_create(self):
        # Arrange
        author_payload = self.author_model_factory.build()

        # Act
        result = await self.create_author_produce.execute(author_payload)

        # Assert
        self.mock_author_producer.upsert_author.assert_called_once()
        self.assertEqual(result, author_payload)
