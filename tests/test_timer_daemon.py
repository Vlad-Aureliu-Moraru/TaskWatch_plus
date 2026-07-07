import json
from pathlib import Path
from unittest.mock import patch

import pytest

from taskwatch.timer_daemon import (
    _atomic_write,
    _clear_timer_file,
    _read_state,
    _write_timer_file,
)


class TestAtomicWrite:
    def test_writes_file(self, tmp_path):
        p = tmp_path / "state.json"
        with patch("taskwatch.timer_daemon.STATE_PATH", p):
            _atomic_write({"running": True})
            data = json.loads(p.read_text())
            assert data["running"] is True

    def test_writes_then_renames(self, tmp_path):
        p = tmp_path / "state.json"
        with patch("taskwatch.timer_daemon.STATE_PATH", p):
            _atomic_write({"key": "val"})
            assert p.exists()
            # No .tmp file should remain
            assert not p.with_suffix(".tmp").exists()


class TestReadState:
    def test_no_file(self, tmp_path):
        p = tmp_path / "nonexistent.json"
        with patch("taskwatch.timer_daemon.STATE_PATH", p):
            assert _read_state() == {}

    def test_bad_json(self, tmp_path):
        p = tmp_path / "bad.json"
        p.write_text("not json")
        with patch("taskwatch.timer_daemon.STATE_PATH", p):
            assert _read_state() == {}

    def test_reads_file(self, tmp_path):
        p = tmp_path / "state.json"
        p.write_text(json.dumps({"running": True}))
        with patch("taskwatch.timer_daemon.STATE_PATH", p):
            state = _read_state()
            assert state["running"] is True

    def test_reads_stopped_flag(self, tmp_path):
        p = tmp_path / "state.json"
        p.write_text(json.dumps({"stopped": True}))
        with patch("taskwatch.timer_daemon.STATE_PATH", p):
            state = _read_state()
            assert state["stopped"] is True


class TestWriteTimerFile:
    def test_writes_simple_mode(self, tmp_path):
        p = tmp_path / "timer.json"
        with patch("taskwatch.timer_daemon.TIMER_FILE_PATH", p):
            _write_timer_file(300, 0, False, "simple")
            data = json.loads(p.read_text())
            assert "text" in data
            assert "⏱" in data["text"]
            assert data["class"] == "timer-timer"

    def test_writes_paused(self, tmp_path):
        p = tmp_path / "timer.json"
        with patch("taskwatch.timer_daemon.TIMER_FILE_PATH", p):
            _write_timer_file(120, 1, True, "scheduled")
            data = json.loads(p.read_text())
            assert "⏸" in data["text"]
            assert data["class"] == "timer-work"

    def test_writes_intro_phase(self, tmp_path):
        p = tmp_path / "timer.json"
        with patch("taskwatch.timer_daemon.TIMER_FILE_PATH", p):
            _write_timer_file(15, 0, False, "scheduled")
            data = json.loads(p.read_text())
            assert data["alt"] == "INTRO"

    def test_writes_break_phase(self, tmp_path):
        p = tmp_path / "timer.json"
        with patch("taskwatch.timer_daemon.TIMER_FILE_PATH", p):
            _write_timer_file(60, 2, False, "scheduled")
            data = json.loads(p.read_text())
            assert data["alt"] == "BREAK"


class TestClearTimerFile:
    def test_clears(self, tmp_path):
        p = tmp_path / "timer.json"
        p.write_text(json.dumps({"text": "old"}))
        with patch("taskwatch.timer_daemon.TIMER_FILE_PATH", p):
            _clear_timer_file()
            data = json.loads(p.read_text())
            assert data["class"] == "inactive"
