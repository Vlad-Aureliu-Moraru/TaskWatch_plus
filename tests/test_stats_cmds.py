from datetime import date, timedelta

from taskwatch.archive_cmds import create_archive
from taskwatch.directory_cmds import create_directory
from taskwatch.stats_cmds import (
    all_directory_stats,
    compute_stats,
    directory_stats,
)
from taskwatch.task_cmds import create_task, mark_done


def _setup(conn):
    create_archive("Test Archive")
    create_directory(1, "Test Dir")


class TestComputeStats:
    def test_empty_database(self, conn):
        s = compute_stats()
        assert s["total"] == 0
        assert s["finished"] == 0
        assert s["pending"] == 0
        assert s["completion_pct"] == 0
        assert s["today_completed"] == 0
        assert s["overdue"] == 0
        assert s["total_time"] == 0
        assert s["total_tags"] == 0
        assert s["streak"] == 0
        assert s["focus_score"] == 0

    def test_counts(self, conn):
        _setup(conn)
        create_task(1, "A", time_dedicated=30, deadline="2026-07-07")
        create_task(1, "B", time_dedicated=60, deadline="2026-07-01")
        mark_done(1)
        s = compute_stats()
        assert s["total"] == 2
        assert s["finished"] == 1
        assert s["pending"] == 1
        assert s["total_time"] == 90
        assert s["overdue"] == 1
        assert s["completion_pct"] == 50

    def test_today_completed(self, conn):
        _setup(conn)
        create_task(1, "A")
        mark_done(1)
        s = compute_stats()
        assert s["today_completed"] == 1

    def test_completed_this_week(self, conn):
        _setup(conn)
        create_task(1, "A")
        mark_done(1)
        s = compute_stats()
        assert s["completed_this_week"] >= 1

    def test_ud_grid(self, conn):
        _setup(conn)
        create_task(1, "A", urgency=5, difficulty=4)
        create_task(1, "B", urgency=1, difficulty=1)
        create_task(1, "C", urgency=3, difficulty=3)
        mark_done(3)
        s = compute_stats()
        # Completed tasks excluded from grid
        assert s["ud_grid"][4][3] == 1  # urgency=5, difficulty=4 (0-indexed)
        assert s["ud_grid"][0][0] == 1  # urgency=1, difficulty=1
        assert s["ud_grid"][2][2] == 0  # urgency=3, diff=3 task is done
        assert sum(sum(row) for row in s["ud_grid"]) == 2

    def test_deadline_timeline(self, conn):
        _setup(conn)
        today_str = date.today().isoformat()
        # "this week" = > today and <= this coming Sunday
        in_2_days = (date.today() + timedelta(days=2)).isoformat()
        in_14_days = (date.today() + timedelta(days=14)).isoformat()
        create_task(1, "Overdue", deadline="2020-01-01")
        create_task(1, "Today", deadline=today_str)
        create_task(1, "Soon", deadline=in_2_days)
        create_task(1, "Later", deadline=in_14_days)
        create_task(1, "No deadline")
        tl = compute_stats()["deadline_timeline"]
        assert tl["overdue"] == 1
        assert tl["due_today"] == 1
        assert tl["this_week"] == 1
        assert tl["later"] >= 1
        assert tl["no_deadline"] == 1

    def test_archive_stats(self, conn):
        _setup(conn)
        create_archive("Empty Archive")
        create_task(1, "A")
        create_task(1, "B")
        mark_done(1)
        stats = compute_stats()["archive_stats"]
        names = [a["name"] for a in stats]
        assert "Test Archive" in names
        assert "Empty Archive" in names
        for a in stats:
            if a["name"] == "Test Archive":
                assert a["total"] == 2
                assert a["done"] == 1
                assert a["pct"] == 50
            if a["name"] == "Empty Archive":
                assert a["total"] == 0
                assert a["pct"] == 0

    def test_focus_score(self, conn):
        _setup(conn)
        s = compute_stats()
        assert s["focus_score"] == 0


class TestDirectoryStats:
    def test_empty_directory(self, conn):
        _setup(conn)
        total, done = directory_stats(1)
        assert total == 0
        assert done == 0

    def test_counts(self, conn):
        _setup(conn)
        create_task(1, "A")
        create_task(1, "B")
        create_task(1, "C")
        mark_done(1)
        mark_done(2)
        total, done = directory_stats(1)
        assert total == 3
        assert done == 2

    def test_nonexistent_directory(self, conn):
        total, done = directory_stats(999)
        assert total == 0
        assert done == 0

    def test_mixed_directories(self, conn):
        _setup(conn)
        create_archive("Personal")
        create_directory(2, "Personal Dir")
        create_task(1, "A")
        create_task(2, "B")
        mark_done(1)
        t1, d1 = directory_stats(1)
        assert t1 == 1
        assert d1 == 1
        t2, d2 = directory_stats(2)
        assert t2 == 1
        assert d2 == 0


class TestAllDirectoryStats:
    def test_empty(self, conn):
        assert all_directory_stats() == []

    def test_stats(self, conn):
        _setup(conn)
        create_task(1, "A")
        create_task(1, "B")
        mark_done(1)
        stats = all_directory_stats()
        assert len(stats) == 1
        assert stats[0]["total"] == 2
        assert stats[0]["done"] == 1
        assert stats[0]["pct"] == 50
        assert "Test Archive" in stats[0]["name"]
        assert "Test Dir" in stats[0]["name"]

    def test_archive_name_included(self, conn):
        _setup(conn)
        stats = all_directory_stats()
        assert ">" in stats[0]["name"]
