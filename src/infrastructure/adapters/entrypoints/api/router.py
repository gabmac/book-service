from fastapi import APIRouter

from src.infrastructure.adapters.entrypoints.api.monitoring import (
    router as monitoring_router,
)

api_router = APIRouter(prefix="/api")
api_router.include_router(monitoring_router)
