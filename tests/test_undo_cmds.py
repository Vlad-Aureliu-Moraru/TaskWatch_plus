from taskwatch.archive_cmds import create_archive
from taskwatch.directory_cmds import create_directory
from taskwatch.task_cmds import create_task, delete_task, get_task, mark_done
from taskwatch.undo_cmds import get_task_data, pop, push, restore_task


class TestPushPop:
    def test_push_and_pop(self):
        push("create", {"id": 1})
        item = pop()
        assert item is not None
        assert item["action"] == "create"
        assert item["data"]["id"] == 1

    def test_pop_empty_stack(self):
        assert pop() is None

    def test_pop_returns_last(self):
        push("a", {})
        push("b", {})
        item = pop()
        assert item["action"] == "b"
        assert pop()["action"] == "a"
        assert pop() is None

    def test_max_undo_size(self):
        for i in range(60):
            push("x", {"n": i})
        # Should only keep latest 50
        count = 0
        while pop():
            count += 1
        assert count == 50


class TestGetTaskData:
    def _setup(self, conn):
        create_archive("Test Archive")
        create_directory(1, "Test Dir")

    def test_existing_task(self, conn):
        self._setup(conn)
        create_task(1, "My Task", deadline="2026-12-31", urgency=3, difficulty=2)
        data = get_task_data(1)
        assert data is not None
        assert data["name"] == "My Task"
        assert data["deadline"] == "2026-12-31"
        assert data["urgency"] == 3
        assert data["difficulty"] == 2

    def test_nonexistent_task(self, conn):
        assert get_task_data(999) is None


class TestRestoreTask:
    def _setup(self, conn):
        create_archive("Test Archive")
        create_directory(1, "Test Dir")

    def test_restore_deleted_task(self, conn):
        self._setup(conn)
        create_task(1, "Restore Me")
        data = get_task_data(1)
        delete_task(1)
        assert get_task(1) is None
        assert restore_task(data) is True
        t = get_task(1)
        assert t is not None
        assert t.name == "Restore Me"

    def test_restore_already_exists_returns_false(self, conn):
        self._setup(conn)
        create_task(1, "Task")
        data = get_task_data(1)
        assert restore_task(data) is False

    def test_restore_with_nonexistent_directory(self, conn):
        self._setup(conn)
        data = {
            "id": 1, "directory_id": 999, "name": "Ghost",
            "description": "", "deadline": "none", "urgency": 1,
            "difficulty": 1, "time_dedicated": 0, "repeatable": False,
            "repeatable_type": "none", "finished": False,
            "finished_date": "none", "has_to_be_completed_to_repeat": True,
            "repeat_on_specific_day": "none", "position": 0, "pinned": False,
        }
        assert restore_task(data) is False

    def test_restore_with_notes(self, conn):
        self._setup(conn)
        create_task(1, "Task")
        from taskwatch.note_cmds import create_note
        create_note(1, "2026-07-04", "My note")
        data = get_task_data(1)
        data["notes"] = [{"id": 1, "task_id": 1, "date": "2026-07-04",
                          "note": "My note", "file_path": None, "created_at": ""}]
        delete_task(1)
        assert restore_task(data) is True
        from taskwatch.note_cmds import list_notes
        notes = list_notes(task_id=1)
        assert len(notes) == 1
        assert notes[0].note == "My note"

    def test_restore_with_subtasks(self, conn):
        self._setup(conn)
        create_task(1, "Task")
        from taskwatch.subtask_cmds import create_subtask
        create_subtask(1, "Step 1")
        data = get_task_data(1)
        data["subtasks"] = [{"id": 1, "task_id": 1, "content": "Step 1",
                             "finished": 0, "position": 0}]
        delete_task(1)
        assert restore_task(data) is True
        from taskwatch.subtask_cmds import list_subtasks
        subs = list_subtasks(1)
        assert len(subs) == 1

    def test_restore_missing_task_fields(self, conn):
        self._setup(conn)
        data = {
            "id": 1, "directory_id": 1, "name": "Minimal",
        }
        assert restore_task(data) is True
        t = get_task(1)
        assert t is not None
        assert t.description == ""
        assert t.deadline == "none"

    def test_double_restore_fails(self, conn):
        self._setup(conn)
        create_task(1, "Task")
        data = get_task_data(1)
        delete_task(1)
        restore_task(data)
        assert restore_task(data) is False
