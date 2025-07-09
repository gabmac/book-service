from tests.unit.branch.usecase.conftest import BranchUseCaseConftest

from src.application.usecase.branch.upsert_branch_produce import UpsertBranchProduce


class TestUpsertBranchProduce(BranchUseCaseConftest):

    def setUp(self):
        super().setUp()
        self.upsert_branch_produce = UpsertBranchProduce(
            branch_producer=self.mock_branch_producer,
            repository=self.mock_branch_repository,
        )
        self.mock_branch_producer.upsert_branch.return_value = None
        self.mock_branch_producer.upsert_branch.side_effect = None

    def tearDown(self):
        super().tearDown()
        self.mock_branch_producer.upsert_branch.reset_mock()

    def test_execute_successful_upsert(self):
        # Arrange
        branch = self.branch_model_factory.build()

        # Act
        result = self.upsert_branch_produce.execute(branch)

        # Assert
        self.mock_branch_producer.upsert_branch.assert_called_once_with(branch)
        self.assertEqual(result, branch)
