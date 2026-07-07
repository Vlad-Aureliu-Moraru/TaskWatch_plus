import json
from pathlib import Path
from unittest.mock import patch

import pytest

from taskwatch.models import Task
from taskwatch.timer import (
    _fmt_duration,
    atomic_write_json,
    compute_schedule,
    fmt_timer_val,
    format_schedule,
    parse_time_string,
    read_presets,
    write_presets,
)


class TestFmtDuration:
    def test_seconds_only(self):
        assert _fmt_duration(45) == "0m45s"

    def test_minutes(self):
        assert _fmt_duration(125) == "2m05s"

    def test_hours(self):
        assert _fmt_duration(3661) == "1h01m01s"


class TestComputeSchedule:
    def test_requires_time_dedicated(self):
        t = Task(id=1, directory_id=1, name="No time", time_dedicated=0)
        result = compute_schedule(t)
        assert "error" in result

    def test_typical_schedule(self):
        t = Task(id=1, directory_id=1, name="Work",
                 time_dedicated=120, urgency=3, difficulty=3)
        result = compute_schedule(t)
        assert "error" not in result
        assert result["total_minutes"] == 120
        assert result["total_seconds"] == 7200
        assert result["difficulty"] == 3
        assert result["urgency"] == 3
        assert result["segment_count"] > 0
        assert result["working_seconds"] > 0
        assert result["segments"][0] == 15

    def test_urgency_difficulty_clamping(self):
        t = Task(id=1, directory_id=1, name="Out of range",
                 time_dedicated=60, urgency=10, difficulty=10)
        result = compute_schedule(t)
        assert "error" not in result
        assert result["urgency"] == 5
        assert result["difficulty"] == 5

    def test_negative_clamping(self):
        t = Task(id=1, directory_id=1, name="Negative",
                 time_dedicated=60, urgency=0, difficulty=0)
        result = compute_schedule(t)
        assert "error" not in result
        assert result["urgency"] == 1
        assert result["difficulty"] == 1

    def test_segments_structure(self):
        t = Task(id=1, directory_id=1, name="Test",
                 time_dedicated=30, urgency=2, difficulty=2)
        result = compute_schedule(t)
        segs = result["segments"]
        assert len(segs) > 0
        assert sum(segs) == result["total_seconds"]

    def test_segment_count_equals_2x_difficulty_plus_one(self):
        t = Task(id=1, directory_id=1, name="S",
                 time_dedicated=60, urgency=3, difficulty=4)
        result = compute_schedule(t)
        assert result["segment_count"] == 1 + 2 * result["difficulty"]

    def test_intro_adjusts_when_small_time(self):
        t = Task(id=1, directory_id=1, name="Short",
                 time_dedicated=1, urgency=1, difficulty=1)
        result = compute_schedule(t)
        assert "error" not in result
        assert result["segments"][0] <= 15


class TestFormatSchedule:
    def test_error_case(self):
        t = Task(id=1, directory_id=1, name="Error",
                 time_dedicated=0)
        output = format_schedule(t)
        assert output.startswith("Error:")

    def test_valid_schedule_output(self):
        t = Task(id=1, directory_id=1, name="My Task",
                 time_dedicated=60, urgency=2, difficulty=2)
        output = format_schedule(t)
        assert "My Task" in output
        assert "Total time:" in output
        assert "Segments:" in output


class TestParseTimeString:
    def test_bare_minutes(self):
        assert parse_time_string("45") == 45.0

    def test_negative_bare(self):
        assert parse_time_string("-45") == -45.0

    def test_hours(self):
        assert parse_time_string("1h") == 60.0

    def test_minutes_suffix(self):
        assert parse_time_string("30m") == 30.0

    def test_seconds(self):
        assert parse_time_string("15s") == 0.25

    def test_hours_and_minutes(self):
        assert parse_time_string("1h30m") == 90.0

    def test_hours_minutes_seconds(self):
        assert parse_time_string("1h30m15s") == 90.25

    def test_empty_string(self):
        with pytest.raises(ValueError, match="empty"):
            parse_time_string("")

    def test_unrecognized(self):
        with pytest.raises(ValueError, match="unrecognized"):
            parse_time_string("xyz")

    def test_whitespace_handling(self):
        assert parse_time_string("  30m  ") == 30.0


class TestFmtTimerVal:
    def test_integer(self):
        assert fmt_timer_val(5.0) == "5"

    def test_float(self):
        assert fmt_timer_val(5.5) == "5.5"

    def test_float_remove_trailing_zeros(self):
        assert fmt_timer_val(5.20) == "5.2"


class TestReadPresets:
    @patch("taskwatch.timer.CONFIG_PATH")
    def test_no_config_file(self, mock_cfg):
        mock_cfg.read_text.side_effect = OSError()
        assert read_presets() == {}

    @patch("taskwatch.timer.CONFIG_PATH")
    def test_reads_presets(self, mock_cfg):
        mock_cfg.read_text.return_value = (
            "TIMER_PRESET:focus=0,25,5,4\n"
            "TIMER_PRESET:quick=15\n"
            "OTHER_SETTING=xyz\n"
        )
        presets = read_presets()
        assert "focus" in presets
        assert presets["focus"]["prep"] == 0.0
        assert presets["focus"]["work"] == 25.0
        assert presets["focus"]["break"] == 5.0
        assert presets["focus"]["laps"] == 4
        assert "quick" in presets
        assert presets["quick"]["work"] == 15.0

    @patch("taskwatch.timer.CONFIG_PATH")
    def test_skips_malformed(self, mock_cfg):
        mock_cfg.read_text.return_value = "TIMER_PRESET:bad=not,enough,parts\n"
        assert read_presets() == {}


class TestWritePresets:
    @patch("taskwatch.timer.CONFIG_PATH")
    def test_writes_presets(self, mock_cfg):
        mock_cfg.read_text.return_value = "EXISTING=value\n"
        write_presets({"test": {"prep": 0.0, "work": 25.0, "break": 5.0, "laps": 4}})
        written = mock_cfg.write_text.call_args[0][0]
        assert "EXISTING=value" in written
        assert "TIMER_PRESET:test=0,25,5,4" in written

    @patch("taskwatch.timer.CONFIG_PATH")
    def test_preserves_non_timer_lines(self, mock_cfg):
        mock_cfg.read_text.return_value = "A=1\nTIMER_PRESET:old=10\nB=2\n"
        write_presets({"new": {"prep": 0, "work": 30, "break": 10, "laps": 3}})
        written = mock_cfg.write_text.call_args[0][0]
        assert "A=1" in written
        assert "B=2" in written
        assert "TIMER_PRESET:old=" not in written
        assert "TIMER_PRESET:new=0,30,10,3" in written

    @patch("taskwatch.timer.CONFIG_PATH")
    def test_handles_missing_config(self, mock_cfg):
        mock_cfg.read_text.side_effect = OSError()
        write_presets({"a": {"prep": 0, "work": 10, "break": 2, "laps": 1}})
        assert mock_cfg.write_text.called


class TestAtomicWriteJson:
    def test_writes_atomically(self, tmp_path):
        p = tmp_path / "test.json"
        atomic_write_json(p, {"key": "value"})
        data = json.loads(p.read_text())
        assert data["key"] == "value"

    def test_overwrites(self, tmp_path):
        p = tmp_path / "test.json"
        atomic_write_json(p, {"a": 1})
        atomic_write_json(p, {"b": 2})
        data = json.loads(p.read_text())
        assert data["b"] == 2
