from unittest.mock import patch

import pytest

from taskwatch.calcurse_cmds import (
    _date_to_mmddyyyy,
    read_apts,
    sync_to_calcurse,
    task_to_apt_line,
)
from taskwatch.models import Task


class TestDateToMmddyyyy:
    def test_none_values(self):
        assert _date_to_mmddyyyy(None) is None
        assert _date_to_mmddyyyy("") is None
        assert _date_to_mmddyyyy("none") is None

    def test_iso_format(self):
        assert _date_to_mmddyyyy("2026-07-04") == "07/04/2026"

    def test_dmy_format(self):
        assert _date_to_mmddyyyy("04/07/2026") == "07/04/2026"

    def test_invalid(self):
        assert _date_to_mmddyyyy("not-a-date") is None


class TestTaskToAptLine:
    def test_with_deadline(self):
        t = Task(id=1, directory_id=1, name="My Task", deadline="2026-07-04")
        line = task_to_apt_line(t)
        assert line is not None
        assert "07/04/2026" in line
        assert "[TW]" in line
        assert "My Task" in line

    def test_no_deadline(self):
        t = Task(id=1, directory_id=1, name="No deadline")
        assert task_to_apt_line(t) is None

    def test_deadline_none(self):
        t = Task(id=1, directory_id=1, name="Task", deadline="none")
        assert task_to_apt_line(t) is None


class TestReadApts:
    def test_file_not_found(self):
        with patch("taskwatch.calcurse_cmds.APTS_FILE") as mock:
            mock.exists.return_value = False
            assert read_apts() == []

    def test_reads_lines(self):
        with patch("taskwatch.calcurse_cmds.APTS_FILE") as mock:
            mock.exists.return_value = True
            mock.read_text.return_value = "line1\nline2\n\n"
            lines = read_apts()
            assert lines == ["line1", "line2"]

    def test_strips_empty_lines(self):
        with patch("taskwatch.calcurse_cmds.APTS_FILE") as mock:
            mock.exists.return_value = True
            mock.read_text.return_value = "a\n\nb\n  \n"
            lines = read_apts()
            assert lines == ["a", "b"]


class TestSyncToCalcurse:
    @patch("taskwatch.calcurse_cmds.APTS_FILE")
    @patch("taskwatch.calcurse_cmds.CALCURSE_DIR")
    def test_sync_empty_tasks(self, mock_dir, mock_apts):
        from taskwatch.archive_cmds import create_archive
        from taskwatch.directory_cmds import create_directory
        from taskwatch.task_cmds import create_task
        import taskwatch.db
        conn = taskwatch.db.get_conn()
        create_archive("Test")
        create_directory(1, "Dir")
        create_task(1, "No deadline")
        mock_apts.exists.return_value = False
        result = sync_to_calcurse()
        assert result == 0

    @patch("taskwatch.calcurse_cmds.APTS_FILE")
    @patch("taskwatch.calcurse_cmds.CALCURSE_DIR")
    def test_sync_with_deadlines(self, mock_dir, mock_apts):
        import taskwatch.db
        conn = taskwatch.db.get_conn()
        from taskwatch.archive_cmds import create_archive
        from taskwatch.directory_cmds import create_directory
        from taskwatch.task_cmds import create_task
        create_archive("Test")
        create_directory(1, "Dir")
        create_task(1, "Due task", deadline="2026-12-31")
        mock_apts.exists.return_value = False
        result = sync_to_calcurse()
        assert result == 1

    @patch("taskwatch.calcurse_cmds.APTS_FILE")
    @patch("taskwatch.calcurse_cmds.CALCURSE_DIR")
    def test_replaces_old_tw_entries(self, mock_dir, mock_apts):
        import taskwatch.db
        conn = taskwatch.db.get_conn()
        from taskwatch.archive_cmds import create_archive
        from taskwatch.directory_cmds import create_directory
        from taskwatch.task_cmds import create_task
        create_archive("Test")
        create_directory(1, "Dir")
        create_task(1, "Task", deadline="2026-12-31")
        mock_apts.exists.return_value = True
        mock_apts.read_text.return_value = (
            "01/01/2020 | [TW] Old task\n"
            "01/02/2020 | Custom appointment\n"
        )
        result = sync_to_calcurse()
        assert result == 1
        written = mock_apts.write_text.call_args[0][0]
        assert "[TW] Old task" not in written
        assert "Custom appointment" in written
        assert "[TW] Task" in written
