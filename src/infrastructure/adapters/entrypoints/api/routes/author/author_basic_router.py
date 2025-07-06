from abc import ABC
from typing import Any

from fastapi import APIRouter

from src.application.ports.route.basic_router import BaseRouterView


class AuthorBasicRouter(BaseRouterView, ABC):
    router: APIRouter | None = None  # type: ignore

    def __init__(
        self,
        use_case: Any,
        name: str = "author",
    ) -> None:
        super().__init__(name, use_case)
