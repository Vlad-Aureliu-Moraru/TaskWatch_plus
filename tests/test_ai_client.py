import json
from pathlib import Path
from unittest.mock import patch

import pytest

from taskwatch.ai_client import (
    MODELS,
    _build_action_reference,
    _build_archive_tree,
    add_provider,
    build_cli_context,
    chat,
    list_providers,
    load_config,
    parse_actions,
    remove_provider,
    save_config,
    test_provider as _test_provider_impl,
)


@pytest.fixture
def tmp_cfg(tmp_path):
    cfg_path = tmp_path / "ai_config.json"
    with patch("taskwatch.ai_client.AI_CONFIG_PATH", cfg_path):
        yield cfg_path


class TestLoadConfig:
    def test_no_file(self, tmp_cfg):
        cfg = load_config()
        assert "providers" in cfg
        assert cfg["providers"] == {}

    def test_loads_existing(self, tmp_cfg):
        tmp_cfg.write_text(json.dumps({"providers": {"groq": {"api_key": "sk-123"}}}))
        cfg = load_config()
        assert cfg["providers"]["groq"]["api_key"] == "sk-123"

    def test_bad_json_returns_defaults(self, tmp_cfg):
        tmp_cfg.write_text("not json")
        cfg = load_config()
        assert cfg["providers"] == {}


class TestSaveConfig:
    def test_saves(self, tmp_cfg):
        cfg = {"providers": {"groq": {"api_key": "sk-123"}}}
        save_config(cfg)
        saved = json.loads(tmp_cfg.read_text())
        assert saved["providers"]["groq"]["api_key"] == "sk-123"

    def test_sets_permissions(self, tmp_cfg):
        save_config({"providers": {}})
        assert tmp_cfg.stat().st_mode & 0o600 == 0o600


class TestAddProvider:
    def test_adds_provider(self, tmp_cfg):
        ok, msg = add_provider("groq", "sk-valid-key")
        assert ok is True
        assert "Added" in msg
        cfg = load_config()
        assert "groq" in cfg["providers"]

    def test_adds_to_fallback_order(self, tmp_cfg):
        add_provider("groq", "sk-key")
        cfg = load_config()
        assert "groq" in cfg["fallback_order"]

    def test_unknown_provider(self, tmp_cfg):
        ok, msg = add_provider("unknown", "key")
        assert ok is False
        assert "Unknown" in msg

    def test_empty_key(self, tmp_cfg):
        ok, msg = add_provider("groq", "")
        assert ok is False
        assert "empty" in msg


class TestRemoveProvider:
    def test_removes_provider(self, tmp_cfg):
        add_provider("groq", "sk-key")
        ok, msg = remove_provider("groq")
        assert ok is True
        assert "Removed" in msg
        cfg = load_config()
        assert "groq" not in cfg["providers"]

    def test_remove_nonexistent(self, tmp_cfg):
        ok, msg = remove_provider("ghost")
        assert ok is False
        assert "not configured" in msg

    def test_remove_from_fallback(self, tmp_cfg):
        add_provider("groq", "sk-key")
        remove_provider("groq")
        cfg = load_config()
        assert "groq" not in cfg["fallback_order"]


class TestListProviders:
    def test_empty(self, tmp_cfg):
        providers = list_providers()
        assert providers == []

    def test_masks_key(self, tmp_cfg):
        add_provider("groq", "sk-1234567890abcdef")
        providers = list_providers()
        assert len(providers) == 1
        assert providers[0]["name"] == "groq"
        assert providers[0]["key"] == "sk-1234567..."
        assert providers[0]["enabled"] is True

    def test_short_key_masked(self, tmp_cfg):
        add_provider("gemini", "abc")
        providers = list_providers()
        assert providers[0]["key"] == "***"


class TestParseActions:
    def test_create_task(self):
        text = ">>>ACTION:CREATE_TASK\nname: My Task\n<<<END"
        actions = parse_actions(text)
        assert len(actions) == 1
        assert actions[0]["type"] == "CREATE_TASK"
        assert actions[0]["name"] == "My Task"

    def test_multiple_actions(self):
        text = (
            ">>>ACTION:CREATE_TASK\nname: A\n<<<END\n"
            ">>>ACTION:FINISH_TASK\ntask_id: 1\n<<<END"
        )
        actions = parse_actions(text)
        assert len(actions) == 2

    def test_extra_text_before(self):
        text = "Here's what I'll do:\n>>>ACTION:CREATE_TASK\nname: T\n<<<END"
        actions = parse_actions(text)
        assert len(actions) == 1
        assert actions[0]["type"] == "CREATE_TASK"

    def test_action_without_end_collects_to_eof(self):
        text = ">>>ACTION:CREATE_TASK\nname: T\n"
        actions = parse_actions(text)
        assert len(actions) == 1
        assert actions[0]["type"] == "CREATE_TASK"

    def test_no_actions(self):
        assert parse_actions("Just a normal message") == []


class TestChat:
    def test_no_providers(self, tmp_cfg):
        text, provider, actions = chat([{"role": "user", "content": "hi"}])
        assert provider == ""
        assert "No AI providers" in text

    def test_all_providers_fail(self, tmp_cfg):
        add_provider("groq", "bad-key")
        text, provider, actions = chat([{"role": "user", "content": "hi"}])
        assert provider == ""
        assert "All providers failed" in text


class TestBuildArchiveTree:
    def test_empty(self, conn):
        tree = _build_archive_tree()
        assert any("0)" in line for line in tree)

    def test_with_data(self, conn):
        from taskwatch.archive_cmds import create_archive
        from taskwatch.directory_cmds import create_directory
        from taskwatch.task_cmds import create_task
        create_archive("Work")
        create_directory(1, "Projects")
        create_task(1, "Task A")
        tree = _build_archive_tree()
        combined = "\n".join(tree)
        assert "Work" in combined
        assert "Projects" in combined
        assert "Task" not in combined  # task detail not in tree, only count


class TestBuildActionReference:
    def test_includes_keywords(self):
        lines = _build_action_reference()
        text = "\n".join(lines)
        assert ">>>ACTION:CREATE_TASK" in text
        assert ">>>ACTION:FINISH_TASK" in text
        assert ">>>ACTION:ADD_NOTE" in text
        assert ">>>ACTION:CREATE_ARCHIVE" in text
        assert ">>>ACTION:CREATE_DIRECTORY" in text


class TestBuildCliContext:
    def test_empty(self, conn):
        context = build_cli_context()
        assert "Archives" in context
        assert ">>>ACTION:" in context

    def test_with_data(self, conn):
        from taskwatch.archive_cmds import create_archive
        from taskwatch.directory_cmds import create_directory
        create_archive("Test")
        create_directory(1, "Dir")
        context = build_cli_context()
        assert "Test" in context
        assert "Dir" in context


class TestTestProvider:
    @patch("taskwatch.ai_client.urllib.request.urlopen")
    def test_unknown_provider(self, mock_urlopen, tmp_cfg):
        ok, msg = _test_provider_impl("unknown", "key")
        assert ok is False
        assert "Unknown" in msg

    @patch("taskwatch.ai_client.urllib.request.urlopen")
    def test_empty_key(self, mock_urlopen, tmp_cfg):
        ok, msg = _test_provider_impl("groq", "")
        assert ok is False
        assert "empty" in msg
