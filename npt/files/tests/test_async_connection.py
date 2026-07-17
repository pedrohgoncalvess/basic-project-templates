"""
Tests for database.async_connection.DatabaseConnection.

Unit tests mock the SQLAlchemy async engine/session, so no real database
(or DB driver) is needed. Coroutines are driven with asyncio.run() so no
pytest-asyncio dependency is required. The healthcheck test is marked
`integration` and only runs when real DB_* environment variables are set.
"""
import asyncio
from unittest.mock import AsyncMock, MagicMock

import pytest

pytest.importorskip("sqlalchemy")
async_connection = pytest.importorskip("database.async_connection")
DatabaseConnection = async_connection.DatabaseConnection

from tests.conftest import DB_ENV_VARS, db_env_is_configured


@pytest.fixture(autouse=True)
def reset_connection(monkeypatch):
    """Resets the singleton and silences the logger around every test."""
    logger_mock = MagicMock()
    logger_mock.error = AsyncMock()
    logger_mock.info = AsyncMock()
    monkeypatch.setattr(async_connection, "logger", logger_mock)
    monkeypatch.setattr(DatabaseConnection, "_engine", None)
    monkeypatch.setattr(DatabaseConnection, "_session_maker", None)
    yield


def _mock_session_maker(execute_side_effect=None):
    """Builds a mock async session maker; returns (session_maker, session)."""
    session = MagicMock(name="session")
    session.execute = AsyncMock(side_effect=execute_side_effect)
    session.commit = AsyncMock()
    session.rollback = AsyncMock()
    session_maker = MagicMock(name="session_maker")
    session_maker.return_value.__aenter__.return_value = session
    return session_maker, session


def test_build_url_uses_env_vars(fake_db_env):
    url = DatabaseConnection._build_url()

    assert url.drivername == "postgresql+asyncpg"
    assert url.host == fake_db_env["DB_HOST"]
    assert url.port == int(fake_db_env["DB_PORT"])
    assert url.username == fake_db_env["DB_USER"]
    assert url.database == fake_db_env["DB_NAME"]


def test_get_engine_is_singleton(fake_db_env, monkeypatch):
    create_async_engine = MagicMock(return_value=MagicMock(name="engine"))
    monkeypatch.setattr(async_connection, "create_async_engine", create_async_engine)

    first = DatabaseConnection.get_engine()
    second = DatabaseConnection.get_engine()

    assert first is second
    create_async_engine.assert_called_once()


def test_session_rolls_back_and_reraises_on_error(fake_db_env):
    async def run():
        DatabaseConnection._engine = MagicMock(name="engine")
        session_maker, session = _mock_session_maker(RuntimeError("boom"))
        DatabaseConnection._session_maker = session_maker

        with pytest.raises(RuntimeError, match="boom"):
            async with DatabaseConnection.session() as s:
                await s.execute("DELETE FROM everything")

        session.rollback.assert_awaited_once()
        session.commit.assert_not_awaited()

    asyncio.run(run())


def test_session_closes_even_on_error(fake_db_env):
    async def run():
        DatabaseConnection._engine = MagicMock(name="engine")
        session_maker, session = _mock_session_maker(RuntimeError("boom"))
        DatabaseConnection._session_maker = session_maker

        with pytest.raises(RuntimeError, match="boom"):
            async with DatabaseConnection.session():
                raise RuntimeError("boom")

        session_maker.return_value.__aexit__.assert_awaited_once()

    asyncio.run(run())


def test_session_commits_on_success(fake_db_env):
    async def run():
        DatabaseConnection._engine = MagicMock(name="engine")
        session_maker, session = _mock_session_maker()
        DatabaseConnection._session_maker = session_maker

        async with DatabaseConnection.session() as s:
            await s.execute("SELECT 1")

        session.commit.assert_awaited_once()
        session.rollback.assert_not_awaited()

    asyncio.run(run())


@pytest.mark.integration
@pytest.mark.skipif(
    not db_env_is_configured(),
    reason=f"real database env vars not set ({', '.join(DB_ENV_VARS)})",
)
def test_healthcheck_against_real_database():
    assert asyncio.run(DatabaseConnection.healthcheck()) is True
