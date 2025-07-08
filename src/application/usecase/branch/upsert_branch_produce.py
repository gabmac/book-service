from src.application.ports.database.branch import BranchRepositoryPort
from src.application.ports.producer.branch_producer import BranchProducerPort
from src.domain.entities.branch import Branch


class UpsertBranchProduce:
    def __init__(
        self,
        branch_producer: BranchProducerPort,
        repository: BranchRepositoryPort,
    ):
        self.branch_producer = branch_producer
        self.repository = repository

    def execute(self, branch: Branch) -> Branch:
        # Optionally check for existing branch by name, update if exists
        self.branch_producer.upsert_branch(branch)
        return branch
