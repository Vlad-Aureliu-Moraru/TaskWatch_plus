import pytest

from taskwatch.archive_cmds import create_archive
from taskwatch.directory_cmds import create_directory
from taskwatch.note_cmds import create_note, delete_note, get_note, list_notes, update_note
from taskwatch.task_cmds import create_task


def _setup(conn):
    create_archive("Test Archive")
    create_directory(1, "Test Dir")
    create_task(1, "Test Task")


class TestCreateNote:
    def test_create(self, conn):
        _setup(conn)
        n = create_note(1, "2026-07-04", "Hello")
        assert n.id == 1
        assert n.task_id == 1
        assert n.date == "2026-07-04"
        assert n.note == "Hello"
        assert n.file_path is None

    def test_with_file_path(self, conn):
        _setup(conn)
        n = create_note(1, "2026-07-04", "Note", file_path="/tmp/test.txt")
        assert n.file_path == "/tmp/test.txt"

    def test_auto_created_at(self, conn):
        _setup(conn)
        n = create_note(1, "2026-07-04", "Hello")
        assert n.created_at != ""


class TestListNotes:
    def test_empty(self, conn):
        _setup(conn)
        assert list_notes(task_id=1) == []

    def test_by_task(self, conn):
        _setup(conn)
        create_note(1, "2026-07-04", "A")
        create_note(1, "2026-07-05", "B")
        notes = list_notes(task_id=1)
        assert len(notes) == 2
        assert [n.note for n in notes] == ["A", "B"]

    def test_all_notes(self, conn):
        _setup(conn)
        create_task(1, "Task 2")
        create_note(1, "2026-07-04", "A")
        create_note(2, "2026-07-05", "B")
        notes = list_notes()
        assert len(notes) == 2


class TestGetNote:
    def test_existing(self, conn):
        _setup(conn)
        create_note(1, "2026-07-04", "Hello")
        n = get_note(1)
        assert n is not None
        assert n.note == "Hello"

    def test_missing(self, conn):
        assert get_note(999) is None


class TestUpdateNote:
    def test_update_note_text(self, conn):
        _setup(conn)
        create_note(1, "2026-07-04", "Old")
        n = update_note(1, note="New")
        assert n is not None
        assert n.note == "New"

    def test_update_date(self, conn):
        _setup(conn)
        create_note(1, "2026-07-04", "Note")
        n = update_note(1, date="2026-07-05")
        assert n.date == "2026-07-05"

    def test_update_file_path(self, conn):
        _setup(conn)
        create_note(1, "2026-07-04", "Note")
        n = update_note(1, file_path="/tmp/new.txt")
        assert n.file_path == "/tmp/new.txt"

    def test_update_nonexistent(self, conn):
        n = update_note(999, note="Ghost")
        assert n is None

    def test_no_updates_returns_original(self, conn):
        _setup(conn)
        create_note(1, "2026-07-04", "Note")
        n = update_note(1)
        assert n is not None
        assert n.note == "Note"


class TestDeleteNote:
    def test_delete(self, conn):
        _setup(conn)
        create_note(1, "2026-07-04", "Hello")
        assert delete_note(1) is True
        assert get_note(1) is None

    def test_delete_nonexistent(self, conn):
        assert delete_note(999) is False
