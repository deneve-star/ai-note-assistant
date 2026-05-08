import os
import sqlite3
import pytest

os.environ["DB_PATH"] = ":memory:"
os.environ["AI_API_KEY"] = ""

import storage


@pytest.fixture(autouse=True)
def setup_db(tmp_path):
    db_path = str(tmp_path / "test.db")
    storage.DB_PATH = db_path

    conn = sqlite3.connect(db_path)
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

    original_get_conn = storage.get_connection

    def patched_get_connection():
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        return conn

    storage.get_connection = patched_get_connection
    yield
    storage.get_connection = original_get_conn


class TestAddNote:
    def test_add_returns_id(self):
        note_id = storage.add_note("test note")
        assert note_id == 1

    def test_add_with_tags(self):
        note_id = storage.add_note("tagged note", "work,urgent")
        assert note_id >= 1

    def test_add_multiple(self):
        id1 = storage.add_note("first")
        id2 = storage.add_note("second")
        assert id2 > id1


class TestGetAllNotes:
    def test_empty_db(self):
        notes = storage.get_all_notes()
        assert notes == []

    def test_get_all(self):
        storage.add_note("note one", "work")
        storage.add_note("note two", "personal")
        notes = storage.get_all_notes()
        assert len(notes) == 2

    def test_filter_by_tag(self):
        storage.add_note("work stuff", "work")
        storage.add_note("personal stuff", "personal")
        notes = storage.get_all_notes(tag="work")
        assert len(notes) == 1
        assert notes[0]["content"] == "work stuff"


class TestSearchNotes:
    def test_search_found(self):
        storage.add_note("meeting with John about roadmap")
        storage.add_note("buy groceries")
        results = storage.search_notes("roadmap")
        assert len(results) == 1
        assert "roadmap" in results[0]["content"]

    def test_search_not_found(self):
        storage.add_note("some note")
        results = storage.search_notes("nonexistent")
        assert results == []


class TestDeleteNote:
    def test_delete_existing(self):
        note_id = storage.add_note("to delete")
        assert storage.delete_note(note_id) is True

    def test_delete_nonexistent(self):
        assert storage.delete_note(9999) is False


class TestGetNoteById:
    def test_get_existing(self):
        note_id = storage.add_note("find me", "test")
        note = storage.get_note_by_id(note_id)
        assert note is not None
        assert note["content"] == "find me"

    def test_get_nonexistent(self):
        note = storage.get_note_by_id(9999)
        assert note is None


class TestUpdateTags:
    def test_update_tags(self):
        note_id = storage.add_note("update me", "old")
        result = storage.update_tags(note_id, "new,updated")
        assert result is True
        note = storage.get_note_by_id(note_id)
        assert note["tags"] == "new,updated"

    def test_update_nonexistent(self):
        result = storage.update_tags(9999, "tag")
        assert result is False
