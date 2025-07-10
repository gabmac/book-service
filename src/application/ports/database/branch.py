from abc import ABC, abstractmethod
from typing import List
from uuid import UUID

from src.domain.entities.branch import Branch, BranchFilter


class BranchRepositoryPort(ABC):
    @abstractmethod
    def get_branch_by_filter(self, filter: BranchFilter) -> List[Branch]:
        pass

    @abstractmethod
    def upsert_branch(self, branch: Branch) -> Branch:
        pass

    @abstractmethod
    def get_branch_by_id(self, id: UUID) -> Branch:
        pass
