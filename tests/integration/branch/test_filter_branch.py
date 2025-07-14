import json

from tests.integration.branch.conftest import BranchViewConfTest


class TestFilterBranch(BranchViewConfTest):

    def setUp(self):
        super().setUp()
        branch1 = self.branch_model_factory.build(
            name="Main Library",
            created_by="test_user",
            updated_by="test_user",
        )
        branch2 = self.branch_model_factory.build(
            name="Downtown Branch",
            created_by="test_user",
            updated_by="test_user",
        )
        branch3 = self.branch_model_factory.build(
            name="University Library",
            created_by="test_user",
            updated_by="test_user",
        )

        # Store branches in database
        self.stored_branch1 = self.branch_write_repository.upsert_branch(branch1)
        self.stored_branch2 = self.branch_write_repository.upsert_branch(branch2)
        self.stored_branch3 = self.branch_write_repository.upsert_branch(branch3)

    def test_filter_branch_with_filter(self):

        # Scenario: Filter branches by filter

        # Given branches are stored in the database

        # When a request is made to filter branches by name
        response = self.client.get("api/branch", params={"name": "Library"})

        # Then the response is a 200 status code
        self.assertEqual(response.status_code, 200)
        response_data = response.json()

        # And the response should be list all branches that matches the filter
        expected_branches = [self.stored_branch1, self.stored_branch3]
        branch_expected = [
            json.loads(expected_branch.model_dump_json())
            for expected_branch in expected_branches
        ]

        self.assertEqual(
            sorted(branch_expected, key=lambda x: x["id"]),
            sorted(response_data, key=lambda x: x["id"]),
        )

    def test_filter_branch_no_results(self):

        # Scenario: Filter branches by filter

        # Given branches are stored in the database

        # When a request is made to filter branches by name that doesn't exist
        branch = self.branch_model_factory.build()
        self.branch_write_repository.upsert_branch(branch)

        response = self.client.get("api/branch", params={"name": "NonExistent"})

        # Then the response is a 200 status code
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertEqual(len(response_data), 0)

    def test_filter_branch_no_filter(self):

        # Scenario: Filter branches by filter

        # Given branches are stored in the database

        # When a request is made to filter branches by name
        response = self.client.get("api/branch")

        # Then the response is a 200 status code
        self.assertEqual(response.status_code, 200)
        response_data = response.json()

        # And the response should be list all branches
        expected_branches = [
            self.stored_branch1,
            self.stored_branch2,
            self.stored_branch3,
        ]
        branch_expected = [
            json.loads(expected_branch.model_dump_json())
            for expected_branch in expected_branches
        ]

        self.assertEqual(
            sorted(branch_expected, key=lambda x: x["id"]),
            sorted(response_data, key=lambda x: x["id"]),
        )
