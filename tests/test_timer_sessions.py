from taskwatch.archive_cmds import create_archive
from taskwatch.directory_cmds import create_directory
from taskwatch.task_cmds import create_task
from taskwatch.timer_sessions import get_total_time_for_task, log_session


def _setup(conn):
    create_archive("Test Archive")
    create_directory(1, "Test Dir")
    create_task(1, "Test Task")


class TestLogSession:
    def test_log(self, conn):
        _setup(conn)
        log_session(1, 300)
        assert get_total_time_for_task(1) == 300

    def test_log_multiple_sessions(self, conn):
        _setup(conn)
        log_session(1, 300)
        log_session(1, 150)
        assert get_total_time_for_task(1) == 450

    def test_log_none_task_id_does_nothing(self, conn):
        log_session(None, 300)
        assert get_total_time_for_task(999) == 0

    def test_log_for_different_tasks(self, conn):
        _setup(conn)
        create_task(1, "Task 2")
        log_session(1, 300)
        log_session(2, 600)
        assert get_total_time_for_task(1) == 300
        assert get_total_time_for_task(2) == 600


class TestGetTotalTime:
    def test_no_sessions(self, conn):
        _setup(conn)
        assert get_total_time_for_task(1) == 0

    def test_nonexistent_task(self, conn):
        assert get_total_time_for_task(999) == 0
