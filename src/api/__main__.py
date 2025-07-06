"""Initialize Uvicorn."""

import os

import uvicorn

from src.infrastructure.settings.config import SystemConfig
from src.infrastructure.settings.environments import Environments


def api() -> None:
    config = SystemConfig()
    """Main funtion to initialize a fastapi application."""
    if config.environment == Environments.LOCAL:
        log_level = "debug"
        reload = True
    else:
        log_level = "info"
        reload = False

    uvicorn.run(
        "src.infrastructure.settings.web_application:app",
        host=config.host,
        port=config.port,
        reload=reload,
        factory=False,
        log_level=log_level,
    )


if __name__ == "__main__":
    if os.getenv("SYSTEM_EXECUTOR") == "api":
        api()
