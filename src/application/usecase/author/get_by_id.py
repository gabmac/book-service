from uuid import UUID

from fastapi import HTTPException

from src.application.dto.author import AuthorResponse
from src.application.exceptions import NotFoundException
from src.application.ports.database.author import AuthorRepositoryPort


class GetAuthorById:
    def __init__(self, author_repository: AuthorRepositoryPort):
        self.author_repository = author_repository

    def execute(self, id: UUID) -> AuthorResponse:
        try:
            author = self.author_repository.get_author_by_id(id)
            return AuthorResponse.model_validate(author)
        except NotFoundException as e:
            raise HTTPException(status_code=404, detail=e.message)
