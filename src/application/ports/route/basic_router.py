from abc import ABC, abstractmethod

from fastapi import APIRouter


class BaseRouterView(ABC):
    router: APIRouter

    def __init__(self, name: str, use_case: object) -> None:
        self.use_case = use_case
        self.name = name
        if self.router is None:
            self.router = APIRouter(
                prefix=f"/{name}",
                tags=[name],
            )
        self._add_to_router()

    @abstractmethod
    def _add_to_router(self) -> None:
        """
        Add to view to router
        """
