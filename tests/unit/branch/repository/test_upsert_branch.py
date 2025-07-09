from tests.unit.branch.repository.conftest import BranchRepositoryConftest


class TestUpsertBranch(BranchRepositoryConftest):

    def test_new_branch(self):
        # Arrange
        branch = self.branch_model_factory.build()

        # Act
        result = self.branch_repository.upsert_branch(branch=branch)

        # Assert
        self.assertEqual(result, branch)

    def test_update_branch(self):
        # Arrange - Create and save a branch first
        branch = self.branch_model_factory.build()
        self.branch_repository.upsert_branch(branch=branch)

        # Act - Update the branch name
        branch.name = "Updated Branch"
        result = self.branch_repository.upsert_branch(branch=branch)

        # Assert
        self.assertEqual(result, branch)
