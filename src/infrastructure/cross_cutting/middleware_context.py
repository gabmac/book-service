from contextvars import ContextVar
from uuid import uuid4

from fastapi import Response
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request


class RequestContextsMiddleware(BaseHTTPMiddleware):
    CORRELATION_ID_CTX_KEY = "correlation_id"
    REQUEST_ID_CTX_KEY = "request_id"

    _correlation_id_ctx_var: ContextVar[str] = ContextVar(
        CORRELATION_ID_CTX_KEY,
        default="",
    )
    _request_id_ctx_var: ContextVar[str] = ContextVar(REQUEST_ID_CTX_KEY, default="")

    async def dispatch(
        self,
        request: Request,
        call_next: RequestResponseEndpoint,
    ) -> Response:
        correlation_id = (
            str(uuid4())
            if request.headers.get("X-Correlation-ID") is None
            else f'{request.headers.get("X-Correlation-ID")}-{str(uuid4())}'
        )
        correlation_id = self._correlation_id_ctx_var.set(correlation_id)  # type: ignore
        request_id = self._request_id_ctx_var.set(str(uuid4()))

        response = await call_next(request)
        response.headers["X-Correlation-ID"] = self._correlation_id_ctx_var.get()
        response.headers["X-Request-ID"] = self._request_id_ctx_var.get()

        self._correlation_id_ctx_var.reset(correlation_id)  # type: ignore
        self._request_id_ctx_var.reset(request_id)

        return response
