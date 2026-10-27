"""Tickets in a SQLite database: the storage behind the ops service."""

import sqlite3
from datetime import UTC, datetime

SCHEMA = """
CREATE TABLE IF NOT EXISTS tickets (
    id INTEGER PRIMARY KEY,
    service TEXT NOT NULL,
    title TEXT NOT NULL,
    severity TEXT NOT NULL,
    opened_at TEXT NOT NULL
)
"""


def connect(path: str = ":memory:") -> sqlite3.Connection:
    db = sqlite3.connect(path)
    db.row_factory = sqlite3.Row
    db.execute(SCHEMA)
    return db


def add_ticket(db: sqlite3.Connection, service: str, title: str, severity: str) -> int:
    opened = datetime.now(UTC).isoformat()
    cur = db.execute(
        "INSERT INTO tickets (service, title, severity, opened_at) VALUES (?, ?, ?, ?)",
        (service, title, severity, opened),
    )
    db.commit()
    return cur.lastrowid


def find_tickets(db: sqlite3.Connection, service: str) -> list[dict]:
    """Every ticket for one service, oldest first."""
    rows = db.execute(
        "SELECT * FROM tickets WHERE service = ? ORDER BY opened_at, id", (service,)
    ).fetchall()
    return [dict(r) for r in rows]
