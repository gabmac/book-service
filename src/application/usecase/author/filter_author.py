from typing import List, Optional

from fastapi import HTTPException

from src.application.dto.author import AuthorResponse
from src.application.exceptions import NotFoundException
from src.application.ports.database.author import AuthorRepositoryPort
from src.domain.entities.author import AuthorFilter


class FilterAuthor:
    def __init__(self, author_repository: AuthorRepositoryPort):
        self.author_repository = author_repository

    def execute(self, filter: Optional[AuthorFilter] = None) -> List[AuthorResponse]:
        try:
            authors = self.author_repository.get_author_by_filter(filter)
            return [AuthorResponse.model_validate(author) for author in authors]
        except NotFoundException as e:
            raise HTTPException(status_code=404, detail=e.message)
