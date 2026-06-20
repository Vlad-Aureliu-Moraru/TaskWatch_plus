from __future__ import annotations

from collections.abc import Callable
from datetime import date, datetime
from enum import Enum, auto
from functools import partial

import urwid
from urwid import (
    AttrMap,
    Columns,
    Edit,
    ExitMainLoop,
    Frame,
    LineBox,
    ListBox,
    MainLoop,
    Overlay,
    SimpleFocusListWalker,
    Text,
    Widget,
)

from . import archive_cmds, directory_cmds, note_cmds, task_cmds, timer as timer_mod


class Level(Enum):
    ARCHIVES = auto()
    DIRECTORIES = auto()
    TASKS = auto()
    NOTES = auto()


PALETTE = [
    ("default", "default", "default"),
    ("focus", "default", "dark blue", "standout"),
    ("head", "default", "default", "bold"),
    ("dim", "dark gray", "default"),
    ("done", "dark green", "default"),
    ("bar_f", "default", "default"),
    ("bar_e", "dark gray", "default"),
    ("error", "dark red", "default"),
    ("help", "default", "default"),
    ("timer_work", "light green", "default"),
    ("timer_break", "light red", "default"),
    ("timer_intro", "yellow", "default"),
]

HELP_TEXT = (
    "TaskWatch+ Help\n\n"
    "Navigation:\n"
    "  \u2191/\u2193        Move selection\n"
    "  Enter       Select / drill in\n"
    "  ` (bq)      Go back one level\n"
    "  Tab         Focus command bar\n\n"
    "Commands (type : then the key):\n"
    "  :a | :add             Add item at current level\n"
    "  :r | :remove          Delete selected item\n"
    "  :e | :edit            Edit selected item\n"
    "  :c | :cancel          Cancel command / wizard\n"
    "  :f | :finish          Toggle task completion\n"
    "  :shf | :showFinished  Toggle showing finished tasks\n"
    "  :hf | :hideFinished  Hide finished tasks\n"
    "  :h | :help            This help\n"
    "  :q | :exit            Quit\n\n"
    "Timer:\n"
    "  :st <minutes>          Start countdown timer\n"
    "  :ts | :timerStop      Stop timer\n"
    "  :pt | :pauseTimer     Pause / unpause timer\n"
    "  :rt | :resetTimer     Reset timer\n\n"
    "Sort (task list only):\n"
    "  :su a | :su d         Sort by urgency asc / desc\n"
    "  :sd a | :sd d         Sort by difficulty asc / desc\n\n"
    "Press any key to close."
)


def _bar(val: int, outof: int) -> list:
    return [("bar_f", "\u25a0" * val), ("bar_e", "\u25a1" * (outof - val))]


def _dur(secs: int) -> str:
    m, s = divmod(secs, 60)
    return f"{m}m{s:02}s" if m else f"{s}s"


class CommandEdit(Edit):
    def __init__(self, app: "TaskWatchTUI"):
        super().__init__(": ")
        self._app = app

    def keypress(self, size: tuple[int, int], key: str) -> str | None:
        if key == "enter":
            text = self.get_edit_text().strip()
            self.set_edit_text("")
            self._app._handle_submit(text)
            return None
        if key == "esc":
            if self.get_edit_text():
                self.set_edit_text("")
                return None
            self._app._handle_submit("")
            return None
        return super().keypress(size, key)


class SelectableText(Text):
    def selectable(self) -> bool:
        return True

    def keypress(self, size: tuple[int, int], key: str) -> str | None:
        return key


class VimListBox(ListBox):
    def keypress(self, size: tuple[int, int], key: str) -> str | None:
        if key == "j":
            key = "down"
        elif key == "k":
            key = "up"
        return super().keypress(size, key)


class NoTabColumns(Columns):
    def keypress(self, size: tuple[int, int], key: str) -> str | None:
        if key == "tab":
            return key
        return super().keypress(size, key)


class MainFrame(Frame):
    def __init__(self, app: TaskWatchTUI):
        self._app = app
        app._title_text = Text("TaskWatch+")
        app._breadcrumb_text = Text("")
        app._clock_text = Text("")
        app._clock_w = AttrMap(app._clock_text, "dim")
        header = Columns(
            [
                ("pack", AttrMap(app._title_text, "head")),
                AttrMap(app._breadcrumb_text, "dim"),
                ("pack", app._clock_w),
            ],
            dividechars=2,
        )
        app._app_title = header[0]
        app._breadcrumb_w = header[1]

        app._list_walker = SimpleFocusListWalker([])
        app._list_box = VimListBox(app._list_walker)
        app._detail_text = Text("Select an item to view details")
        app._detail_w = AttrMap(app._detail_text, "dim")

        list_pane = LineBox(app._list_box)
        detail_pane = LineBox(app._detail_w)

        body = NoTabColumns(
            [("weight", 38, list_pane), ("weight", 62, detail_pane)],
            dividechars=1,
        )
        app._body = body

        app._cmd = CommandEdit(app)
        super().__init__(body, header=header, footer=app._cmd)

    def keypress(self, size: tuple[int, int], key: str) -> str | None:
        key = super().keypress(size, key)
        if key is None:
            return None
        if key == "tab":
            if self.focus_position == "body":
                self.focus_position = "footer"
            else:
                self.focus_position = "body"
                self._app._body.focus_column = 0
            return None
        if key == "`":
            self._app._go_back()
            return None
        return key


class TaskWatchTUI:
    def __init__(self):
        self._level = Level.ARCHIVES
        self._selected_archive_id: int | None = None
        self._selected_archive_name: str | None = None
        self._selected_directory_id: int | None = None
        self._selected_directory_name: str | None = None
        self._selected_task_id: int | None = None
        self._selected_task_name: str | None = None
        self._prompt_handler: Callable[[str], None] | None = None
        self._show_finished = False
        self._sort_field: str | None = None
        self._sort_dir: str = "asc"

        self._timer_running = False
        self._timer_seconds = 0
        self._timer_elapsed = 0
        self._timer_paused = False
        self._timer_task_id: int | None = None
        self._timer_schedule: dict | None = None
        self._timer_segment_idx: int = 0
        self._timer_segment_elapsed: int = 0
        self._tick_counter: int = 0

        self._frame = MainFrame(self)
        self._loop = urwid.MainLoop(
            self._frame, PALETTE, unhandled_input=self._unhandled_input
        )
        self._list_walker: SimpleFocusListWalker
        self._list_box: ListBox
        self._detail_text: Text
        self._detail_w: AttrMap
        self._cmd: CommandEdit
        self._breadcrumb_text: Text
        self._clock_text: Text
        self._breadcrumb_w: AttrMap
        self._clock_w: AttrMap

    def _focus_body(self) -> None:
        self._frame.focus_position = "body"
        self._body.focus_column = 0

    def _refresh_list(self) -> None:
        self._list_walker.clear()
        tasks: list = []

        if self._level == Level.ARCHIVES:
            tasks = archive_cmds.list_archives()
            self._set_breadcrumb("\uea98 Archives")
            for a in tasks:
                w = AttrMap(SelectableText(f"\uea98 {a.name}"), "default", "focus")
                self._list_walker.append(w)

        elif self._level == Level.DIRECTORIES:
            self._set_breadcrumb(
                f"\uea98 Archives / \uf4d3 {self._selected_archive_name or '?'}"
            )
            dirs = directory_cmds.list_directories(
                archive_id=self._selected_archive_id
            )
            for d in dirs:
                w = AttrMap(SelectableText(f"\uf4d3 {d.name}"), "default", "focus")
                self._list_walker.append(w)

        elif self._level == Level.TASKS:
            status = " [+done]" if self._show_finished else ""
            self._set_breadcrumb(
                f"\uea98 Archives / \uf4d3 {self._selected_archive_name or '?'}"
                f" / \ueb67 {self._selected_directory_name or '?'}{status}"
            )
            kw: dict = {}
            if not self._show_finished:
                kw["finished"] = False
            if self._sort_field:
                kw["order_by"] = self._sort_field
                kw["order_dir"] = self._sort_dir
            task_list = task_cmds.list_tasks(self._selected_directory_id, **kw)
            for t in task_list:
                prefix = "\u2713 " if t.finished else "\u25cb "
                label = prefix + f"\ueb67 {t.name}"
                if t.finished:
                    w = AttrMap(SelectableText(label), "dim", "focus")
                else:
                    w = AttrMap(SelectableText(label), "default", "focus")
                self._list_walker.append(w)

        elif self._level == Level.NOTES:
            self._set_breadcrumb(
                f"\uea98 Archives / \uf4d3 {self._selected_archive_name or '?'}"
                f" / \ueb67 {self._selected_directory_name or '?'}"
                f" / \U000f039a {self._selected_task_name or '?'}"
            )
            notes = note_cmds.list_notes(self._selected_task_id)
            for n in notes:
                first_line = n.note.split("\n")[0][:60]
                label = f"\U000f039a {n.id}: {first_line}"
                w = AttrMap(SelectableText(label), "default", "focus")
                self._list_walker.append(w)

    def _set_breadcrumb(self, path: str) -> None:
        self._breadcrumb_text.set_text(path)

    def _show_detail(self) -> None:
        if not self._list_walker:
            self._detail_text.set_text("")
            return
        try:
            idx = self._list_box.focus_position
        except IndexError:
            self._detail_text.set_text("")
            return
        if idx >= len(self._list_walker):
            self._detail_text.set_text("")
            return

        if self._level == Level.ARCHIVES:
            archives = archive_cmds.list_archives()
            if idx < len(archives):
                a = archives[idx]
                self._detail_text.set_text(
                    [("head", f"\uea98 {a.name}"), "\n\nPress Enter to browse directories."]
                )

        elif self._level == Level.DIRECTORIES:
            dirs = directory_cmds.list_directories(
                archive_id=self._selected_archive_id
            )
            if idx < len(dirs):
                d = dirs[idx]
                self._detail_text.set_text(
                    [("head", f"\uf4d3 {d.name}"), "\n\nPress Enter to browse tasks."]
                )

        elif self._level == Level.TASKS:
            kw: dict = {}
            if not self._show_finished:
                kw["finished"] = False
            if self._sort_field:
                kw["order_by"] = self._sort_field
                kw["order_dir"] = self._sort_dir
            task_list = task_cmds.list_tasks(self._selected_directory_id, **kw)
            if idx < len(task_list):
                task = task_list[idx]
                self._selected_task_id = task.id
                self._selected_task_name = task.name
                self._show_task_detail(task)

        elif self._level == Level.NOTES:
            notes = note_cmds.list_notes(self._selected_task_id)
            if idx < len(notes):
                n = notes[idx]
                self._detail_text.set_text(n.note)

    def _show_task_detail(self, task) -> None:
        s = timer_mod.compute_schedule(task)

        status = "\u2713 Done" if task.finished else "\u25cb Pending"
        deadline = task.deadline if task.deadline != "none" else "\u2014"
        repeat = f"{task.repeatable_type}" if task.repeatable else "\u2014"
        fd = (
            task.finished_date
            if task.finished_date != "none"
            else "\u2014"
        )

        lines: list = [
            ("head", f"\ueb67 {task.name}"),
            "\n\n",
            ("head", "Status: "),
            ("done" if task.finished else "default", status),
            "\n",
            ("head", "Deadline: "),
            deadline,
            "\n",
            ("head", "Repeat: "),
            repeat,
            "\n",
            ("head", "Finished: "),
            fd,
            "\n\n",
            ("head", "Urgency:   "),
            *_bar(task.urgency, 5),
            f"  {task.urgency}/5",
            "\n",
            ("head", "Difficulty: "),
            *_bar(task.difficulty, 5),
            f"  {task.difficulty}/5",
            "\n",
            ("head", "Time budget: "),
            f"{task.time_dedicated} min",
        ]

        if task.description:
            lines.append("\n\n")
            lines.append(task.description)

        if "error" in s:
            lines.append("\n\n")
            lines.append(("error", s["error"]))
            lines.append("\nSet a time budget to see the Pomodoro schedule.")
        else:
            lines.append("\n\n")
            lines.append(("head", "Pomodoro:"))
            lines.append("\n  ")
            lines.append(("head", "Work:  "))
            lines.append(f"{s['work_minutes']}m  ({s['work_pct']}%)")
            lines.append("\n  ")
            lines.append(("head", "Break: "))
            lines.append(f"{s['break_minutes']}m")
            lines.append("\n  ")
            lines.append(("head", "Segments: "))
            lines.append(str(s["segment_count"]))

            segs = s["segments"]
            if segs:
                lines.append("\n\n")
                lines.append(("head", "Schedule:"))
                idx = 0
                lines.append(f"\n  {idx}: {_dur(segs[0])}  intro")
                idx = 1
                for i in range(s["difficulty"]):
                    wk = segs[1 + i * 2]
                    br = segs[1 + i * 2 + 1]
                    lines.append(f"\n  {idx}: {_dur(wk)}  work")
                    idx += 1
                    lines.append(f"\n  {idx}: {_dur(br)}  break")
                    idx += 1

        self._detail_text.set_text(lines)

    def _get_selected_id(self) -> int | None:
        if self._level == Level.ARCHIVES:
            archives = archive_cmds.list_archives()
            idx = self._list_box.focus_position
            if idx < len(archives):
                return archives[idx].id
        elif self._level == Level.DIRECTORIES:
            dirs = directory_cmds.list_directories(
                archive_id=self._selected_archive_id
            )
            idx = self._list_box.focus_position
            if idx < len(dirs):
                return dirs[idx].id
        elif self._level == Level.TASKS:
            kw: dict = {}
            if not self._show_finished:
                kw["finished"] = False
            if self._sort_field:
                kw["order_by"] = self._sort_field
                kw["order_dir"] = self._sort_dir
            task_list = task_cmds.list_tasks(self._selected_directory_id, **kw)
            idx = self._list_box.focus_position
            if idx < len(task_list):
                return task_list[idx].id
        elif self._level == Level.NOTES:
            notes = note_cmds.list_notes(self._selected_task_id)
            idx = self._list_box.focus_position
            if idx < len(notes):
                return notes[idx].id
        return None

    def _get_selected_name(self) -> str | None:
        if self._level == Level.ARCHIVES:
            archives = archive_cmds.list_archives()
            idx = self._list_box.focus_position
            if idx < len(archives):
                return archives[idx].name
        elif self._level == Level.DIRECTORIES:
            dirs = directory_cmds.list_directories(
                archive_id=self._selected_archive_id
            )
            idx = self._list_box.focus_position
            if idx < len(dirs):
                return dirs[idx].name
        elif self._level == Level.TASKS:
            kw: dict = {}
            if not self._show_finished:
                kw["finished"] = False
            if self._sort_field:
                kw["order_by"] = self._sort_field
                kw["order_dir"] = self._sort_dir
            task_list = task_cmds.list_tasks(self._selected_directory_id, **kw)
            idx = self._list_box.focus_position
            if idx < len(task_list):
                return task_list[idx].name
        elif self._level == Level.NOTES:
            notes = note_cmds.list_notes(self._selected_task_id)
            idx = self._list_box.focus_position
            if idx < len(notes):
                return notes[idx].content.split("\n")[0][:60]
        return None

    def _select(self) -> None:
        if self._level == Level.ARCHIVES:
            idx = self._list_box.focus_position
            archives = archive_cmds.list_archives()
            if idx < len(archives):
                a = archives[idx]
                self._selected_archive_id = a.id
                self._selected_archive_name = a.name
                self._level = Level.DIRECTORIES
                self._refresh_list()

        elif self._level == Level.DIRECTORIES:
            idx = self._list_box.focus_position
            dirs = directory_cmds.list_directories(
                archive_id=self._selected_archive_id
            )
            if idx < len(dirs):
                d = dirs[idx]
                self._selected_directory_id = d.id
                self._selected_directory_name = d.name
                self._level = Level.TASKS
                self._refresh_list()

        elif self._level == Level.TASKS:
            self._level = Level.NOTES
            self._refresh_list()

    def _go_back(self) -> None:
        if self._level == Level.NOTES:
            self._level = Level.TASKS
        elif self._level == Level.TASKS:
            self._level = Level.DIRECTORIES
        elif self._level == Level.DIRECTORIES:
            self._level = Level.ARCHIVES
            self._selected_archive_id = None
            self._selected_archive_name = None
            self._selected_directory_id = None
            self._selected_directory_name = None
            self._selected_task_id = None
            self._selected_task_name = None
        elif self._level == Level.ARCHIVES:
            raise urwid.ExitMainLoop()
        self._refresh_list()

    def _handle_submit(self, text: str) -> None:
        if self._prompt_handler:
            self._prompt_handler(text)
            return
        if not text:
            self._focus_body()
            return
        if text.startswith(":"):
            cmd = text[1:].strip()
            self._handle_command(cmd)
        else:
            self._focus_body()

    def _handle_command(self, cmd: str) -> None:
        if cmd in ("q", "exit"):
            raise urwid.ExitMainLoop()
        if cmd in ("h", "help"):
            self._show_help()
            return
        if cmd in ("a", "add"):
            self._cmd_add()
            return
        if cmd in ("r", "remove", "d"):
            self._cmd_remove()
            return
        if cmd in ("e", "edit"):
            self._cmd_edit()
            return
        if cmd in ("f", "finish"):
            self._cmd_finish()
            return
        if cmd in ("shf", "showFinished"):
            self._show_finished = not self._show_finished
            self._refresh_list()
            return
        if cmd in ("hf", "hideFinished"):
            self._show_finished = False
            self._refresh_list()
            return
        if cmd in ("c", "cancel"):
            self._prompt_handler = None
            self._cmd.set_caption(": ")
            self._focus_body()
            return

        if cmd == "st":
            if self._selected_task_id is not None:
                t = task_cmds.get_task(self._selected_task_id)
                if t:
                    self._start_timer_for_task(t)
            return
        if cmd.startswith("st "):
            try:
                mins = int(cmd.split(" ", 1)[1])
                self._start_timer(mins)
            except ValueError:
                pass
            return
        if cmd in ("ts", "timerStop"):
            self._stop_timer()
            return
        if cmd in ("pt", "pauseTimer"):
            self._timer_paused = not self._timer_paused
            return
        if cmd in ("rt", "resetTimer"):
            self._stop_timer()
            return

        if cmd in ("su a", "su d"):
            self._sort_field = "urgency"
            self._sort_dir = "asc" if cmd == "su a" else "desc"
            if self._level == Level.TASKS:
                self._refresh_list()
            return
        if cmd in ("sd a", "sd d"):
            self._sort_field = "difficulty"
            self._sort_dir = "asc" if cmd == "sd a" else "desc"
            if self._level == Level.TASKS:
                self._refresh_list()
            return

        self._focus_body()

    def _cmd_add(self) -> None:
        if self._level == Level.ARCHIVES:
            self._start_wizard("Archive name: ", self._wiz_archive_name)
        elif self._level == Level.DIRECTORIES:
            self._start_wizard("Directory name: ", self._wiz_dir_name)
        elif self._level == Level.TASKS:
            self._start_wizard("Task name: ", self._wiz_task_name)
        elif self._level == Level.NOTES:
            today = date.today().strftime("%d/%m/%Y")
            note_cmds.create_note(self._selected_task_id, today, "")
            self._start_wizard(
                "Note content (leave empty for date-only): ",
                partial(self._wiz_note_content, today),
            )

    def _wiz_archive_name(self, name: str) -> None:
        if not name:
            self._end_wizard()
            return
        archive_cmds.create_archive(name)
        self._end_wizard()

    def _wiz_dir_name(self, name: str) -> None:
        if not name:
            self._end_wizard()
            return
        directory_cmds.create_directory(
            self._selected_archive_id, name
        )
        self._end_wizard()

    def _wiz_task_name(self, name: str) -> None:
        if not name:
            self._start_wizard(
                "Task name: ",
                self._wiz_task_name,
            )
            return
        self._wiz_name = name
        self._start_wizard(
            "Urgency (1-5): ",
            partial(self._wiz_task_urgency, name),
        )

    def _wiz_task_urgency(self, name: str, urgency_str: str) -> None:
        if not urgency_str:
            urgency = 1
        else:
            try:
                urgency = int(urgency_str)
                if not 1 <= urgency <= 5:
                    raise ValueError
            except ValueError:
                self._start_wizard(
                    "Urgency (1-5): ",
                    partial(self._wiz_task_urgency, name),
                )
                return
        self._start_wizard(
            "Difficulty (1-5): ",
            partial(self._wiz_task_difficulty, name, urgency),
        )

    def _wiz_task_difficulty(
        self, name: str, urgency: int, diff_str: str
    ) -> None:
        if not diff_str:
            difficulty = 1
        else:
            try:
                difficulty = int(diff_str)
                if not 1 <= difficulty <= 5:
                    raise ValueError
            except ValueError:
                self._start_wizard(
                    "Difficulty (1-5): ",
                    partial(self._wiz_task_difficulty, name, urgency),
                )
                return
        self._start_wizard(
            "Time budget (minutes): ",
            partial(self._wiz_task_time, name, urgency, difficulty),
        )

    def _wiz_task_time(
        self,
        name: str,
        urgency: int,
        difficulty: int,
        time_str: str,
    ) -> None:
        if not time_str:
            time_dedicated = 0
        else:
            try:
                time_dedicated = int(time_str)
            except ValueError:
                self._start_wizard(
                    "Time budget (minutes): ",
                    partial(self._wiz_task_time, name, urgency, difficulty),
                )
                return
        self._start_wizard(
            "Deadline (dd/MM/yyyy, or 'none'): ",
            partial(
                self._wiz_task_deadline,
                name,
                urgency,
                difficulty,
                time_dedicated,
            ),
        )

    def _wiz_task_deadline(
        self,
        name: str,
        urgency: int,
        difficulty: int,
        time_dedicated: int,
        deadline: str,
    ) -> None:
        if not deadline:
            deadline = "none"
        if deadline != "none":
            try:
                datetime.strptime(deadline, "%d/%m/%Y")
            except ValueError:
                self._start_wizard(
                    "Deadline (dd/MM/yyyy, or 'none'): ",
                    partial(
                        self._wiz_task_deadline,
                        name,
                        urgency,
                        difficulty,
                        time_dedicated,
                    ),
                )
                return
        self._start_wizard(
            "Repeatable? (y/n): ",
            partial(
                self._wiz_task_repeat,
                name,
                urgency,
                difficulty,
                time_dedicated,
                deadline,
            ),
        )

    def _wiz_task_repeat(
        self,
        name: str,
        urgency: int,
        difficulty: int,
        time_dedicated: int,
        deadline: str,
        repeat_yn: str,
    ) -> None:
        if not repeat_yn:
            repeatable = False
        else:
            repeatable = repeat_yn.lower() in ("y", "yes")
        if repeatable:
            self._start_wizard(
                "Repeat type (daily/weekly/biweekly/monthly/yearly): ",
                partial(
                    self._wiz_task_repeat_type,
                    name,
                    urgency,
                    difficulty,
                    time_dedicated,
                    deadline,
                ),
            )
        else:
            task_cmds.create_task(
                self._selected_directory_id,
                name,
                urgency=urgency,
                difficulty=difficulty,
                time_dedicated=time_dedicated,
                deadline=deadline,
                repeatable=False,
            )
            self._end_wizard()

    def _wiz_task_repeat_type(
        self,
        name: str,
        urgency: int,
        difficulty: int,
        time_dedicated: int,
        deadline: str,
        repeat_type: str,
    ) -> None:
        if not repeat_type:
            repeat_type = "daily"
        valid = ("daily", "weekly", "biweekly", "monthly", "yearly")
        if repeat_type not in valid:
            self._start_wizard(
                "Repeat type (daily/weekly/biweekly/monthly/yearly): ",
                partial(
                    self._wiz_task_repeat_type,
                    name,
                    urgency,
                    difficulty,
                    time_dedicated,
                    deadline,
                ),
            )
            return
        self._start_wizard(
            "Auto-repeat (task recreates on finish)? (y/n): ",
            partial(
                self._wiz_task_auto_repeat,
                name,
                urgency,
                difficulty,
                time_dedicated,
                deadline,
                repeat_type,
            ),
        )

    def _wiz_task_auto_repeat(
        self,
        name: str,
        urgency: int,
        difficulty: int,
        time_dedicated: int,
        deadline: str,
        repeat_type: str,
        auto_repeat_yn: str,
    ) -> None:
        to_complete = auto_repeat_yn.lower() in ("y", "yes")
        task_cmds.create_task(
            self._selected_directory_id,
            name,
            urgency=urgency,
            difficulty=difficulty,
            time_dedicated=time_dedicated,
            deadline=deadline,
            repeatable=True,
            repeatable_type=repeat_type,
            has_to_be_completed_to_repeat=to_complete,
        )
        self._end_wizard()

    def _wiz_note_content(self, today: str, content: str) -> None:
        if content:
            note_cmds.update_note_content(
                self._selected_task_id, today, content
            )
        self._end_wizard()

    def _cmd_remove(self) -> None:
        sid = self._get_selected_id()
        if sid is None:
            return
        if self._level == Level.ARCHIVES:
            archive_cmds.delete_archive(sid)
        elif self._level == Level.DIRECTORIES:
            directory_cmds.delete_directory(sid)
        elif self._level == Level.TASKS:
            task_cmds.delete_task(sid)
        elif self._level == Level.NOTES:
            note_cmds.delete_note(sid)
        self._refresh_list()

    def _cmd_edit(self) -> None:
        sid = self._get_selected_id()
        if sid is None:
            return
        sname = self._get_selected_name()
        if self._level == Level.ARCHIVES:
            self._start_wizard(
                f"New name [{sname}]: ",
                partial(self._wiz_edit_archive, sid, sname),
            )
        elif self._level == Level.DIRECTORIES:
            self._start_wizard(
                f"New name [{sname}]: ",
                partial(self._wiz_edit_dir, sid, sname),
            )
        elif self._level == Level.TASKS and self._selected_task_id is not None:
            self._edit_task(sid)

    def _wiz_edit_archive(
        self, archive_id: int, old_name: str, new_name: str
    ) -> None:
        if not new_name:
            self._end_wizard()
            return
        archive_cmds.rename_archive(archive_id, new_name)
        self._end_wizard()

    def _wiz_edit_dir(
        self, dir_id: int, old_name: str, new_name: str
    ) -> None:
        if not new_name:
            self._end_wizard()
            return
        directory_cmds.rename_directory(dir_id, new_name)
        self._end_wizard()

    def _edit_task(self, task_id: int) -> None:
        task = task_cmds.get_task(task_id)
        if not task:
            return
        self._edit_ctx = {
            "task_id": task_id,
            "name": task.name,
            "urgency": task.urgency,
            "difficulty": task.difficulty,
            "time_dedicated": task.time_dedicated,
            "deadline": task.deadline,
            "repeatable": task.repeatable,
            "repeatable_type": task.repeatable_type,
            "has_to_be_completed_to_repeat": task.has_to_be_completed_to_repeat,
        }
        self._start_wizard(
            f"Name [{task.name}]: ",
            self._wiz_edit_task_name,
        )

    def _wiz_edit_task_name(self, name: str) -> None:
        if name:
            self._edit_ctx["name"] = name
        self._start_wizard(
            f"Urgency ({self._edit_ctx['urgency']}): ",
            self._wiz_edit_task_urgency,
        )

    def _wiz_edit_task_urgency(self, urgency_str: str) -> None:
        if urgency_str:
            try:
                v = int(urgency_str)
                if 1 <= v <= 5:
                    self._edit_ctx["urgency"] = v
            except ValueError:
                pass
        self._start_wizard(
            f"Difficulty ({self._edit_ctx['difficulty']}): ",
            self._wiz_edit_task_difficulty,
        )

    def _wiz_edit_task_difficulty(self, diff_str: str) -> None:
        if diff_str:
            try:
                v = int(diff_str)
                if 1 <= v <= 5:
                    self._edit_ctx["difficulty"] = v
            except ValueError:
                pass
        self._start_wizard(
            f"Time budget ({self._edit_ctx['time_dedicated']}): ",
            self._wiz_edit_task_time,
        )

    def _wiz_edit_task_time(self, time_str: str) -> None:
        if time_str:
            try:
                self._edit_ctx["time_dedicated"] = int(time_str)
            except ValueError:
                pass
        self._start_wizard(
            f"Deadline ({self._edit_ctx['deadline']}): ",
            self._wiz_edit_task_deadline,
        )

    def _wiz_edit_task_deadline(self, deadline: str) -> None:
        if deadline and deadline != self._edit_ctx["deadline"]:
            if deadline != "none":
                try:
                    datetime.strptime(deadline, "%d/%m/%Y")
                    self._edit_ctx["deadline"] = deadline
                except ValueError:
                    pass
            else:
                self._edit_ctx["deadline"] = "none"

        ctx = self._edit_ctx
        task_cmds.edit_task(
            ctx["task_id"],
            name=ctx["name"],
            urgency=ctx["urgency"],
            difficulty=ctx["difficulty"],
            time_dedicated=ctx["time_dedicated"],
            deadline=ctx["deadline"],
        )
        self._edit_ctx = None
        self._end_wizard()

    def _cmd_finish(self) -> None:
        if self._level != Level.TASKS:
            return
        sid = self._get_selected_id()
        if sid is None:
            return
        task = task_cmds.get_task(sid)
        if not task:
            return
        if task.finished:
            task_cmds.mark_not_done(sid)
        else:
            task_cmds.mark_done(sid)
        self._refresh_list()

    def _show_help(self) -> None:
        help_w = LineBox(ListBox([Text(HELP_TEXT)]))
        self._help_overlay = Overlay(
            help_w,
            self._frame,
            align="center",
            width=("relative", 80),
            valign="middle",
            height=("relative", 80),
        )
        self._loop.widget = self._help_overlay

    def _start_wizard(
        self, prompt: str, handler: Callable[[str], None]
    ) -> None:
        self._prompt_handler = handler
        self._cmd.set_caption(prompt)
        self._cmd.set_edit_text("")
        self._frame.focus_position = "footer"

    def _end_wizard(self) -> None:
        self._prompt_handler = None
        self._cmd.set_caption(": ")
        self._refresh_list()
        self._show_detail()
        self._focus_body()

    def _start_timer_for_task(self, task) -> None:
        schedule = timer_mod.compute_schedule(task)
        if "error" in schedule:
            return
        self._timer_running = True
        self._timer_schedule = schedule
        self._timer_segment_idx = 0
        self._timer_segment_elapsed = 0
        self._timer_paused = False
        self._timer_task_id = task.id
        self._update_clock_display()

    def _start_timer(self, minutes: int) -> None:
        self._timer_running = True
        self._timer_seconds = minutes * 60
        self._timer_elapsed = 0
        self._timer_paused = False
        self._timer_task_id = None
        self._timer_schedule = None
        self._timer_segment_idx = 0
        self._timer_segment_elapsed = 0
        self._update_clock_display()

    def _stop_timer(self) -> None:
        self._timer_running = False
        self._timer_seconds = 0
        self._timer_elapsed = 0
        self._timer_paused = False
        self._timer_task_id = None
        self._timer_schedule = None
        self._timer_segment_idx = 0
        self._timer_segment_elapsed = 0
        self._update_clock_display()

    def _update_clock_display(self) -> None:
        now = datetime.now()
        if self._timer_running:
            if self._timer_schedule:
                segments = self._timer_schedule["segments"]
                seg_dur = segments[self._timer_segment_idx]
                remaining = max(0, seg_dur - self._timer_segment_elapsed)
                if self._timer_segment_idx == 0:
                    attr = "timer_intro"
                elif self._timer_segment_idx % 2 == 1:
                    attr = "timer_work"
                else:
                    attr = "timer_break"
            else:
                remaining = max(0, self._timer_seconds - self._timer_elapsed)
                attr = "dim"
            m, s = divmod(remaining, 60)
            pause_ind = " \u23f8" if self._timer_paused else ""
            self._clock_text.set_text(f"\u23f1 {m:02d}:{s:02d}{pause_ind}")
            self._clock_w.set_attr_map({None: attr})
        else:
            self._clock_text.set_text(now.strftime("%H:%M:%S"))
            self._clock_w.set_attr_map({None: "dim"})

    def _tick(self, loop: object, data: object) -> None:
        if self._timer_running and not self._timer_paused:
            if self._timer_schedule:
                segments = self._timer_schedule["segments"]
                self._timer_segment_elapsed += 1
                if self._timer_segment_elapsed >= segments[self._timer_segment_idx]:
                    self._timer_segment_elapsed = 0
                    self._timer_segment_idx += 1
                    if self._timer_segment_idx >= len(segments):
                        self._stop_timer()
            else:
                self._timer_elapsed += 1
                if self._timer_elapsed >= self._timer_seconds:
                    self._timer_elapsed = self._timer_seconds
                    self._stop_timer()

        self._tick_counter += 1
        if self._tick_counter % 60 == 0:
            task_cmds.reset_overdue_repeatables()

        self._update_clock_display()
        self._loop.set_alarm_in(1, self._tick)

    def _unhandled_input(self, key: str) -> None:
        if hasattr(self, "_help_overlay") and self._loop.widget is not self._frame:
            self._loop.widget = self._frame
            return
        if key == ":":
            self._frame.focus_position = "footer"
            self._cmd.set_edit_text(":")
            return
        if key == "enter" and self._frame.focus_position == "body":
            if self._level == Level.NOTES:
                self._show_detail()
            else:
                self._select()
            return


    def run(self) -> None:
        self._refresh_list()
        urwid.connect_signal(self._list_walker, "modified", self._show_detail)
        self._loop.set_alarm_in(1, self._tick)
        self._frame.focus_position = "body"
        self._loop.run()


def run_tui() -> None:
    TaskWatchTUI().run()
