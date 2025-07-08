from src.application.dto.producer import Message
from src.application.ports.producer.branch_producer import BranchProducerPort
from src.domain.entities.branch import Branch
from src.infrastructure.adapters.entrypoints.producer import Producer


class BranchProducerAdapter(BranchProducerPort):
    def __init__(self, producer: Producer):
        self.producer = producer

    def upsert_branch(self, branch: Branch) -> None:
        self.producer.publish(
            message=Message(
                queue_name="branch.upsert",
                message=branch.model_dump_json(),
            ),
        )
