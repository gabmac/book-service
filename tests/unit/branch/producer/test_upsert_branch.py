from tests.unit.branch.producer.conftest import BranchProducerConftest

from src.application.dto.producer import Message


class TestUpsertBranch(BranchProducerConftest):

    def test_upsert_branch(self):
        # Arrange
        branch = self.branch_model_factory.build()

        # Act
        self.branch_producer.upsert_branch(branch=branch)

        # Assert
        self.mock_producer.publish.assert_called_once_with(
            message=Message(
                queue_name="branch.upsert",
                message=branch.model_dump_json(),
            ),
        )
