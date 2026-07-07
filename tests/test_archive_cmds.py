import pytest

from taskwatch.archive_cmds import (
    create_archive,
    delete_archive,
    get_archive,
    list_archives,
    rename_archive,
)


class TestCreateArchive:
    def test_create(self, conn):
        a = create_archive("Work")
        assert a is not None
        assert a.id == 1
        assert a.name == "Work"

    def test_duplicate_name_returns_none(self, conn):
        create_archive("Work")
        a = create_archive("Work")
        assert a is None

    def test_multiple_archives(self, conn):
        a1 = create_archive("Work")
        a2 = create_archive("Personal")
        assert a1.id == 1
        assert a2.id == 2


class TestListArchives:
    def test_empty(self, conn):
        assert list_archives() == []

    def test_returns_all(self, conn):
        create_archive("A")
        create_archive("B")
        names = [a.name for a in list_archives()]
        assert names == ["A", "B"]


class TestGetArchive:
    def test_existing(self, conn):
        create_archive("Work")
        a = get_archive(1)
        assert a is not None
        assert a.name == "Work"

    def test_missing(self, conn):
        assert get_archive(999) is None


class TestRenameArchive:
    def test_rename(self, conn):
        create_archive("Work")
        a = rename_archive(1, "Job")
        assert a is not None
        assert a.name == "Job"

    def test_rename_nonexistent(self, conn):
        a = rename_archive(999, "Ghost")
        assert a is None

    def test_rename_to_duplicate(self, conn):
        create_archive("Work")
        create_archive("Personal")
        a = rename_archive(2, "Work")
        assert a is None

    def test_rename_same_name(self, conn):
        create_archive("Work")
        a = rename_archive(1, "Work")
        assert a is not None


class TestDeleteArchive:
    def test_delete(self, conn):
        create_archive("Work")
        assert delete_archive(1) is True
        assert get_archive(1) is None

    def test_delete_nonexistent(self, conn):
        assert delete_archive(999) is False

    def test_list_after_delete(self, conn):
        create_archive("A")
        create_archive("B")
        delete_archive(1)
        assert [a.name for a in list_archives()] == ["B"]
