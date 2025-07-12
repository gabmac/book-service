from typing import List
from uuid import UUID

from sqlalchemy.exc import NoResultFound
from sqlmodel import select

from src.application.exceptions import NotFoundException
from src.application.ports.database.branch import BranchReadRepositoryPort
from src.domain.entities.branch import Branch, BranchFilter
from src.infrastructure.adapters.database.db.session import DatabaseSettings
from src.infrastructure.adapters.database.models.branch import Branch as BranchModel


class BranchReadRepository(BranchReadRepositoryPort):
    def __init__(self, db: DatabaseSettings) -> None:
        self.db = db

    def get_branch_by_filter(self, filter: BranchFilter) -> List[Branch]:
        with self.db.get_session(slave=True) as session:
            statement = select(BranchModel)
            if filter.name:
                statement = statement.where(
                    BranchModel.name.ilike(f"%{filter.name}%"),  # type: ignore
                )
            return [
                Branch.model_validate(branch_model)
                for branch_model in session.exec(statement).all()
            ]

    def get_branch_by_id(self, id: UUID) -> Branch:
        with self.db.get_session(slave=True) as session:
            try:
                branch_model = session.exec(
                    select(BranchModel).where(BranchModel.id == id),
                ).one()
            except NoResultFound:
                raise NotFoundException("Branch not found")
            return Branch.model_validate(branch_model)
