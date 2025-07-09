from sqlmodel import text
from tests.conftest import BaseRepositoryConfTest
from tests.unit.author.conftest import BaseAuthorConfTest


class AuthorRepositoryConftest(BaseAuthorConfTest, BaseRepositoryConfTest):
    def setUp(self):
        super().setUp()
        with self.db.get_session() as session:
            session.exec(text("DELETE FROM author"))  # type: ignore
            session.commit()
