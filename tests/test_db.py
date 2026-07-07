import sqlite3

import pytest


class TestSchemaCreation:
    def test_tables_exist(self, conn):
        tables = conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name"
        ).fetchall()
        names = [r["name"] for r in tables]
        assert "archives" in names
        assert "directories" in names
        assert "tasks" in names
        assert "notes" in names
        assert "tags" in names
        assert "task_tags" in names
        assert "task_dependencies" in names
        assert "subtasks" in names
        assert "timer_sessions" in names

    def test_foreign_keys_enabled(self, conn):
        row = conn.execute("PRAGMA foreign_keys").fetchone()
        assert row[0] == 1

    def test_journal_mode_wal(self, conn):
        row = conn.execute("PRAGMA journal_mode").fetchone()
        assert row[0] == "wal"


class TestIndexes:
    def _index_names(self, conn):
        rows = conn.execute(
            "SELECT name FROM sqlite_master WHERE type='index' AND name LIKE 'idx_%'"
        ).fetchall()
        return {r["name"] for r in rows}

    def test_key_indexes_exist(self, conn):
        idxs = self._index_names(conn)
        assert "idx_tasks_directory_id" in idxs
        assert "idx_tasks_finished" in idxs
        assert "idx_tasks_deadline" in idxs
        assert "idx_directories_archive_id" in idxs
        assert "idx_notes_task_id" in idxs
        assert "idx_subtasks_task_id" in idxs


class TestMigrations:
    def test_position_column_exists(self, conn):
        cols = [r["name"] for r in conn.execute("PRAGMA table_info(tasks)").fetchall()]
        assert "position" in cols

    def test_pinned_column_exists(self, conn):
        cols = [r["name"] for r in conn.execute("PRAGMA table_info(tasks)").fetchall()]
        assert "pinned" in cols

    def test_file_path_column_exists(self, conn):
        cols = [r["name"] for r in conn.execute("PRAGMA table_info(notes)").fetchall()]
        assert "file_path" in cols

    def test_created_at_column_exists(self, conn):
        cols = [r["name"] for r in conn.execute("PRAGMA table_info(notes)").fetchall()]
        assert "created_at" in cols

    def test_migration_idempotent(self, conn):
        """Running get_conn() again should not fail."""
        from taskwatch.db import get_conn
        c2 = get_conn()
        assert c2 is not None

    def test_date_migration_dmy_to_iso(self, conn):
        from taskwatch.archive_cmds import create_archive
        from taskwatch.directory_cmds import create_directory
        create_archive("Test")
        create_directory(1, "Dir")
        # Insert a task with DMY date directly
        conn.execute(
            "INSERT INTO tasks (id, directory_id, name, deadline) VALUES (?, ?, ?, ?)",
            (1, 1, "Test", "04/07/2026"),
        )
        # Run migration again
        from taskwatch.db import _migrate_dates
        _migrate_dates(conn)
        row = conn.execute("SELECT deadline FROM tasks WHERE id = 1").fetchone()
        assert row["deadline"] == "2026-07-04"

    def test_date_migration_iso_untouched(self, conn):
        from taskwatch.archive_cmds import create_archive
        from taskwatch.directory_cmds import create_directory
        create_archive("Test")
        create_directory(1, "Dir")
        conn.execute(
            "INSERT INTO tasks (id, directory_id, name, deadline) VALUES (?, ?, ?, ?)",
            (1, 1, "Test", "2026-07-04"),
        )
        from taskwatch.db import _migrate_dates
        _migrate_dates(conn)
        row = conn.execute("SELECT deadline FROM tasks WHERE id = 1").fetchone()
        assert row["deadline"] == "2026-07-04"


class TestCascadeDelete:
    def test_delete_archive_cascades(self, conn):
        from taskwatch.archive_cmds import create_archive, delete_archive
        from taskwatch.directory_cmds import create_directory
        create_archive("Test")
        create_directory(1, "Dir")
        delete_archive(1)
        rows = conn.execute("SELECT id FROM directories").fetchall()
        assert len(rows) == 0

    def test_delete_directory_cascades(self, conn):
        from taskwatch.archive_cmds import create_archive
        from taskwatch.directory_cmds import create_directory, delete_directory
        from taskwatch.task_cmds import create_task
        create_archive("Test")
        create_directory(1, "Dir")
        create_task(1, "Task")
        delete_directory(1)
        rows = conn.execute("SELECT id FROM tasks").fetchall()
        assert len(rows) == 0


class TestClose:
    def test_close_reopens(self, conn):
        from taskwatch.db import close, get_conn
        close()
        c = get_conn()
        assert c is not None
