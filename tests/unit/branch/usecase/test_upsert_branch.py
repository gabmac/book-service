from tests.unit.branch.usecase.conftest import BranchUseCaseConftest

from src.application.usecase.branch.upsert_branch import UpsertBranch


class TestUpsertBranch(BranchUseCaseConftest):

    def setUp(self):
        super().setUp()
        self.upsert_branch = UpsertBranch(
            repository=self.mock_branch_repository,
        )
        self.mock_branch_repository.upsert_branch.return_value = None
        self.mock_branch_repository.upsert_branch.side_effect = None

    def tearDown(self):
        super().tearDown()
        self.mock_branch_repository.upsert_branch.reset_mock()

    def test_execute_successful_upsert(self):
        # Arrange
        branch = self.branch_model_factory.build()

        # Mock repository response
        self.mock_branch_repository.upsert_branch.return_value = branch

        # Act
        result = self.upsert_branch.execute(branch)

        # Assert
        self.mock_branch_repository.upsert_branch.assert_called_once_with(branch)
        self.assertEqual(result, branch)
