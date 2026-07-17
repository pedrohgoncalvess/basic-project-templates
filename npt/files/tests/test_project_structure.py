"""
Tests for the generated project structure and configuration files.
"""
import importlib
import tomllib
from pathlib import Path

import pytest

ESSENTIAL_FILES = ("pyproject.toml", ".gitignore", ".python-version", "LICENSE")


def test_essential_files_exist(project_root):
    missing = [name for name in ESSENTIAL_FILES if not (project_root / name).exists()]
    assert not missing, f"Essential project files missing: {missing}"


def test_readme_exists(project_root):
    readmes = [p for p in project_root.iterdir() if p.name.lower().startswith("readme")]
    assert readmes, "No README file found in project root"


def test_env_file_is_gitignored(project_root):
    gitignore = project_root / ".gitignore"
    if not gitignore.exists():
        pytest.skip("project has no .gitignore")

    ignored = {
        line.strip()
        for line in gitignore.read_text(encoding="utf-8").splitlines()
        if line.strip() and not line.startswith("#")
    }
    assert any(
        entry.lstrip("/") in (".env", ".env/") or entry == ".env*" for entry in ignored
    ), ".env must be listed in .gitignore to avoid committing secrets"


def test_pyproject_is_valid(project_root):
    pyproject = project_root / "pyproject.toml"
    if not pyproject.exists():
        pytest.skip("project has no pyproject.toml")

    with pyproject.open("rb") as f:
        data = tomllib.load(f)

    project = data.get("project", {})
    assert project.get("name"), "pyproject.toml must define project.name"
    assert project.get("version"), "pyproject.toml must define project.version"


def test_top_level_packages_are_importable(project_root):
    """Importing the project packages must not raise (catches circular imports
    and missing dependencies)."""
    for package in ("utils", "log"):
        if (project_root / package).is_dir():
            importlib.import_module(package)

    if (project_root / "database").is_dir():
        pytest.importorskip("sqlalchemy")
        importlib.import_module("database")
