from tests.conftest import BaseRepositoryConfTest
from tests.unit.book.conftest import BaseBookConfTest


class BookRepositoryConftest(BaseBookConfTest, BaseRepositoryConfTest):
    pass
