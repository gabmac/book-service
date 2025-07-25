from typing import List

from src.application.ports.database.branch import BranchReadRepositoryPort
from src.domain.entities.branch import Branch, BranchFilter


class FilterBranch:
    def __init__(self, repository: BranchReadRepositoryPort):
        self.repository = repository

    def execute(self, filter: BranchFilter) -> List[Branch]:
        return self.repository.get_branch_by_filter(filter)
