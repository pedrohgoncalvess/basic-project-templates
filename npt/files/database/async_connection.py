"""
Asynchronous PostgreSQL Database Connection Module with SQLAlchemy

Environment Variables Required:
    DB_HOST, DB_PORT, DB_USER, DB_PASSWORD, DB_NAME

Note:
    The Windows event loop policy should be set in the app entrypoint
    (main.py), not here:

        if sys.platform == "win32":
            asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
"""
from contextlib import asynccontextmanager
from typing import AsyncIterator

from sqlalchemy import text
from sqlalchemy.engine import URL
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from log import logger
from utils import get_env_var


class DatabaseConnection:
    _engine: AsyncEngine | None = None
    _session_maker: async_sessionmaker[AsyncSession] | None = None

    @classmethod
    def _build_url(cls) -> URL:
        return URL.create(
            "postgresql+asyncpg",
            username=get_env_var("DB_USER"),
            password=get_env_var("DB_PASSWORD"),
            host=get_env_var("DB_HOST"),
            port=int(get_env_var("DB_PORT")),
            database=get_env_var("DB_NAME"),
        )

    @classmethod
    def get_engine(cls) -> AsyncEngine:
        """Singleton engine — pool lives for the whole process."""
        if cls._engine is None:
            cls._engine = create_async_engine(
                cls._build_url(),
                echo=False,
                pool_pre_ping=True,
                pool_recycle=1800,
            )
            cls._session_maker = async_sessionmaker(
                bind=cls._engine,
                class_=AsyncSession,
                expire_on_commit=False,
            )
        return cls._engine

    @classmethod
    @asynccontextmanager
    async def session(cls) -> AsyncIterator[AsyncSession]:
        """
        Per-operation session with commit/rollback/close handled.

        Usage:
            async with DatabaseConnection.session() as session:
                result = await session.execute(text("SELECT 1"))
        """
        cls.get_engine()
        async with cls._session_maker() as session:
            try:
                yield session
                await session.commit()
            except Exception as error:
                await session.rollback()
                await logger.error("Database", f"Session error, rolled back: {error}")
                raise

    @classmethod
    async def healthcheck(cls) -> bool:
        try:
            async with cls.session() as session:
                await session.execute(text("SELECT 1"))
            return True
        except Exception:
            return False

    @classmethod
    async def shutdown(cls):
        """Call once on app shutdown, not per operation."""
        if cls._engine is not None:
            await logger.info("Database", "Connection", "Disposing engine")
            await cls._engine.dispose()
            cls._engine = None
            cls._session_maker = None