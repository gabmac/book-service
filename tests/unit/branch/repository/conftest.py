from sqlmodel import text
from tests.conftest import BaseRepositoryConfTest
from tests.unit.branch.conftest import BaseBranchConfTest


class BranchRepositoryConftest(BaseBranchConfTest, BaseRepositoryConfTest):
    def setUp(self):
        super().setUp()
        with self.db.get_session() as session:
            session.exec(text("DELETE FROM branch"))  # type: ignore
            session.commit()
