"""
Shared pytest configuration and fixtures.

Responsibilities:
    - Guarantees the project root is importable (so `utils`, `log`,
      `database`, ... can be imported no matter where pytest runs from).
    - Registers the `integration` marker (tests that need external
      resources such as a running database).
    - Provides common fixtures (fake database env vars, project root).
"""
import os
import sys
from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).resolve().parent.parent

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

DB_ENV_VARS = ("DB_HOST", "DB_PORT", "DB_USER", "DB_PASSWORD", "DB_NAME")


def pytest_configure(config):
    config.addinivalue_line(
        "markers",
        "integration: test requires external resources (e.g. a running database).",
    )


@pytest.fixture
def project_root() -> Path:
    """Absolute path of the generated project root."""
    return PROJECT_ROOT


@pytest.fixture
def fake_db_env(monkeypatch) -> dict:
    """Sets fake DB_* environment variables and returns them as a dict."""
    values = {
        "DB_HOST": "fake-host",
        "DB_PORT": "5432",
        "DB_USER": "fake-user",
        "DB_PASSWORD": "fake-password",
        "DB_NAME": "fake-db",
    }
    for key, value in values.items():
        monkeypatch.setenv(key, value)
    return values


def db_env_is_configured() -> bool:
    """True when every DB_* variable is set and non-empty (real database)."""
    return all(os.getenv(var) for var in DB_ENV_VARS)
