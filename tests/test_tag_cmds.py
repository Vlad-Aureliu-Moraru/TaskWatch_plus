import pytest

from taskwatch.archive_cmds import create_archive
from taskwatch.directory_cmds import create_directory
from taskwatch.tag_cmds import (
    add_tag_to_task,
    create_tag,
    delete_tag,
    get_tags_for_task,
    get_tasks_by_tag,
    list_tags,
    remove_tag_from_task,
    search_tags_global,
)
from taskwatch.task_cmds import create_task


def _setup(conn):
    create_archive("Test Archive")
    create_directory(1, "Test Dir")
    create_task(1, "Test Task")


class TestCreateTag:
    def test_create(self, conn):
        t = create_tag("urgent")
        assert t.id == 1
        assert t.name == "urgent"

    def test_create_trims_whitespace(self, conn):
        t = create_tag("  urgent  ")
        assert t.name == "urgent"

    def test_duplicate_returns_existing(self, conn):
        t1 = create_tag("urgent")
        t2 = create_tag("urgent")
        assert t2.id == t1.id
        assert t2.name == "urgent"


class TestListTags:
    def test_empty(self, conn):
        assert list_tags() == []

    def test_ordered_by_name(self, conn):
        create_tag("z")
        create_tag("a")
        create_tag("m")
        names = [t.name for t in list_tags()]
        assert names == ["a", "m", "z"]


class TestDeleteTag:
    def test_delete(self, conn):
        create_tag("urgent")
        assert delete_tag(1) is True
        assert list_tags() == []

    def test_delete_nonexistent(self, conn):
        assert delete_tag(999) is False


class TestSearchTagsGlobal:
    def test_search(self, conn):
        create_tag("high priority")
        create_tag("low priority")
        results = search_tags_global("high")
        assert len(results) == 1
        assert results[0].name == "high priority"

    def test_case_insensitive(self, conn):
        create_tag("Urgent")
        results = search_tags_global("urgent")
        assert len(results) == 1

    def test_no_match(self, conn):
        create_tag("urgent")
        assert search_tags_global("zzz") == []


class TestAddTagToTask:
    def test_add(self, conn):
        _setup(conn)
        t = add_tag_to_task(1, "urgent")
        assert t is not None
        assert t.name == "urgent"

    def test_add_creates_tag_if_missing(self, conn):
        _setup(conn)
        t = add_tag_to_task(1, "new_tag")
        assert t is not None
        assert t.name == "new_tag"
        tags = list_tags()
        assert len(tags) == 1

    def test_add_duplicate_is_idempotent(self, conn):
        _setup(conn)
        add_tag_to_task(1, "urgent")
        add_tag_to_task(1, "urgent")
        tags = get_tags_for_task(1)
        assert len(tags) == 1


class TestRemoveTagFromTask:
    def test_remove(self, conn):
        _setup(conn)
        add_tag_to_task(1, "urgent")
        assert remove_tag_from_task(1, "urgent") is True
        assert get_tags_for_task(1) == []

    def test_remove_nonexistent_tag(self, conn):
        _setup(conn)
        assert remove_tag_from_task(1, "ghost") is False

    def test_remove_not_attached(self, conn):
        _setup(conn)
        create_tag("urgent")
        assert remove_tag_from_task(1, "urgent") is False


class TestGetTagsForTask:
    def test_multiple_tags(self, conn):
        _setup(conn)
        add_tag_to_task(1, "urgent")
        add_tag_to_task(1, "bug")
        tags = get_tags_for_task(1)
        names = sorted(t.name for t in tags)
        assert names == ["bug", "urgent"]

    def test_no_tags(self, conn):
        _setup(conn)
        assert get_tags_for_task(1) == []


class TestGetTasksByTag:
    def test_get_tasks(self, conn):
        _setup(conn)
        create_task(1, "Task 2")
        add_tag_to_task(1, "urgent")
        add_tag_to_task(2, "urgent")
        add_tag_to_task(2, "bug")
        task_ids = get_tasks_by_tag("urgent")
        assert sorted(task_ids) == [1, 2]

    def test_no_tasks_for_tag(self, conn):
        _setup(conn)
        create_tag("orphan")
        assert get_tasks_by_tag("orphan") == []

    def test_nonexistent_tag(self, conn):
        _setup(conn)
        assert get_tasks_by_tag("ghost") == []
