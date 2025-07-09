from tests.unit.branch.usecase.conftest import BranchUseCaseConftest

from src.application.usecase.branch.filter_branch import FilterBranch
from src.domain.entities.branch import BranchFilter


class TestFilterBranch(BranchUseCaseConftest):

    def setUp(self):
        super().setUp()
        self.filter_branch = FilterBranch(
            repository=self.mock_branch_repository,
        )
        self.mock_branch_repository.get_branch_by_filter.return_value = None
        self.mock_branch_repository.get_branch_by_filter.side_effect = None

    def tearDown(self):
        super().tearDown()
        self.mock_branch_repository.get_branch_by_filter.reset_mock()

    def test_execute_with_filter(self):
        # Arrange
        branch1 = self.branch_model_factory.build(name="Main Library")
        branch2 = self.branch_model_factory.build(name="Main Branch")
        branches = [branch1, branch2]

        filter_obj = BranchFilter(name="Main")

        # Mock repository response
        self.mock_branch_repository.get_branch_by_filter.return_value = branches

        # Act
        result = self.filter_branch.execute(filter_obj)

        # Assert
        self.mock_branch_repository.get_branch_by_filter.assert_called_once_with(
            filter_obj,
        )
        self.assertEqual(result, branches)

    def test_execute_empty_result(self):
        # Arrange
        filter_obj = BranchFilter(name="Non-existent Branch")

        # Mock repository response - no branches found
        self.mock_branch_repository.get_branch_by_filter.return_value = []

        # Act
        result = self.filter_branch.execute(filter_obj)

        # Assert
        self.mock_branch_repository.get_branch_by_filter.assert_called_once_with(
            filter_obj,
        )
        self.assertEqual(result, [])
