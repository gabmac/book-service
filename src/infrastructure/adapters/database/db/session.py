from contextlib import contextmanager
from typing import Generator

from sqlalchemy import Engine
from sqlmodel import Session, create_engine

from src.infrastructure.adapters.database.models.base_model import Base


class DatabaseSettings:
    """Database settings."""

    _instance = None
    host: str = ""
    password: str = ""
    port: int = 0
    user: str = ""
    database: str = ""

    engine: Engine | None = None

    def __new__(cls, host: str, password: str, port: int, user: str):  # type: ignore
        if cls._instance is None:
            cls.host = host
            cls.password = password
            cls.port = port
            cls.user = user
            cls._create_engine()
            cls._instance = cls
        return cls._instance

    @classmethod
    def get_db_url(cls) -> str:
        return f"postgresql+psycopg2://{cls.user}:{cls.password}@{cls.host}:{cls.port}"

    @classmethod
    def _create_engine(cls) -> Engine:
        if cls.engine is None:
            cls.engine = create_engine(cls.get_db_url(), echo=True)
        return cls.engine

    @classmethod
    def init_db(cls) -> None:
        if cls.engine is None:
            raise ValueError("Engine is not initialized")
        Base.metadata.create_all(cls.engine)

    @classmethod
    @contextmanager
    def get_session(cls) -> Generator[Session, None, None]:
        if cls.engine is None:
            raise ValueError("Engine is not initialized")
        with Session(cls.engine, autoflush=True) as session:
            try:
                yield session
                session.commit()
            except Exception as e:
                session.rollback()
                raise e
            finally:
                session.close()
