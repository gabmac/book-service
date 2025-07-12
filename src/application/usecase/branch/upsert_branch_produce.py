from src.application.ports.database.branch import BranchReadRepositoryPort
from src.application.ports.producer.branch_producer import BranchProducerPort
from src.domain.entities.branch import Branch


class UpsertBranchProduce:
    def __init__(
        self,
        branch_producer: BranchProducerPort,
        repository: BranchReadRepositoryPort,
    ):
        self.branch_producer = branch_producer
        self.repository = repository

    def execute(self, branch: Branch) -> Branch:
        self.branch_producer.upsert_branch(branch)
        return branch
