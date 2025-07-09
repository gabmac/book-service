from sqlmodel import text
from tests.conftest import BaseRepositoryConfTest
from tests.unit.branch.conftest import BaseBranchConfTest


class BranchRepositoryConftest(BaseBranchConfTest, BaseRepositoryConfTest):
    def tearDown(self):
        super().tearDown()
        with self.db.get_session() as session:
            session.exec(text("DELETE FROM branch"))  # type: ignore
            session.commit()
