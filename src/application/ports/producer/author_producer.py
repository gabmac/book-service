from abc import ABC, abstractmethod
from uuid import UUID

from src.application.ports.producer.base_producer import BaseProducerPort
from src.domain.entities.author import Author


class AuthorProducerPort(BaseProducerPort, ABC):
    @abstractmethod
    def upsert_author(self, author: Author) -> None:
        pass

    @abstractmethod
    def delete_author(self, id: UUID) -> None:
        pass

    @abstractmethod
    def notify_external_author_upsert(self, author: Author) -> None:
        pass

    @abstractmethod
    def notify_external_author_deletion(self, id: UUID) -> None:
        pass
