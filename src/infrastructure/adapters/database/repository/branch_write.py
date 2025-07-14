from sqlmodel import and_, text, update

from src.application.exceptions import OptimisticLockException
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
                statement = (
                    update(BranchModel)
                    .where(
                        and_(
                            BranchModel.id == branch.id,
                            BranchModel.version == branch.version - 1,
                        ),
                    )
                    .values(
                        **branch.model_dump(
                            exclude_none=True,
                            exclude_unset=True,
                            mode="json",
                        )
                    )
                )
                result = session.exec(statement)  # type: ignore
                if result.rowcount == 0:
                    raise OptimisticLockException(
                        f"""Optimistic lock failed for branch {branch.id}.
                        Expected version {branch.version - 1},
                        but data may have been modified by another transaction.""",
                    )
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
