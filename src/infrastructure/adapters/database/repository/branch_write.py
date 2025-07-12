from sqlmodel import text

from src.application.ports.database.branch import BranchWriteRepositoryPort
from src.domain.entities.branch import Branch
from src.infrastructure.adapters.database.db.session import DatabaseSettings
from src.infrastructure.adapters.database.models.branch import Branch as BranchModel


class BranchWriteRepository(BranchWriteRepositoryPort):
    def __init__(self, db: DatabaseSettings) -> None:
        self.db = db

    def upsert_branch(self, branch: Branch) -> Branch:
        with self.db.get_session() as session:
            branch_model = session.get(BranchModel, branch.id)
            if branch_model:
                for k, v in branch.model_dump().items():
                    if k == "id":
                        continue
                    setattr(branch_model, k, v)
            else:
                branch_model = BranchModel.model_validate(branch)
                session.add(branch_model)
            session.flush()
            session.commit()
            session.refresh(branch_model)
            # Create partition for this branch
            partition_name = f"physical_exemplar_branch_{branch.id}".replace("-", "_")
            branch_id = str(branch.id)
            sql = f"""
            CREATE TABLE IF NOT EXISTS {partition_name} PARTITION OF physical_exemplar
            FOR VALUES IN ('{branch_id}');
            """
            session.exec(text(sql))  # type: ignore
            session.commit()
            return Branch.model_validate(branch_model)
