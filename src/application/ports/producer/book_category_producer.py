from abc import ABC, abstractmethod

from src.application.ports.producer.base_producer import BaseProducerPort
from src.domain.entities.book_category import BookCategory


class BookCategoryProducerPort(BaseProducerPort, ABC):
    @abstractmethod
    def upsert_book_category(self, book_category: BookCategory) -> None:
        pass
