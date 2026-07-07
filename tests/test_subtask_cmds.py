import pytest

from taskwatch.archive_cmds import create_archive
from taskwatch.directory_cmds import create_directory
from taskwatch.subtask_cmds import (
    create_subtask,
    delete_subtask,
    list_subtasks,
    mark_done,
    mark_not_done,
    update_subtask,
)
from taskwatch.task_cmds import create_task


def _setup(conn):
    create_archive("Test Archive")
    create_directory(1, "Test Dir")
    create_task(1, "Test Task")


class TestCreateSubtask:
    def test_create(self, conn):
        _setup(conn)
        s = create_subtask(1, "Step 1")
        assert s.id == 1
        assert s.task_id == 1
        assert s.content == "Step 1"
        assert s.finished is False

    def test_auto_position(self, conn):
        _setup(conn)
        s1 = create_subtask(1, "A")
        s2 = create_subtask(1, "B")
        assert s1.position == 0
        assert s2.position == 1


class TestListSubtasks:
    def test_empty(self, conn):
        _setup(conn)
        assert list_subtasks(1) == []

    def test_ordered_by_position(self, conn):
        _setup(conn)
        s1 = create_subtask(1, "B")
        s2 = create_subtask(1, "A")
        items = list_subtasks(1)
        assert [s.content for s in items] == ["B", "A"]
        assert [s.position for s in items] == [0, 1]


class TestMarkDone:
    def test_mark_done(self, conn):
        _setup(conn)
        create_subtask(1, "Step 1")
        s = mark_done(1)
        assert s is not None
        assert s.finished is True

    def test_mark_done_nonexistent(self, conn):
        assert mark_done(999) is None


class TestMarkNotDone:
    def test_mark_not_done(self, conn):
        _setup(conn)
        create_subtask(1, "Step 1")
        mark_done(1)
        s = mark_not_done(1)
        assert s is not None
        assert s.finished is False

    def test_mark_not_done_nonexistent(self, conn):
        assert mark_not_done(999) is None


class TestUpdateSubtask:
    def test_update_content(self, conn):
        _setup(conn)
        create_subtask(1, "Old")
        s = update_subtask(1, "New")
        assert s is not None
        assert s.content == "New"

    def test_update_nonexistent(self, conn):
        assert update_subtask(999, "Ghost") is None


class TestDeleteSubtask:
    def test_delete(self, conn):
        _setup(conn)
        create_subtask(1, "Step 1")
        assert delete_subtask(1) is True
        assert list_subtasks(1) == []

    def test_delete_nonexistent(self, conn):
        assert delete_subtask(999) is False
