from abc import ABC, abstractmethod

from src.application.ports.producer.base_producer import BaseProducerPort
from src.domain.entities.branch import Branch


class BranchProducerPort(BaseProducerPort, ABC):
    @abstractmethod
    def upsert_branch(self, branch: Branch) -> None:
        pass
