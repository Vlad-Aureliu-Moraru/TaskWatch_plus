import json
from pathlib import Path
from unittest.mock import patch

import pytest

from taskwatch.archive_cmds import create_archive
from taskwatch.directory_cmds import create_directory
from taskwatch.io_cmds import (
    ALLOWED_TABLES,
    _build_archive_export,
    _build_directory_export,
    _build_note_export,
    _build_task_export,
    _do_import_archive,
    _do_import_directory,
    _do_import_note,
    _do_import_task,
    _do_merge_import_directory,
    export_current_item,
    export_data,
    import_data,
    import_notes_json,
    import_tasks_from_directory_json,
)
from taskwatch.note_cmds import create_note, list_notes
from taskwatch.subtask_cmds import create_subtask
from taskwatch.tag_cmds import add_tag_to_task, get_tags_for_task
from taskwatch.task_cmds import create_task, get_task, list_tasks


def _setup(conn):
    create_archive("Test Archive")
    create_directory(1, "Test Dir")


class TestExportData:
    def test_export_empty(self, tmp_path):
        path = str(tmp_path / "export.json")
        result = export_data(path)
        assert result is True
        data = json.loads(Path(path).read_text())
        for table in ALLOWED_TABLES:
            assert table in data
            assert data[table] == []

    def test_export_with_data(self, conn, tmp_path):
        _setup(conn)
        create_task(1, "My Task", deadline="2026-12-31")
        path = str(tmp_path / "export.json")
        export_data(path)
        data = json.loads(Path(path).read_text())
        assert len(data["archives"]) == 1
        assert len(data["directories"]) == 1
        assert len(data["tasks"]) == 1
        assert data["tasks"][0]["name"] == "My Task"

    def test_export_fails_on_bad_path(self):
        result = export_data("/nonexistent/dir/export.json")
        assert result is False


class TestImportData:
    def test_import(self, conn, tmp_path):
        data = {
            "archives": [{"id": 1, "name": "Imported Archive"}],
            "directories": [{"id": 1, "archive_id": 1, "name": "Imported Dir"}],
            "tasks": [],
            "notes": [],
            "tags": [],
            "task_tags": [],
        }
        path = str(tmp_path / "import.json")
        Path(path).write_text(json.dumps(data))
        result = import_data(path)
        assert "Imported" in result
        from taskwatch.archive_cmds import list_archives
        archives = list_archives()
        assert len(archives) == 1
        assert archives[0].name == "Imported Archive"

    def test_import_missing_keys(self, conn, tmp_path):
        path = str(tmp_path / "bad.json")
        Path(path).write_text(json.dumps({"archives": []}))
        result = import_data(path)
        assert "Missing" in result

    def test_import_invalid_json(self, conn, tmp_path):
        path = str(tmp_path / "bad.json")
        Path(path).write_text("not json")
        result = import_data(path)
        assert "Failed" in result

    def test_import_file_not_found(self, conn):
        result = import_data("/nonexistent/file.json")
        assert "Failed" in result


class TestImportTasksFromDirectoryJson:
    def _setup(self, conn):
        _setup(conn)

    def test_list_of_tasks(self, conn):
        self._setup(conn)
        json_str = json.dumps([
            {"name": "Task 1", "urgency": 3},
            {"name": "Task 2", "deadline": "2026-12-31"},
        ])
        ok, msg = import_tasks_from_directory_json(json_str, 1)
        assert ok is True
        assert "Imported 2 of 2" in msg
        assert len(list_tasks(directory_id=1)) == 2

    def test_single_task_object(self, conn):
        self._setup(conn)
        json_str = json.dumps({"task": {"name": "Single"}})
        ok, msg = import_tasks_from_directory_json(json_str, 1)
        assert ok is True
        assert get_task(1).name == "Single"

    def test_tasks_key(self, conn):
        self._setup(conn)
        json_str = json.dumps({"tasks": [{"name": "A"}, {"name": "B"}]})
        ok, msg = import_tasks_from_directory_json(json_str, 1)
        assert ok is True
        assert "Imported 2 of 2" in msg

    def test_with_tags_and_notes(self, conn):
        self._setup(conn)
        json_str = json.dumps([{
            "name": "Task",
            "tags": ["urgent", "bug"],
            "notes": [{"date": "2026-07-04", "note": "Hello"}],
        }])
        ok, msg = import_tasks_from_directory_json(json_str, 1)
        assert ok is True
        tags = get_tags_for_task(1)
        assert sorted(t.name for t in tags) == ["bug", "urgent"]
        notes = list_notes(task_id=1)
        assert len(notes) == 1
        assert notes[0].note == "Hello"

    def test_missing_name(self, conn):
        self._setup(conn)
        json_str = json.dumps([{"urgency": 3}])
        ok, msg = import_tasks_from_directory_json(json_str, 1)
        assert ok is True
        assert "error" in msg

    def test_invalid_json(self, conn):
        ok, msg = import_tasks_from_directory_json("not json", 1)
        assert ok is False
        assert "Invalid JSON" in msg

    def test_unrecognized_structure(self, conn):
        ok, msg = import_tasks_from_directory_json('"just a string"', 1)
        assert ok is False
        assert "Expected" in msg

    def test_empty_array(self, conn):
        self._setup(conn)
        ok, msg = import_tasks_from_directory_json("[]", 1)
        assert ok is False
        assert "No tasks" in msg

    def test_task_with_note_no_date(self, conn):
        self._setup(conn)
        json_str = json.dumps([{
            "name": "Task",
            "notes": [{"note": "Just text"}],
        }])
        ok, msg = import_tasks_from_directory_json(json_str, 1)
        assert ok is True
        notes = list_notes(task_id=1)
        assert len(notes) == 1
        assert notes[0].note == "Just text"


class TestImportNotesJson:
    def _setup(self, conn):
        _setup(conn)
        create_task(1, "Task")

    def test_array_of_notes(self, conn):
        self._setup(conn)
        json_str = json.dumps([
            {"note": "First"},
            {"note": "Second", "date": "2026-07-05"},
        ])
        ok, msg = import_notes_json(json_str, 1)
        assert ok is True
        assert "Imported 2 of 2" in msg

    def test_single_note(self, conn):
        self._setup(conn)
        json_str = json.dumps({"note": "Single note"})
        ok, msg = import_notes_json(json_str, 1)
        assert ok is True
        notes = list_notes(task_id=1)
        assert len(notes) == 1

    def test_notes_key(self, conn):
        self._setup(conn)
        json_str = json.dumps({"notes": [{"note": "A"}, {"note": "B"}]})
        ok, msg = import_notes_json(json_str, 1)
        assert ok is True
        assert "Imported 2 of 2" in msg

    def test_invalid_json(self, conn):
        ok, msg = import_notes_json("not json", 1)
        assert ok is False
        assert "Invalid JSON" in msg

    def test_missing_note_field(self, conn):
        self._setup(conn)
        json_str = json.dumps([{"date": "2026-07-04"}])
        ok, msg = import_notes_json(json_str, 1)
        assert ok is True
        assert "error" in msg


class TestBuildExport:
    def _setup(self, conn):
        _setup(conn)
        create_task(1, "Task A")
        create_task(1, "Task B")
        create_note(1, "2026-07-04", "Note for A")
        create_subtask(1, "Subtask")
        create_note(2, "2026-07-05", "Note for B")
        add_tag_to_task(1, "urgent")

    def test_build_archive_export(self, conn):
        self._setup(conn)
        data = _build_archive_export(1, conn)
        assert "archive" in data
        assert data["archive"]["name"] == "Test Archive"
        assert len(data["directories"]) == 1
        assert len(data["tasks"]) == 2
        assert len(data["notes"]) == 2
        assert len(data["subtasks"]) == 1
        assert len(data["tags"]) == 1

    def test_build_archive_export_nonexistent(self, conn):
        data = _build_archive_export(999, conn)
        assert data == {}

    def test_build_directory_export(self, conn):
        self._setup(conn)
        data = _build_directory_export(1, conn)
        assert "directory" in data
        assert data["directory"]["name"] == "Test Dir"
        assert "archive" in data
        assert len(data["tasks"]) == 2
        assert len(data["notes"]) == 2

    def test_build_directory_export_nonexistent(self, conn):
        data = _build_directory_export(999, conn)
        assert data == {}

    def test_build_task_export(self, conn):
        self._setup(conn)
        data = _build_task_export(1, conn)
        assert "task" in data
        assert data["task"]["name"] == "Task A"
        assert "directory" in data
        assert "archive" in data
        assert len(data["notes"]) == 1
        assert len(data["subtasks"]) == 1

    def test_build_task_export_nonexistent(self, conn):
        data = _build_task_export(999, conn)
        assert data == {}

    def test_build_note_export(self, conn):
        self._setup(conn)
        data = _build_note_export(1, conn)
        assert "note" in data
        assert data["note"]["note"] == "Note for A"

    def test_build_note_export_nonexistent(self, conn):
        data = _build_note_export(999, conn)
        assert data == {}


class TestExportCurrentItem:
    def _setup(self, conn):
        _setup(conn)

    def test_export_archive(self, conn, tmp_path):
        self._setup(conn)
        path = str(tmp_path / "export.json")
        result = export_current_item("ARCHIVES", 1, path)
        assert result is True
        data = json.loads(Path(path).read_text())
        assert data["export_type"] == "archive"

    def test_export_directory(self, conn, tmp_path):
        self._setup(conn)
        path = str(tmp_path / "export.json")
        result = export_current_item("DIRECTORIES", 1, path)
        assert result is True
        data = json.loads(Path(path).read_text())
        assert data["export_type"] == "directory"

    def test_export_task(self, conn, tmp_path):
        self._setup(conn)
        create_task(1, "Task")
        path = str(tmp_path / "export.json")
        result = export_current_item("TASKS", 1, path)
        assert result is True
        data = json.loads(Path(path).read_text())
        assert data["export_type"] == "task"

    def test_export_note(self, conn, tmp_path):
        self._setup(conn)
        create_task(1, "Task")
        create_note(1, "2026-07-04", "Note")
        path = str(tmp_path / "export.json")
        result = export_current_item("NOTES", 1, path)
        assert result is True
        data = json.loads(Path(path).read_text())
        assert data["export_type"] == "note"

    def test_export_invalid_level(self, conn, tmp_path):
        result = export_current_item("INVALID", 1, "/tmp/x.json")
        assert result is False

    def test_export_nonexistent(self, conn, tmp_path):
        result = export_current_item("ARCHIVES", 999, str(tmp_path / "x.json"))
        assert result is False


class TestDoImportArchive:
    def _setup(self, conn):
        _setup(conn)

    def test_import_new_archive(self, conn):
        self._setup(conn)
        data = {
            "archive": {"id": 1, "name": "New Archive"},
            "directories": [{"id": 1, "archive_id": 1, "name": "New Dir"}],
            "tasks": [{"id": 1, "directory_id": 1, "name": "New Task"}],
        }
        result = _do_import_archive(data, conn)
        assert "Imported" in result
        from taskwatch.archive_cmds import list_archives
        names = [a.name for a in list_archives()]
        assert "New Archive" in names

    def test_import_archive_no_data(self, conn):
        result = _do_import_archive({}, conn)
        assert "no archive data" in result


class TestDoImportDirectory:
    def _setup(self, conn):
        create_archive("Target Archive")

    def test_import_directory(self, conn):
        self._setup(conn)
        data = {
            "directory": {"id": 1, "archive_id": 1, "name": "Imported Dir"},
            "tasks": [{"id": 1, "directory_id": 1, "name": "Task"}],
        }
        result = _do_import_directory(data, conn, 1)
        assert "Imported" in result
        dirs = conn.execute("SELECT name FROM directories").fetchall()
        names = [r["name"] for r in dirs]
        assert "Imported Dir" in names

    def test_import_directory_no_data(self, conn):
        result = _do_import_directory({}, conn, 1)
        assert "no directory data" in result


class TestDoImportTask:
    def _setup(self, conn):
        _setup(conn)

    def test_import_task(self, conn):
        self._setup(conn)
        data = {"task": {"id": 1, "directory_id": 1, "name": "Imported Task"}}
        result = _do_import_task(data, conn, 1)
        assert "Imported" in result
        t = get_task(1)
        assert t is not None
        assert t.name == "Imported Task"

    def test_import_task_no_data(self, conn):
        result = _do_import_task({}, conn, 1)
        assert "no task data" in result


class TestDoImportNote:
    def _setup(self, conn):
        _setup(conn)
        create_task(1, "Task")

    def test_import_note(self, conn):
        self._setup(conn)
        data = {"note": {"note": "Hello"}}
        result = _do_import_note(data, conn, 1)
        assert "Imported" in result
        notes = list_notes(task_id=1)
        assert len(notes) == 1
        assert notes[0].note == "Hello"

    def test_import_note_no_data(self, conn):
        result = _do_import_note({}, conn, 1)
        assert "no note data" in result


class TestDoMergeImportDirectory:
    def _setup(self, conn):
        create_archive("Archive")
        create_directory(1, "Existing Dir")
        create_task(1, "Existing Task", deadline="2026-12-31")

    def test_merge_matches_existing(self, conn):
        self._setup(conn)
        data = {
            "directory": {"id": 1, "archive_id": 1, "name": "Existing Dir"},
            "tasks": [{"id": 1, "directory_id": 1, "name": "Existing Task",
                       "finished": True, "finished_date": "2026-07-04"}],
            "notes": [],
            "task_tags": [],
            "subtasks": [],
            "tags": [],
        }
        result = _do_merge_import_directory(data, conn, 1)
        assert "Merged" in result
        # Task should be marked done
        t = get_task(1)
        assert t.finished is True

    def test_merge_creates_new_tasks(self, conn):
        self._setup(conn)
        data = {
            "directory": {"id": 1, "archive_id": 1, "name": "Existing Dir"},
            "tasks": [{"id": 2, "directory_id": 1, "name": "New Task"}],
            "notes": [],
            "task_tags": [],
            "subtasks": [],
            "tags": [],
        }
        result = _do_merge_import_directory(data, conn, 1)
        assert "created" in result

    def test_merge_nonexistent_dir_creates_it(self, conn):
        self._setup(conn)
        data = {
            "directory": {"id": 2, "archive_id": 1, "name": "New Dir"},
            "tasks": [],
        }
        result = _do_merge_import_directory(data, conn, 1)
        assert "Imported" in result
        assert "New Dir" in result


class TestImportExportedItem:
    def _setup(self, conn):
        _setup(conn)

    def test_import_archive_from_file(self, conn, tmp_path):
        self._setup(conn)
        data = {
            "export_type": "archive",
            "archive": {"id": 1, "name": "File Archive"},
            "directories": [],
        }
        path = str(tmp_path / "import.json")
        Path(path).write_text(json.dumps(data))
        from taskwatch.io_cmds import import_exported_item
        result = import_exported_item(path, "ARCHIVES")
        assert "Imported" in result

    def test_import_missing_export_type(self, conn, tmp_path):
        path = str(tmp_path / "bad.json")
        Path(path).write_text(json.dumps({"name": "test"}))
        from taskwatch.io_cmds import import_exported_item
        result = import_exported_item(path, "ARCHIVES")
        assert "Unknown export type" in result

    def test_import_bad_file(self, conn):
        from taskwatch.io_cmds import import_exported_item
        result = import_exported_item("/nonexistent.json", "ARCHIVES")
        assert "Failed" in result

    def test_import_directory_no_archive_id(self, conn, tmp_path):
        data = {"export_type": "directory", "directory": {"name": "D"}}
        path = str(tmp_path / "d.json")
        Path(path).write_text(json.dumps(data))
        from taskwatch.io_cmds import import_exported_item
        result = import_exported_item(path, "DIRECTORIES", archive_id=None)
        assert "archive" in result
