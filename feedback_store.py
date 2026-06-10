from __future__ import annotations

import logging
import sqlite3
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "meridianai_feedback.db"


def _connect() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_feedback_db() -> None:
    with _connect() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS feedback_events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT NOT NULL,
                symptom TEXT NOT NULL,
                region TEXT NOT NULL,
                selected_meridian TEXT,
                duration_minutes INTEGER,
                recommended_point TEXT NOT NULL,
                helped INTEGER NOT NULL,
                created_at TEXT NOT NULL DEFAULT (datetime('now'))
            )
            """
        )
        conn.commit()
    logger.info("Feedback database initialized at %s", DB_PATH)


def insert_feedback(payload: dict[str, Any]) -> int:
    with _connect() as conn:
        cur = conn.execute(
            """
            INSERT INTO feedback_events (
                session_id, symptom, region, selected_meridian,
                duration_minutes, recommended_point, helped
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                payload["session_id"],
                payload["symptom"],
                payload["region"],
                payload.get("selected_meridian"),
                payload.get("duration_minutes"),
                payload["recommended_point"],
                1 if payload["helped"] else 0,
            ),
        )
        conn.commit()
        return int(cur.lastrowid)


def get_feedback_summary() -> dict[str, Any]:
    with _connect() as conn:
        total = conn.execute("SELECT COUNT(*) AS c FROM feedback_events").fetchone()["c"]
        helped = conn.execute(
            "SELECT COUNT(*) AS c FROM feedback_events WHERE helped = 1"
        ).fetchone()["c"]
        point_rows = conn.execute(
            """
            SELECT recommended_point, COUNT(*) AS total_count,
                   SUM(CASE WHEN helped = 1 THEN 1 ELSE 0 END) AS helped_count
            FROM feedback_events
            GROUP BY recommended_point
            ORDER BY total_count DESC
            """
        ).fetchall()

    return {
        "total_feedback": int(total),
        "helped_feedback": int(helped),
        "help_rate": (float(helped) / float(total)) if total else 0.0,
        "points": [dict(row) for row in point_rows],
    }


def get_helpful_feedback_rows(min_count_per_point: int = 1) -> list[dict[str, Any]]:
    with _connect() as conn:
        rows = conn.execute(
            """
            SELECT symptom, region, duration_minutes, recommended_point
            FROM feedback_events
            WHERE helped = 1
            """
        ).fetchall()
    return [dict(r) for r in rows if r["recommended_point"]]
