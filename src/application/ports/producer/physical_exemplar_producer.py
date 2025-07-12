from abc import ABC, abstractmethod

from src.application.ports.producer.base_producer import BaseProducerPort
from src.domain.entities.physical_exemplar import PhysicalExemplar


class PhysicalExemplarProducerPort(BaseProducerPort, ABC):
    @abstractmethod
    def upsert_physical_exemplar(self, physical_exemplar: PhysicalExemplar) -> None:
        pass

    @abstractmethod
    def notify_external_physical_exemplar_upsert(
        self,
        physical_exemplar: PhysicalExemplar,
    ) -> None:
        pass
