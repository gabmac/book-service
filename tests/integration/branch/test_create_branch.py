import json

from tests.integration.branch.conftest import BranchViewConfTest

from src.application.dto.branch import ProcessingBranch
from src.domain.entities.branch import Branch, BranchFilter


class TestCreateBranch(BranchViewConfTest):
    def test_create_branch(self):

        # Scenario: Create a branch

        # When a request is made to create a branch
        body = self.branch_upsert_model_factory.build()
        response = self.client.post("api/branch", json=body.model_dump())

        # Then the response is a 202 status code
        self.assertEqual(response.status_code, 202)
        response_body = ProcessingBranch.model_validate_json(
            json.dumps(response.json()),
        )

        # And the message is consumed from the queue
        self.consumer.consume("branch.upsert")
        store_branch = self.branch_repository.get_branch_by_filter(BranchFilter())

        # And the branch is stored in the database
        exclude_fields = {"created_at", "updated_at"}
        self.assertEqual(
            store_branch[0].model_dump(exclude=exclude_fields),
            Branch.model_validate(response_body.branch).model_dump(
                exclude=exclude_fields,
            ),
        )

        self.assertEqual(response_body.message, "Task is processing")
