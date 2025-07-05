from typing import Any, Generator
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field, PostgresDsn, AliasChoices

from sqlalchemy import Engine
from sqlmodel import create_engine, SQLModel, Session


class DatabaseSettings(BaseSettings):
    """Database settings."""
    model_config = SettingsConfigDict(env_prefix="DATABASE_")
    host: str = "localhost"
    password: str = "123456"
    port: int = 5432
    user: str = "postgres"
    database: str = "book_service"
    
    engine: Engine | None = None
    
    def get_db_url(self) -> str:
        return f"postgresql+psycopg2://{self.user}:{self.password}@{self.host}:{self.port}" 
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._create_engine()
    
    def _create_engine(self) -> Engine:
        if self.engine is None:
            self.engine = create_engine(self.get_db_url())
        return self.engine
    
    def init_db(self) -> None:
        if self.engine is None:
            raise ValueError("Engine is not initialized")
        SQLModel.metadata.create_all(self.engine)
        
    def get_session(self) -> Generator[Session, Any, Any]:
        if self.engine is None:
            raise ValueError("Engine is not initialized")
        with Session(self.engine) as session:
            yield session
    