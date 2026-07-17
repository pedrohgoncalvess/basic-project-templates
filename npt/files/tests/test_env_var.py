"""
Tests for utils.env_var (get_env_var) and environment variable documentation.
"""
import re
from pathlib import Path

import pytest

from utils import get_env_var

ENV_VAR_USAGE = re.compile(r"""get_env_var\(\s*["']([A-Z_][A-Z0-9_]*)["']\s*\)""")


def test_get_env_var_returns_value(monkeypatch):
    monkeypatch.setenv("NPT_TEST_VAR", "some-value")
    assert get_env_var("NPT_TEST_VAR") == "some-value"


def test_get_env_var_returns_none_when_missing(monkeypatch):
    monkeypatch.delenv("NPT_MISSING_VAR", raising=False)
    assert get_env_var("NPT_MISSING_VAR") is None


def _env_example_keys(path: Path) -> set[str]:
    keys = set()
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            keys.add(line.split("=", 1)[0].strip())
    return keys


def _env_vars_used_in_code(project_root: Path) -> set[str]:
    used = set()
    for py_file in project_root.rglob("*.py"):
        parts = set(py_file.parts)
        if parts & {"tests", ".venv", "__pycache__", "migrations"}:
            continue
        used |= set(ENV_VAR_USAGE.findall(py_file.read_text(encoding="utf-8")))
    return used


def test_env_example_documents_all_required_vars(project_root):
    """
    Every variable read through get_env_var() in the project code must be
    documented in .env.example, so new developers know what to configure.
    """
    env_example = project_root / ".env.example"
    if not env_example.exists():
        pytest.skip("project has no .env.example file")

    documented = _env_example_keys(env_example)
    used = _env_vars_used_in_code(project_root)

    missing = used - documented
    assert not missing, (
        f"Variables used in code but missing from .env.example: {sorted(missing)}"
    )
