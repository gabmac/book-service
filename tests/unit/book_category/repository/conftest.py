from sqlmodel import text
from tests.conftest import BaseRepositoryConfTest
from tests.unit.book_category.conftest import BaseBookCategoryConfTest


class BookCategoryRepositoryConftest(BaseBookCategoryConfTest, BaseRepositoryConfTest):
    def tearDown(self):
        super().tearDown()
        with self.db.get_session() as session:
            session.exec(text("DELETE FROM book_category"))  # type: ignore
            session.commit()
