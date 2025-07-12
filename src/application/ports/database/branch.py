from abc import ABC, abstractmethod
from typing import List
from uuid import UUID

from src.domain.entities.branch import Branch, BranchFilter


class BranchReadRepositoryPort(ABC):
    @abstractmethod
    def get_branch_by_filter(self, filter: BranchFilter) -> List[Branch]:
        pass

    @abstractmethod
    def get_branch_by_id(self, id: UUID) -> Branch:
        pass


class BranchWriteRepositoryPort(ABC):
    @abstractmethod
    def upsert_branch(self, branch: Branch) -> Branch:
        pass
