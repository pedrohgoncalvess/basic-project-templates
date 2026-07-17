"""
Tests for the structured logger (log.config.StructuredLogger).

The logger writes to files partitioned by date; these tests redirect the
output to a temporary directory so the real log folder is never touched.
"""
import asyncio

import pytest

from log import logger


@pytest.fixture
def logger_tmp_path(tmp_path, monkeypatch):
    """Redirects the logger output to a temporary directory."""
    log_file = tmp_path / f"{logger.partition_by}{logger._log_file_format_}"
    monkeypatch.setattr(logger, "_log_file_dir_", str(tmp_path))
    monkeypatch.setattr(logger, "_log_path_", str(log_file))
    return log_file


def test_info_writes_structured_line(logger_tmp_path):
    asyncio.run(logger.info("TestModule", "TestOperation", "hello world"))

    content = logger_tmp_path.read_text(encoding="utf-8")
    assert "MODE" in content  # header was written on init
    assert "INFO" in content
    assert "TestModule" in content
    assert "hello world" in content
    assert logger.sep in content


def test_error_writes_error_level(logger_tmp_path):
    asyncio.run(logger.error("TestModule", "TestError", "something broke"))

    content = logger_tmp_path.read_text(encoding="utf-8")
    assert "ERROR" in content
    assert "TestError" in content
    assert "something broke" in content


def test_init_creates_file_with_headers(logger_tmp_path):
    asyncio.run(logger.init())

    content = logger_tmp_path.read_text(encoding="utf-8")
    for header in logger.headers:
        assert header in content
