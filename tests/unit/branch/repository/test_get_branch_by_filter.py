from tests.unit.branch.repository.conftest import BranchRepositoryConftest

from src.domain.entities.branch import BranchFilter


class TestGetBranchByFilter(BranchRepositoryConftest):

    def test_filter_by_name_found(self):
        # Arrange - Create and save branches with different names
        branch1 = self.branch_model_factory.build(name="Main Branch")
        branch2 = self.branch_model_factory.build(name="Secondary Branch")
        branch3 = self.branch_model_factory.build(name="Main Office")

        self.branch_repository.upsert_branch(branch=branch1)
        self.branch_repository.upsert_branch(branch=branch2)
        self.branch_repository.upsert_branch(branch=branch3)

        # Act - Filter by name containing "Main"
        filter_criteria = BranchFilter(name="Main")
        results = self.branch_repository.get_branch_by_filter(filter=filter_criteria)

        # Assert
        self.assertEqual(
            results.sort(key=lambda x: x.name),
            [branch1, branch3].sort(key=lambda x: x.name),
        )

    def test_filter_by_name_not_found(self):
        # Arrange - Create and save branches with different names
        branch1 = self.branch_model_factory.build(name="Main Branch")
        branch2 = self.branch_model_factory.build(name="Secondary Branch")

        self.branch_repository.upsert_branch(branch=branch1)
        self.branch_repository.upsert_branch(branch=branch2)

        # Act - Filter by name that doesn't exist
        filter_criteria = BranchFilter(name="NonExistentBranch")
        results = self.branch_repository.get_branch_by_filter(filter=filter_criteria)

        # Assert - Should return empty list
        self.assertEqual(results, [])

    def test_no_filter_name_returns_all(self):
        # Arrange - Create and save multiple branches
        branch1 = self.branch_model_factory.build()
        branch2 = self.branch_model_factory.build()

        self.branch_repository.upsert_branch(branch=branch1)
        self.branch_repository.upsert_branch(branch=branch2)

        # Act - Call with filter that has no name
        empty_filter = BranchFilter(name=None)
        results = self.branch_repository.get_branch_by_filter(filter=empty_filter)

        # Assert - Should return all branches
        self.assertEqual(
            results.sort(key=lambda x: x.name),
            [branch1, branch2].sort(key=lambda x: x.name),
        )
