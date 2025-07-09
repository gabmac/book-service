from contextlib import contextmanager
from typing import Generator

from sqlalchemy import Engine
from sqlmodel import Session, create_engine, text

from src.infrastructure.adapters.database.models.base_model import Base


class DatabaseSettings:
    """Database settings."""

    _instance = None
    host: str = ""
    password: str = ""
    port: int = 0
    user: str = ""
    database: str = ""
    slave_host: str = ""
    slave_port: int = 0

    engine: Engine | None = None
    engine_slave: Engine | None = None

    def __new__(cls, host: str, password: str, port: int, user: str, slave_host: str, slave_port: int):  # type: ignore
        if cls._instance is None:
            cls.host = host
            cls.password = password
            cls.port = port
            cls.user = user
            cls.slave_host = slave_host
            cls.slave_port = slave_port
            cls._create_engine()
            cls._pg_trgm_install()
            cls._instance = cls
        return cls._instance

    @classmethod
    def get_db_url(cls) -> str:
        return f"postgresql+psycopg2://{cls.user}:{cls.password}@{cls.host}:{cls.port}"

    @classmethod
    def get_db_url_slave(cls) -> str:
        return f"postgresql+psycopg2://{cls.user}:{cls.password}@{cls.slave_host}:{cls.slave_port}"

    @classmethod
    def _create_engine(cls) -> Engine:
        if cls.engine is None:
            cls.engine = create_engine(cls.get_db_url(), echo=True)
            cls.engine_slave = create_engine(cls.get_db_url_slave(), echo=True)
        return cls.engine

    @classmethod
    def init_db(cls) -> None:
        if cls.engine is None:
            raise ValueError("Engine is not initialized")
        sql = """
            CREATE TABLE physical_exemplar (
            id UUID NOT NULL,
            branch_id UUID NOT NULL,
            created_at TIMESTAMPTZ NOT NULL,
            created_by TEXT NOT NULL,
            updated_at TIMESTAMPTZ NOT NULL,
            updated_by TEXT NOT NULL,
            available BOOLEAN NOT NULL,
            room INTEGER NOT NULL,
            floor INTEGER NOT NULL,
            bookshelf INTEGER NOT NULL,
            book_id UUID,

            PRIMARY KEY (id, branch_id),
            CONSTRAINT fk_book FOREIGN KEY (book_id) REFERENCES book(id),
            CONSTRAINT fk_branch FOREIGN KEY (branch_id) REFERENCES branch(id)
        ) PARTITION BY LIST (branch_id);
        """
        session = Session(cls.engine)
        session.exec(text(sql))  # type: ignore
        session.commit()
        session.close()
        Base.metadata.create_all(cls.engine)

    @classmethod
    def _pg_trgm_install(cls) -> None:
        session = Session(cls.engine)
        session.exec(text("CREATE EXTENSION IF NOT EXISTS pg_trgm;"))  # type: ignore
        session.commit()
        session.close()

    @classmethod
    @contextmanager
    def get_session(cls, slave: bool = False) -> Generator[Session, None, None]:
        if cls.engine is None:
            raise ValueError("Engine is not initialized")
        if cls.engine_slave is None:
            raise ValueError("Engine slave is not initialized")
        engine = cls.engine_slave if slave else cls.engine
        with Session(engine, autoflush=True) as session:
            try:
                yield session
                session.commit()
            except Exception as e:
                session.rollback()
                raise e
            finally:
                session.close()
