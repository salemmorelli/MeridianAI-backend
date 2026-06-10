# tests/conftest.py
from __future__ import annotations
import os
from pathlib import Path
from unittest.mock import MagicMock, patch

# ── Load environment FIRST before any app imports ──
from dotenv import load_dotenv
env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

if not os.getenv("DATABASE_URL"):
    os.environ["DATABASE_URL"] = "postgresql://postgres:password123@localhost:5432/meridianai_db"
if not os.getenv("ANTHROPIC_API_KEY"):
    os.environ["ANTHROPIC_API_KEY"] = "test-key-placeholder"

# ── Patch SQLAlchemy engine BEFORE main.py is imported ──
# This stops the PostgreSQL connection attempt at module load time
_mock_engine = MagicMock()
_mock_session = MagicMock()
_mock_base = MagicMock()

_engine_patcher  = patch("database.engine",      _mock_engine)
_session_patcher = patch("database.SessionLocal", _mock_session)
_create_patcher  = patch("sqlalchemy.create_engine", return_value=_mock_engine)

_engine_patcher.start()
_session_patcher.start()
_create_patcher.start()

# ── Patch feedback_store SQLite operations ──
_init_patcher    = patch("feedback_store.init_feedback_db", MagicMock(return_value=None))
_insert_patcher  = patch("feedback_store.insert_feedback",  MagicMock(return_value=42))
_summary_patcher = patch("feedback_store.get_feedback_summary", MagicMock(return_value={
    "total_feedback": 10,
    "helped_feedback": 8,
    "help_rate": 0.8,
    "points": []
}))

_init_patcher.start()
_insert_patcher.start()
_summary_patcher.start()

# ── NOW import pytest and app ──
import pytest
from fastapi.testclient import TestClient

@pytest.fixture(scope="session")
def client():
    from main import app
    return TestClient(app)

@pytest.fixture(autouse=True)
def reset_mocks():
    """Reset mock call counts between tests."""
    _mock_engine.reset_mock()
    _mock_session.reset_mock()