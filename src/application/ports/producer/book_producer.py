from abc import ABC, abstractmethod
from uuid import UUID

from src.application.ports.producer.base_producer import BaseProducerPort
from src.domain.entities.book import Book


class BookProducerPort(BaseProducerPort, ABC):
    @abstractmethod
    def upsert_book(self, book: Book) -> None:
        pass

    @abstractmethod
    def delete_book(self, id: UUID) -> None:
        pass
