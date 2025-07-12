from contextvars import ContextVar

from fastapi import Response
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from uuid6 import uuid7


class RequestContextsMiddleware(BaseHTTPMiddleware):

    async def dispatch(
        self,
        request: Request,
        call_next: RequestResponseEndpoint,
    ) -> Response:

        self._correlation_id_ctx_var: ContextVar[str] = ContextVar(
            "CID",
            default="",
        )
        correlation_id = (
            str(uuid7())
            if request.headers.get("X-Correlation-ID") is None
            else f'{request.headers.get("X-Correlation-ID")}-{str(uuid7())}'
        )
        correlation_id = self._correlation_id_ctx_var.set(correlation_id)  # type: ignore

        response = await call_next(request)
        response.headers["X-Correlation-ID"] = self._correlation_id_ctx_var.get()
        response.headers["X-Request-ID"] = str(uuid7())

        self._correlation_id_ctx_var.reset(correlation_id)  # type: ignore

        return response
