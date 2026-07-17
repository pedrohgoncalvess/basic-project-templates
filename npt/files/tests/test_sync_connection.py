"""
Tests for database.sync_connection.DatabaseConnection.

Unit tests mock the SQLAlchemy engine/session, so no real database (or DB
driver) is needed. The healthcheck test is marked `integration` and only
runs when real DB_* environment variables are configured.
"""
from unittest.mock import MagicMock

import pytest

pytest.importorskip("sqlalchemy")
sync_connection = pytest.importorskip("database.sync_connection")
DatabaseConnection = sync_connection.DatabaseConnection

from tests.conftest import DB_ENV_VARS, db_env_is_configured


@pytest.fixture(autouse=True)
def reset_connection(monkeypatch):
    """Resets the singleton and silences the logger around every test."""
    monkeypatch.setattr(sync_connection, "logger", MagicMock())
    monkeypatch.setattr(DatabaseConnection, "_engine", None)
    monkeypatch.setattr(DatabaseConnection, "_session_maker", None)
    yield


def test_build_url_uses_env_vars(fake_db_env):
    url = DatabaseConnection._build_url()

    assert url.drivername == "postgresql+psycopg2"
    assert url.host == fake_db_env["DB_HOST"]
    assert url.port == int(fake_db_env["DB_PORT"])
    assert url.username == fake_db_env["DB_USER"]
    assert url.database == fake_db_env["DB_NAME"]


def test_get_engine_is_singleton(fake_db_env, monkeypatch):
    create_engine = MagicMock(return_value=MagicMock(name="engine"))
    monkeypatch.setattr(sync_connection, "create_engine", create_engine)

    first = DatabaseConnection.get_engine()
    second = DatabaseConnection.get_engine()

    assert first is second
    create_engine.assert_called_once()


def test_session_rolls_back_and_reraises_on_error(fake_db_env):
    DatabaseConnection._engine = MagicMock(name="engine")
    session = MagicMock(name="session")
    session.execute.side_effect = RuntimeError("boom")
    session_maker = MagicMock(name="session_maker")
    session_maker.return_value.__enter__.return_value = session
    DatabaseConnection._session_maker = session_maker

    with pytest.raises(RuntimeError, match="boom"):
        with DatabaseConnection.session() as s:
            s.execute("DELETE FROM everything")

    session.rollback.assert_called_once()
    session.commit.assert_not_called()


def test_session_closes_even_on_error(fake_db_env):
    DatabaseConnection._engine = MagicMock(name="engine")
    session = MagicMock(name="session")
    session.execute.side_effect = RuntimeError("boom")
    session_maker = MagicMock(name="session_maker")
    session_maker.return_value.__enter__.return_value = session
    DatabaseConnection._session_maker = session_maker

    with pytest.raises(RuntimeError, match="boom"):
        with DatabaseConnection.session():
            raise RuntimeError("boom")

    session_maker.return_value.__exit__.assert_called_once()


def test_session_commits_on_success(fake_db_env):
    DatabaseConnection._engine = MagicMock(name="engine")
    session = MagicMock(name="session")
    session_maker = MagicMock(name="session_maker")
    session_maker.return_value.__enter__.return_value = session
    DatabaseConnection._session_maker = session_maker

    with DatabaseConnection.session() as s:
        s.execute("SELECT 1")

    session.commit.assert_called_once()
    session.rollback.assert_not_called()


@pytest.mark.integration
@pytest.mark.skipif(
    not db_env_is_configured(),
    reason=f"real database env vars not set ({', '.join(DB_ENV_VARS)})",
)
def test_healthcheck_against_real_database():
    assert DatabaseConnection.healthcheck() is True
