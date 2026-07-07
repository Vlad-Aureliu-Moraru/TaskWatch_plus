import pytest

from taskwatch.archive_cmds import create_archive
from taskwatch.directory_cmds import (
    create_directory,
    delete_directory,
    get_directory,
    list_directories,
    move_directory,
    rename_directory,
    search_directories_global,
)


def _setup(conn):
    create_archive("Test Archive")


class TestCreateDirectory:
    def test_create(self, conn):
        _setup(conn)
        d = create_directory(1, "Projects")
        assert d is not None
        assert d.id == 1
        assert d.archive_id == 1
        assert d.name == "Projects"

    def test_duplicate_name_in_archive(self, conn):
        _setup(conn)
        create_directory(1, "Projects")
        d = create_directory(1, "Projects")
        assert d is None

    def test_same_name_different_archive(self, conn):
        _setup(conn)
        create_archive("Personal")
        d1 = create_directory(1, "Projects")
        d2 = create_directory(2, "Projects")
        assert d1 is not None
        assert d2 is not None

    def test_nonexistent_archive(self, conn):
        d = create_directory(999, "Orphan")
        assert d is None


class TestListDirectories:
    def test_empty(self, conn):
        assert list_directories() == []

    def test_all(self, conn):
        _setup(conn)
        create_directory(1, "A")
        create_directory(1, "B")
        names = [d.name for d in list_directories()]
        assert names == ["A", "B"]

    def test_filter_by_archive(self, conn):
        _setup(conn)
        create_archive("Personal")
        create_directory(1, "WorkDir")
        create_directory(2, "PersonalDir")
        names = [d.name for d in list_directories(archive_id=1)]
        assert names == ["WorkDir"]
        names = [d.name for d in list_directories(archive_id=2)]
        assert names == ["PersonalDir"]


class TestGetDirectory:
    def test_existing(self, conn):
        _setup(conn)
        create_directory(1, "Projects")
        d = get_directory(1)
        assert d is not None
        assert d.name == "Projects"

    def test_missing(self, conn):
        assert get_directory(999) is None


class TestRenameDirectory:
    def test_rename(self, conn):
        _setup(conn)
        create_directory(1, "Old")
        d = rename_directory(1, "New")
        assert d is not None
        assert d.name == "New"

    def test_rename_nonexistent(self, conn):
        d = rename_directory(999, "Ghost")
        assert d is None

    def test_rename_to_duplicate(self, conn):
        _setup(conn)
        create_directory(1, "A")
        create_directory(1, "B")
        d = rename_directory(2, "A")
        assert d is None


class TestDeleteDirectory:
    def test_delete(self, conn):
        _setup(conn)
        create_directory(1, "Projects")
        assert delete_directory(1) is True
        assert get_directory(1) is None

    def test_delete_nonexistent(self, conn):
        assert delete_directory(999) is False


class TestSearchDirectoriesGlobal:
    def test_search(self, conn):
        _setup(conn)
        create_directory(1, "Work Projects")
        create_directory(1, "Personal")
        results = search_directories_global("Proj")
        assert len(results) == 1
        assert results[0].name == "Work Projects"

    def test_case_insensitive(self, conn):
        _setup(conn)
        create_directory(1, "Work Projects")
        results = search_directories_global("work")
        assert len(results) == 1

    def test_search_limit(self, conn):
        _setup(conn)
        for i in range(5):
            create_directory(1, f"Dir {i}")
        results = search_directories_global("Dir", limit=3)
        assert len(results) == 3

    def test_no_match(self, conn):
        _setup(conn)
        create_directory(1, "Projects")
        assert search_directories_global("Zzz") == []


class TestMoveDirectory:
    def test_move(self, conn):
        _setup(conn)
        create_archive("Personal")
        create_directory(1, "Projects")
        d = move_directory(1, 2)
        assert d is not None
        assert d.archive_id == 2

    def test_move_to_nonexistent_archive(self, conn):
        _setup(conn)
        create_directory(1, "Projects")
        d = move_directory(1, 999)
        assert d is None

    def test_move_nonexistent(self, conn):
        _setup(conn)
        create_archive("Personal")
        d = move_directory(999, 2)
        assert d is None
