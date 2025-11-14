# database/db.py
import sqlite3
from pathlib import Path
from typing import Dict, Any

DB_PATH = Path(__file__).resolve().parents[1] / "events.db"

SCHEMA = """
CREATE TABLE IF NOT EXISTS events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    site_id TEXT NOT NULL,
    event_type TEXT NOT NULL,
    path TEXT,
    user_id TEXT,
    timestamp TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_site_date ON events(site_id, timestamp);
"""

def get_conn():
    conn = sqlite3.connect(str(DB_PATH), check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_conn()
    cur = conn.cursor()
    cur.executescript(SCHEMA)
    conn.commit()
    conn.close()
    print(f"Initialized DB at: {DB_PATH}")

def insert_event(event: Dict[str, Any]):
    """
    event expected keys: site_id, event_type, path (opt), user_id (opt), timestamp
    """
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        """
        INSERT INTO events (site_id, event_type, path, user_id, timestamp)
        VALUES (?, ?, ?, ?, ?)
        """,
        (
            event.get("site_id"),
            event.get("event_type"),
            event.get("path"),
            event.get("user_id"),
            event.get("timestamp"),
        ),
    )
    conn.commit()
    last_id = cur.lastrowid
    conn.close()
    return last_id

def query_sample(limit=10):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT * FROM events ORDER BY id DESC LIMIT ?", (limit,))
    rows = cur.fetchall()
    conn.close()
    return [dict(r) for r in rows]
