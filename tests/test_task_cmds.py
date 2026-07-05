import pytest
from datetime import date, timedelta

from taskwatch.archive_cmds import create_archive
from taskwatch.directory_cmds import create_directory
from taskwatch.task_cmds import (
    VALID_REPEAT_TYPES,
    _clamp,
    _display_date,
    _normalize_date,
    _validate_repeatable_type,
    create_task,
    delete_task,
    edit_task,
    get_task,
    list_tasks,
    mark_done,
    parse_natural_date,
    relative_deadline,
)


class TestClamp:
    def test_within_range(self):
        assert _clamp(3, 1, 5, "x") == 3

    def test_below_min(self):
        with pytest.raises(ValueError):
            _clamp(0, 1, 5, "x")

    def test_above_max(self):
        with pytest.raises(ValueError):
            _clamp(6, 1, 5, "x")


class TestNormalizeDate:
    def test_none(self):
        assert _normalize_date("none") == "none"

    def test_iso_format(self):
        assert _normalize_date("2026-07-04") == "2026-07-04"

    def test_dmy_format(self):
        assert _normalize_date("04/07/2026") == "2026-07-04"

    def test_invalid(self):
        with pytest.raises(ValueError):
            _normalize_date("not-a-date")

    def test_natural_language(self):
        assert _normalize_date("today") == date.today().isoformat()
        assert _normalize_date("tomorrow") == (date.today() + timedelta(days=1)).isoformat()
        assert _normalize_date("in 3 days") == (date.today() + timedelta(days=3)).isoformat()


class TestParseNaturalDate:
    def test_today(self):
        assert parse_natural_date("today") == date.today().isoformat()

    def test_tdy(self):
        assert parse_natural_date("tdy") == date.today().isoformat()

    def test_tomorrow(self):
        expected = (date.today() + timedelta(days=1)).isoformat()
        assert parse_natural_date("tomorrow") == expected
        assert parse_natural_date("tmr") == expected

    def test_in_days(self):
        expected = (date.today() + timedelta(days=3)).isoformat()
        assert parse_natural_date("in 3 days") == expected
        assert parse_natural_date("in 1 day") == (date.today() + timedelta(days=1)).isoformat()

    def test_in_weeks(self):
        expected = (date.today() + timedelta(weeks=2)).isoformat()
        assert parse_natural_date("in 2 weeks") == expected

    def test_next_week(self):
        expected = (date.today() + timedelta(weeks=1)).isoformat()
        assert parse_natural_date("next week") == expected

    def test_next_weekday(self):
        today_idx = date.today().weekday()
        friday_idx = 4
        days_ahead = friday_idx - today_idx
        if days_ahead <= 0:
            days_ahead += 7
        expected = (date.today() + timedelta(days=days_ahead)).isoformat()
        assert parse_natural_date("next friday") == expected

    def test_unrecognized(self):
        assert parse_natural_date("invalid string") is None
        assert parse_natural_date("") is None

    def test_case_insensitive(self):
        assert parse_natural_date("TOMORROW") == (date.today() + timedelta(days=1)).isoformat()


class TestRelativeDeadline:
    def test_none_and_empty(self):
        assert relative_deadline(None) == ""
        assert relative_deadline("") == ""
        assert relative_deadline("none") == ""

    def test_due_today(self):
        assert relative_deadline(date.today().isoformat()) == "Due today"

    def test_due_tomorrow(self):
        tomorrow = (date.today() + timedelta(days=1)).isoformat()
        assert relative_deadline(tomorrow) == "Due tomorrow"

    def test_due_in_days(self):
        d = (date.today() + timedelta(days=3)).isoformat()
        assert relative_deadline(d) == "Due in 3 days"

    def test_due_in_1_week(self):
        d = (date.today() + timedelta(weeks=1)).isoformat()
        assert relative_deadline(d) == "Due in 1 week"

    def test_due_in_multiple_weeks(self):
        d = (date.today() + timedelta(weeks=3)).isoformat()
        assert relative_deadline(d) == "Due in 3 weeks"

    def test_overdue_one_day(self):
        d = (date.today() - timedelta(days=1)).isoformat()
        assert relative_deadline(d) == "Overdue by 1 day"

    def test_overdue_multi_day(self):
        d = (date.today() - timedelta(days=3)).isoformat()
        assert relative_deadline(d) == "Overdue by 3 days"


class TestDisplayDate:
    def test_none_values(self):
        assert _display_date("none") == "\u2014"
        assert _display_date(None) == "\u2014"
        assert _display_date("") == "\u2014"

    def test_iso_to_dmy(self):
        assert _display_date("2026-07-04") == "04/07/2026"


class TestValidateRepeatableType:
    def test_valid_types(self):
        for t in VALID_REPEAT_TYPES:
            _validate_repeatable_type(t)

    def test_case_insensitive(self):
        assert _validate_repeatable_type("WEEKLY") == "weekly"

    def test_invalid(self):
        with pytest.raises(ValueError):
            _validate_repeatable_type("invalid")

    def test_error_message(self):
        with pytest.raises(ValueError) as exc:
            _validate_repeatable_type("bogus")
        assert "bogus" in str(exc.value)


class TestTaskCrud:
    def _setup(self, conn):
        create_archive("Test Archive")
        create_directory(1, "Test Dir")

    def test_create_task(self, conn):
        self._setup(conn)
        t = create_task(1, "My Task", deadline="2026-12-31",
                        urgency=3, difficulty=2, time_dedicated=60)
        assert t.id == 1
        assert t.name == "My Task"
        assert t.urgency == 3
        assert t.difficulty == 2
        assert t.time_dedicated == 60
        assert t.deadline == "2026-12-31"

    def test_create_repeatable_task(self, conn):
        self._setup(conn)
        t = create_task(1, "Daily", repeatable=True, repeatable_type="daily")
        assert t.repeatable is True
        assert t.repeatable_type == "daily"

    def test_create_duplicate_raises(self, conn):
        self._setup(conn)
        create_task(1, "Unique")
        with pytest.raises(ValueError):
            create_task(1, "Unique")

    def test_list_tasks(self, conn):
        self._setup(conn)
        create_task(1, "A")
        create_task(1, "B")
        tasks = list_tasks(directory_id=1)
        assert len(tasks) == 2
        assert [t.name for t in tasks] == ["A", "B"]

    def test_list_tasks_finished_filter(self, conn):
        self._setup(conn)
        create_task(1, "A")
        t = create_task(1, "B")
        mark_done(t.id)
        pending = list_tasks(directory_id=1, finished=False)
        done = list_tasks(directory_id=1, finished=True)
        assert len(pending) == 1
        assert len(done) == 1

    def test_get_task(self, conn):
        self._setup(conn)
        create_task(1, "Find Me")
        t = get_task(1)
        assert t is not None
        assert t.name == "Find Me"

    def test_get_missing_task(self, conn):
        assert get_task(999) is None

    def test_edit_task(self, conn):
        self._setup(conn)
        create_task(1, "Old Name")
        updated = edit_task(1, name="New Name", urgency=5)
        assert updated is not None
        assert updated.name == "New Name"
        assert updated.urgency == 5

    def test_mark_done(self, conn):
        self._setup(conn)
        create_task(1, "Do It")
        done = mark_done(1)
        assert done is not None
        assert done.finished is True
        t = get_task(1)
        assert t.finished is True
        assert t.finished_date != "none"

    def test_mark_done_repeatable(self, conn):
        self._setup(conn)
        t = create_task(1, "Repeat", deadline="2026-07-06",
                        repeatable=True, repeatable_type="daily")
        done = mark_done(t.id)
        assert done.finished is True
        assert done.deadline >= "2026-07-06"

    def test_mark_done_repeatable_advances(self, conn):
        self._setup(conn)
        t = create_task(1, "Weekly", deadline="2026-07-06",
                        repeatable=True, repeatable_type="weekly")
        done = mark_done(t.id)
        assert done.finished is True
        assert done.deadline > "2026-07-06"

    def test_delete_task(self, conn):
        self._setup(conn)
        create_task(1, "Delete Me")
        assert delete_task(1) is True
        assert get_task(1) is None


class TestDirectoryDefaults:
    def _setup(self, conn):
        create_archive("Test Archive")
        create_directory(1, "Test Dir")

    def test_empty_directory_returns_one(self, conn):
        self._setup(conn)
        from taskwatch.directory_cmds import get_directory_defaults
        d = get_directory_defaults(1)
        assert d["urgency"] == 1
        assert d["difficulty"] == 1

    def test_averages(self, conn):
        self._setup(conn)
        create_task(1, "A", urgency=3, difficulty=4)
        create_task(1, "B", urgency=5, difficulty=2)
        from taskwatch.directory_cmds import get_directory_defaults
        d = get_directory_defaults(1)
        assert d["urgency"] == 4  # (3+5)/2 = 4
        assert d["difficulty"] == 3  # (4+2)/2 = 3


class TestStreakAndHeatmap:
    def _setup(self, conn):
        create_archive("Test Archive")
        create_directory(1, "Test Dir")

    def test_streak_zero_when_no_tasks(self, conn):
        self._setup(conn)
        from taskwatch.stats_cmds import get_completion_streak
        assert get_completion_streak() == 0

    def test_streak_one_today(self, conn):
        self._setup(conn)
        t = create_task(1, "Task A")
        from taskwatch.task_cmds import mark_done
        mark_done(t.id)
        from taskwatch.stats_cmds import get_completion_streak
        assert get_completion_streak() >= 1

    def test_heatmap_returns_grid(self, conn):
        self._setup(conn)
        from taskwatch.stats_cmds import get_completion_heatmap
        grid = get_completion_heatmap(12)
        assert len(grid) == 7
        assert len(grid[0]) == 12
