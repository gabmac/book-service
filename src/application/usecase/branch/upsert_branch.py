from src.application.ports.database.branch import BranchWriteRepositoryPort
from src.domain.entities.branch import Branch


class UpsertBranch:
    def __init__(self, repository: BranchWriteRepositoryPort):
        self.repository = repository

    def execute(self, branch: Branch) -> Branch:
        return self.repository.upsert_branch(branch)
