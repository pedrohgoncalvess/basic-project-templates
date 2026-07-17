"""
Synchronous PostgreSQL Database Connection Module with SQLAlchemy

Environment Variables Required:
    DB_HOST, DB_PORT, DB_USER, DB_PASSWORD, DB_NAME
"""
from contextlib import contextmanager
from typing import Iterator

from sqlalchemy import create_engine, text
from sqlalchemy.engine import URL, Engine
from sqlalchemy.orm import Session, sessionmaker

from log import logger
from utils import get_env_var


class DatabaseConnection:
    _engine: Engine | None = None
    _session_maker: sessionmaker[Session] | None = None

    @classmethod
    def _build_url(cls) -> URL:
        return URL.create(
            "postgresql+psycopg2",
            username=get_env_var("DB_USER"),
            password=get_env_var("DB_PASSWORD"),
            host=get_env_var("DB_HOST"),
            port=int(get_env_var("DB_PORT")),
            database=get_env_var("DB_NAME"),
        )

    @classmethod
    def get_engine(cls) -> Engine:
        """Singleton engine — pool lives for the whole process."""
        if cls._engine is None:
            cls._engine = create_engine(
                cls._build_url(),
                echo=False,
                pool_pre_ping=True,
                pool_recycle=1800,
            )
            cls._session_maker = sessionmaker(
                bind=cls._engine,
                class_=Session,
                expire_on_commit=False,
            )
        return cls._engine

    @classmethod
    @contextmanager
    def session(cls) -> Iterator[Session]:
        """
        Per-operation session with commit/rollback/close handled.

        Usage:
            with DatabaseConnection.session() as session:
                result = session.execute(text("SELECT 1"))
        """
        cls.get_engine()
        with cls._session_maker() as session:
            try:
                yield session
                session.commit()
            except Exception as error:
                session.rollback()
                logger.error("Database", f"Session error, rolled back: {error}")
                raise

    @classmethod
    def healthcheck(cls) -> bool:
        try:
            with cls.session() as session:
                session.execute(text("SELECT 1"))
            return True
        except Exception:
            return False

    @classmethod
    def shutdown(cls):
        """Call once on app shutdown, not per operation."""
        if cls._engine is not None:
            logger.info("Database", "Connection", "Disposing engine")
            cls._engine.dispose()
            cls._engine = None
            cls._session_maker = None