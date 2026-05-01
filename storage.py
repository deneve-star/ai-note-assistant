import sqlite3
from datetime import datetime
from config import DB_PATH


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_connection()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            content TEXT NOT NULL,
            tags TEXT DEFAULT '',
            created_at TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()


def add_note(content: str, tags: str = "") -> int:
    conn = get_connection()
    cursor = conn.execute(
        "INSERT INTO notes (content, tags, created_at) VALUES (?, ?, ?)",
        (content, tags, datetime.now().isoformat()),
    )
    conn.commit()
    note_id = cursor.lastrowid
    conn.close()
    return note_id


def get_all_notes(tag: str = None) -> list[dict]:
    conn = get_connection()
    if tag:
        rows = conn.execute(
            "SELECT * FROM notes WHERE tags LIKE ? ORDER BY created_at DESC",
            (f"%{tag}%",),
        ).fetchall()
    else:
        rows = conn.execute(
            "SELECT * FROM notes ORDER BY created_at DESC"
        ).fetchall()
    conn.close()
    return [dict(row) for row in rows]


def search_notes(query: str) -> list[dict]:
    conn = get_connection()
    rows = conn.execute(
        "SELECT * FROM notes WHERE content LIKE ? ORDER BY created_at DESC",
        (f"%{query}%",),
    ).fetchall()
    conn.close()
    return [dict(row) for row in rows]


def delete_note(note_id: int) -> bool:
    conn = get_connection()
    cursor = conn.execute("DELETE FROM notes WHERE id = ?", (note_id,))
    conn.commit()
    deleted = cursor.rowcount > 0
    conn.close()
    return deleted
