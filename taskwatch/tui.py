from __future__ import annotations

import json
import subprocess
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

from . import archive_cmds, calcurse_cmds, db as db_mod, directory_cmds, io_cmds, note_cmds, stats_cmds, tag_cmds, task_cmds, timer as timer_mod, undo_cmds


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
    ("warn", "brown", "default"),
    ("bar_f", "default", "default"),
    ("bar_e", "dark gray", "default"),
    ("error", "dark red", "default"),
    ("help", "default", "default"),
]

COMMANDS = [
    "a", "add", "r", "remove", "d", "e", "edit", "f", "finish",
    "c", "cancel", "shf", "showFinished", "hf", "hideFinished",
    "h", "help", "q", "exit", "stats", "ftc", "undo", "week",
    "st", "ts", "timerStop", "pt", "pauseTimer", "rt", "resetTimer",
    "su a", "su d", "sd a", "sd d", "sn a", "sn d", "sdl a", "sdl d", "sr",
    "tag ", "untag ", "ft ", "gs ", "qa ", "mv ", "mu", "md", "all",
    "export", "import ",
    "bm", "bd", "bt ", "bv ", "bc",
]

HELP_TEXT = (
    "TaskWatch+ Help\n\n"
    "Navigation:\n"
    "  \u2191/\u2193        Move selection\n"
    "  Enter / l    Select / drill in\n"
    "  ` / h        Go back one level\n"
    "  Tab         Focus command bar\n\n"
    "Commands (type : then the key):\n"
    "  :a | :add             Add item at current level\n"
    "  :r | :remove          Delete selected item (with confirmation)\n"
    "  :e | :edit            Edit selected item\n"
    "  :c | :cancel          Cancel command / wizard\n"
    "  :f | :finish          Toggle task completion\n"
    "  :shf | :showFinished  Toggle showing finished tasks\n"
    "  :hf | :hideFinished  Hide finished tasks\n"
    "  :h | :help            This help\n"
    "  :q | :exit            Quit\n"
    "  Tab                   Cycle command completions\n"
    "  \u2191/\u2193              Recall command history (in command bar)\n"
    "  Space                 Toggle bulk selection (task list)\n\n"
    "Search:\n"
    "  /                    Search items in list (type text, Enter to apply, Esc to clear)\n"
    "  :gs <text>           Global search tasks across all archives\n"
    "  :all                 Show all tasks in current archive\n\n"
    "Move:\n"
    "  :mv <target-id>       Move task to directory / dir to archive\n"
    "  :mu | :md             Move task up / down (manual order)\n\n"
    "Quick add:\n"
    "  :qa <name>            Quick-add task (defaults: u:1 d:1)\n"
    "                      :qa name u:3 d:2 t:30 for custom values\n\n"
    "Tags:\n"
    "  :tag <name>          Add tag to selected task\n"
    "  :untag <name>        Remove tag from selected task\n"
    "  :ft <name>           Filter tasks by tag name\n"
    "  :ftc                 Clear tag filter\n\n"
    "Bulk (select with Space first):\n"
    "  :bm                  Mark selected tasks done\n"
    "  :bd                  Delete selected tasks\n"
    "  :bt <name>           Tag selected tasks\n"
    "  :bv <dir-id>         Move selected tasks to directory\n"
    "  :bc                  Clear selection\n\n"
    "Stats & View:\n"
    "  :stats               Show task statistics\n"
    "  :week                Show tasks grouped by deadline this week\n\n"
    "Undo:\n"
    "  :undo                Undo last delete / edit / finish\n\n"
    "Export/Import:\n"
    "  :export [path]        Export all data as JSON\n"
    "  :import <path>        Import data from JSON\n\n"
    "Timer:\n"
    "  :st <minutes>          Start countdown timer\n"
    "  :ts | :timerStop      Stop timer\n"
    "  :pt | :pauseTimer     Pause / unpause timer\n"
    "  :rt | :resetTimer     Reset timer\n\n"
    "Sort (task list only):\n"
    "  :su a | :su d         Sort by urgency asc / desc\n"
    "  :sd a | :sd d         Sort by difficulty asc / desc\n"
    "  :sn a | :sn d         Sort by name asc / desc\n"
    "  :sdl a | :sdl d       Sort by deadline asc / desc\n"
    "  :sr                   Reset to default order\n\n"
    "Press any key to close."
)


def _bar(val: int, outof: int) -> list:
    result = [("bar_f", "\u25a0" * val)]
    if val < outof:
        result.append(("bar_e", "\u25a1" * (outof - val)))
    return result


def _pct_bar(pct: int, width: int) -> list:
    filled = int(width * pct / 100)
    empty = width - filled
    fill_style = "done" if pct >= 80 else ("warn" if pct >= 50 else "error")
    parts = [(fill_style, "\u2588" * filled)]
    if empty:
        parts.append(("bar_e", "\u2591" * empty))
    return parts


def _dur(secs: int) -> str:
    m, s = divmod(secs, 60)
    return f"{m}m{s:02}s" if m else f"{s}s"


class CommandEdit(Edit):
    def __init__(self, app: "TaskWatchTUI"):
        super().__init__(("standout", "\u276f "))
        self._app = app

    def keypress(self, size: tuple[int, int], key: str) -> str | None:
        if self._app._in_search_mode:
            if key == "esc":
                self._app._exit_search_mode()
                return None
            if key == "enter":
                self._app._apply_search()
                return None
            result = super().keypress(size, key)
            self._app._on_search_change(self.get_edit_text())
            return result
        if key == "tab":
            self._app._complete_command()
            return None
        if key == "up" and not self._app._prompt_handler and self._app._cmd_history:
            self._app._cmd_history_index = max(-1, self._app._cmd_history_index - 1)
            if self._app._cmd_history_index >= 0:
                self.set_edit_text(self._app._cmd_history[self._app._cmd_history_index])
            else:
                self.set_edit_text("")
            return None
        if key == "down" and not self._app._prompt_handler and self._app._cmd_history:
            self._app._cmd_history_index += 1
            if self._app._cmd_history_index < len(self._app._cmd_history):
                self.set_edit_text(self._app._cmd_history[self._app._cmd_history_index])
            else:
                self._app._cmd_history_index = len(self._app._cmd_history)
                self.set_edit_text("")
            return None
        if key == "enter":
            self._app._tab_matches = []
            self._app._tab_index = -1
            text = self.get_edit_text().strip()
            self.set_edit_text("")
            self._app._handle_submit(text)
            return None
        if key == "esc":
            self._app._tab_matches = []
            self._app._tab_index = -1
            if self.get_edit_text():
                self.set_edit_text("")
                return None
            self._app._handle_submit("")
            return None
        if key == "h" and self._app._prompt_handler:
            self._app._wizard_back()
            return None
        if self._app._tab_matches:
            self._app._tab_matches = []
            self._app._tab_index = -1
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
        if key == ":" and self.focus_position == "body":
            self.focus_position = "footer"
            self._app._cmd.set_edit_text("")
            return None
        if key == "/" and self.focus_position == "body" and not self._app._in_search_mode:
            self._app._enter_search_mode()
            return None
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
        if key in ("`", "h"):
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
        self._wiz_name: str | None = None
        self._wiz_desc: str = ""
        self._wizard_stack: list[dict] = []
        self._cmd_history: list[str] = []
        self._cmd_history_index: int = -1
        self._edit_ctx: dict | None = None
        self._help_overlay = None
        self._current_items: list | None = None

        self._timer_running = False
        self._timer_seconds = 0
        self._timer_elapsed = 0
        self._timer_paused = False
        self._timer_task_id: int | None = None
        self._timer_schedule: dict | None = None
        self._timer_segment_idx: int = 0
        self._timer_segment_elapsed: int = 0
        self._tick_counter: int = 0
        self._filter_text: str = ""
        self._in_search_mode: bool = False
        self._filter_tag: str | None = None
        self._stats_overlay = None
        self._tab_matches: list[str] = []
        self._tab_index: int = -1
        self._notified_deadlines: set[int] = set()
        self._notify_deadlines_enabled: bool = True
        self._bulk_selection: set[int] = set()
        self._all_tasks_mode: bool = False

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

        filter_indicator = ""
        if self._filter_text:
            filter_indicator = f" [filter: {self._filter_text}]"

        tag_filter_indicator = ""
        if self._filter_tag:
            tag_filter_indicator = f" [tag: {self._filter_tag}]"

        if self._level == Level.ARCHIVES:
            items = archive_cmds.list_archives()
            if self._filter_text:
                items = [x for x in items if self._filter_text.lower() in x.name.lower()]
            self._current_items = items
            self._set_breadcrumb(f"\uf187 Archives{filter_indicator}")
            for a in items:
                cnt = len(directory_cmds.list_directories(archive_id=a.id))
                w = AttrMap(SelectableText(f"\uf187 {a.name}  [{cnt}]"), "default", "focus")
                self._list_walker.append(w)

        elif self._level == Level.DIRECTORIES:
            self._set_breadcrumb(
                f"\uf187 Archives \u25b8 \uf4d3 {self._selected_archive_name or '?'}{filter_indicator}"
            )
            items = directory_cmds.list_directories(
                archive_id=self._selected_archive_id
            )
            if self._filter_text:
                items = [x for x in items if self._filter_text.lower() in x.name.lower()]
            self._current_items = items
            for d in items:
                total, done = stats_cmds.directory_stats(d.id)
                w = AttrMap(SelectableText(f"\uf4d3 {d.name}  [{done}/{total}]"), "default", "focus")
                self._list_walker.append(w)

        elif self._level == Level.TASKS:
            status = " [+done]" if self._show_finished else ""
            dir_label = self._selected_directory_name or "?"
            if self._all_tasks_mode:
                dir_label = "All Tasks"
            self._set_breadcrumb(
                f"\uf187 Archives \u25b8 \uf4d3 {self._selected_archive_name or '?'}"
                f" \u25b8 \ueebf {dir_label}{status}{filter_indicator}{tag_filter_indicator}"
            )
            kw: dict = {}
            if not self._show_finished:
                kw["finished"] = False
            if self._sort_field:
                kw["order_by"] = self._sort_field
                kw["order_dir"] = self._sort_dir
            if self._all_tasks_mode and self._selected_archive_id is not None:
                raw = task_cmds.list_all_tasks(self._selected_archive_id, **kw)
                items = [r["task"] for r in raw]
                dir_map = {r["task"].id: r["dir_name"] for r in raw}
            else:
                items = task_cmds.list_tasks(self._selected_directory_id, **kw)
                dir_map = {}
            if self._filter_text:
                items = [x for x in items if self._filter_text.lower() in x.name.lower()]
            if self._filter_tag:
                tagged_ids = set(tag_cmds.get_tasks_by_tag(self._filter_tag))
                items = [x for x in items if x.id in tagged_ids]
            self._current_items = items
            for t in items:
                sel = "[x]" if t.id in self._bulk_selection else " "
                prefix = "\u2713 " if t.finished else f"\u25cb{sel} "
                cnt = len(note_cmds.list_notes(task_id=t.id))
                tags = tag_cmds.get_tags_for_task(t.id)
                tag_str = f" [{','.join(tg.name for tg in tags)}]" if tags else ""
                dir_str = f" [{dir_map[t.id]}]" if t.id in dir_map else ""
                label = prefix + f"\ueebf {t.name}  [{cnt}]{tag_str}{dir_str}"
                selected = t.id in self._bulk_selection
                if t.finished:
                    w = AttrMap(SelectableText(label), "dim", "focus")
                elif selected:
                    w = AttrMap(SelectableText(label), "focus", "focus")
                else:
                    w = AttrMap(SelectableText(label), "default", "focus")
                self._list_walker.append(w)

        elif self._level == Level.NOTES:
            self._set_breadcrumb(
                f"\uf187 Archives \u25b8 \uf4d3 {self._selected_archive_name or '?'}"
                f" \u25b8 \ueebf {self._selected_directory_name or '?'}"
                f" \u25b8 \U000f039a {self._selected_task_name or '?'}{filter_indicator}"
            )
            items = note_cmds.list_notes(self._selected_task_id)
            if self._filter_text:
                items = [x for x in items if self._filter_text.lower() in x.note.lower()]
            self._current_items = items
            for n in items:
                first_line = n.note.split("\n")[0][:60]
                label = f"\U000f039a {n.id}: {first_line}"
                w = AttrMap(SelectableText(label), "default", "focus")
                self._list_walker.append(w)

    def _set_breadcrumb(self, path: str) -> None:
        self._breadcrumb_text.set_text(path)

    def _show_detail(self) -> None:
        if not self._list_walker or not self._current_items:
            self._detail_text.set_text("")
            return
        try:
            idx = self._list_box.focus_position
        except IndexError:
            self._detail_text.set_text("")
            return
        if idx >= len(self._current_items):
            self._detail_text.set_text("")
            return

        if self._level == Level.ARCHIVES:
            a = self._current_items[idx]
            self._detail_text.set_text(
                [("head", f"\uf187 {a.name}"), "\n\nPress Enter to browse directories."]
            )

        elif self._level == Level.DIRECTORIES:
            d = self._current_items[idx]
            self._detail_text.set_text(
                [("head", f"\uf4d3 {d.name}"), "\n\nPress Enter to browse tasks."]
            )

        elif self._level == Level.TASKS:
            task = self._current_items[idx]
            self._selected_task_id = task.id
            self._selected_task_name = task.name
            self._show_task_detail(task)

        elif self._level == Level.NOTES:
            n = self._current_items[idx]
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
            ("head", f"\ueebf {task.name}"),
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

        tags = tag_cmds.get_tags_for_task(task.id)
        lines.append("\n\n")
        lines.append(("head", "Tags: "))
        if tags:
            lines.append(", ".join(t.name for t in tags))
        else:
            lines.append("\u2014")

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
                lines.append(("head", "\n  "))
                dur_fmt = _dur(segs[0])
                lines.append(f" 0  {dur_fmt:>8}  ")
                lines.append(("default", "INTRO"))
                for i in range(s["difficulty"]):
                    wk = segs[1 + i * 2]
                    br = segs[1 + i * 2 + 1]
                    wk_fmt = _dur(wk)
                    br_fmt = _dur(br)
                    lines.append(f"\n  {1 + i * 2}  {wk_fmt:>8}  ")
                    lines.append(("head", "WORK"))
                    lines.append(f"\n  {2 + i * 2}  {br_fmt:>8}  ")
                    lines.append(("dim", "BREAK"))

        self._detail_text.set_text(lines)

    def _get_selected_id(self) -> int | None:
        if not self._current_items:
            return None
        idx = self._list_box.focus_position
        if idx < len(self._current_items):
            return self._current_items[idx].id
        return None

    def _get_selected_name(self) -> str | None:
        if not self._current_items:
            return None
        idx = self._list_box.focus_position
        if idx >= len(self._current_items):
            return None
        item = self._current_items[idx]
        if self._level == Level.NOTES:
            return item.note.split("\n")[0][:60]
        return item.name

    def _select(self) -> None:
        if not self._current_items:
            return
        idx = self._list_box.focus_position
        if idx >= len(self._current_items):
            return
        if self._level == Level.ARCHIVES:
            a = self._current_items[idx]
            self._selected_archive_id = a.id
            self._selected_archive_name = a.name
            self._level = Level.DIRECTORIES
            self._refresh_list()

        elif self._level == Level.DIRECTORIES:
            d = self._current_items[idx]
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
            if self._all_tasks_mode:
                self._all_tasks_mode = False
                self._selected_directory_id = self._selected_directory_id
                self._level = Level.DIRECTORIES
                self._selected_directory_name = self._selected_directory_name
            else:
                self._level = Level.DIRECTORIES
            self._selected_task_id = None
            self._selected_task_name = None
        elif self._level == Level.DIRECTORIES:
            self._level = Level.ARCHIVES
            self._selected_archive_id = None
            self._selected_archive_name = None
            self._selected_directory_id = None
            self._selected_directory_name = None
            self._selected_task_id = None
            self._selected_task_name = None
        self._refresh_list()

    def _handle_submit(self, text: str) -> None:
        if self._prompt_handler:
            self._prompt_handler(text)
            return
        if not text:
            self._focus_body()
            return
        self._handle_command(text)
        if text and (not self._cmd_history or self._cmd_history[-1] != text):
            self._cmd_history.append(text)
            if len(self._cmd_history) > 50:
                self._cmd_history.pop(0)
        self._cmd_history_index = -1
        if not self._prompt_handler:
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
            self._wizard_stack.clear()
            self._cmd.set_caption(": ")
            self._bulk_selection.clear()
            self._refresh_list()
            self._focus_body()
            return

        if cmd == "all":
            if self._selected_archive_id is not None:
                self._all_tasks_mode = True
                self._level = Level.TASKS
                self._refresh_list()
            return
        if cmd == "mu":
            if self._level == Level.TASKS and not self._sort_field:
                sid = self._get_selected_id()
                if sid is not None and task_cmds.move_task_up(sid):
                    self._refresh_list()
                    self._show_detail()
            return
        if cmd == "md":
            if self._level == Level.TASKS and not self._sort_field:
                sid = self._get_selected_id()
                if sid is not None and task_cmds.move_task_down(sid):
                    self._refresh_list()
                    self._show_detail()
            return
        if cmd.startswith("mv "):
            try:
                target_id = int(cmd.split(" ", 1)[1])
                sid = self._get_selected_id()
                if sid is None:
                    return
                if self._level == Level.TASKS:
                    if task_cmds.move_task(sid, target_id):
                        self._cmd.set_caption(("done", "Moved task "))
                        self._loop.set_alarm_in(2, lambda *a: self._cmd.set_caption(("standout", "\u276f ")))
                        self._refresh_list()
                elif self._level == Level.DIRECTORIES:
                    if directory_cmds.move_directory(sid, target_id):
                        self._cmd.set_caption(("done", "Moved directory "))
                        self._loop.set_alarm_in(2, lambda *a: self._cmd.set_caption(("standout", "\u276f ")))
                        self._refresh_list()
            except ValueError:
                pass
            return
        if cmd.startswith("qa "):
            if self._level == Level.TASKS and self._selected_directory_id is not None:
                rest = cmd[3:].strip()
                name = rest
                urgency = 1
                difficulty = 1
                time_dedicated = 0
                deadline = "none"
                for token in rest.split():
                    if token.startswith("u:") or token.startswith("U:"):
                        try:
                            urgency = int(token[2:])
                        except ValueError:
                            pass
                    elif token.startswith("d:") or token.startswith("D:"):
                        try:
                            difficulty = int(token[2:])
                        except ValueError:
                            pass
                    elif token.startswith("t:") or token.startswith("T:"):
                        try:
                            time_dedicated = int(token[2:])
                        except ValueError:
                            pass
                    elif token.startswith("dl:") or token.startswith("DL:"):
                        deadline = token[3:]
                # Strip tokens from name
                for token in rest.split():
                    if any(token.startswith(p) for p in ("u:", "U:", "d:", "D:", "t:", "T:", "dl:", "DL:")):
                        name = name.replace(token, "", 1).strip()
                if name:
                    task_cmds.create_task(
                        self._selected_directory_id, name,
                        urgency=urgency, difficulty=difficulty,
                        time_dedicated=time_dedicated, deadline=deadline,
                    )
                    self._cmd.set_caption(("done", "Task added "))
                    self._loop.set_alarm_in(2, lambda *a: self._cmd.set_caption(("standout", "\u276f ")))
                    self._refresh_list()
            return
        if cmd.startswith("export"):
            parts = cmd.split(" ", 1)
            path = parts[1].strip() if len(parts) > 1 else "/tmp/taskwatch_export.json"
            if io_cmds.export_data(path):
                self._cmd.set_caption(("done", f"Exported to {path} "))
            else:
                self._cmd.set_caption(("error", "Export failed "))
            self._loop.set_alarm_in(3, lambda *a: self._cmd.set_caption(("standout", "\u276f ")))
            return
        if cmd.startswith("import "):
            path = cmd.split(" ", 1)[1].strip()
            result = io_cmds.import_data(path)
            self._cmd.set_caption(("done" if "failed" not in result else "error", f"{result} "))
            self._loop.set_alarm_in(3, lambda *a: self._cmd.set_caption(("standout", "\u276f ")))
            self._refresh_list()
            return
        if cmd == "bm":
            if self._level == Level.TASKS and self._bulk_selection:
                for tid in list(self._bulk_selection):
                    task_cmds.mark_done(tid)
                self._bulk_selection.clear()
                self._refresh_list()
            return
        if cmd == "bd":
            if self._level == Level.TASKS and self._bulk_selection:
                self._start_wizard(
                    f"Delete {len(self._bulk_selection)} tasks? (y/n): ",
                    self._wiz_bulk_delete,
                )
            return
        if cmd.startswith("bt "):
            if self._level == Level.TASKS and self._bulk_selection:
                tag_name = cmd.split(" ", 1)[1].strip()
                if tag_name:
                    for tid in list(self._bulk_selection):
                        tag_cmds.add_tag_to_task(tid, tag_name)
                    self._bulk_selection.clear()
                    self._refresh_list()
            return
        if cmd.startswith("bv "):
            if self._level == Level.TASKS and self._bulk_selection:
                try:
                    target_dir = int(cmd.split(" ", 1)[1])
                    for tid in list(self._bulk_selection):
                        task_cmds.move_task(tid, target_dir)
                    self._bulk_selection.clear()
                    self._refresh_list()
                except ValueError:
                    pass
            return
        if cmd == "bc":
            self._bulk_selection.clear()
            self._refresh_list()
            return

        if cmd == "stats":
            self._show_stats()
            return
        if cmd == "undo":
            self._undo_last_action()
            return
        if cmd == "week":
            self._show_week_view()
            return
        if cmd.startswith("gs "):
            query = cmd.split(" ", 1)[1].strip()
            if query:
                self._show_global_search(query)
            return
        if cmd.startswith("tag "):
            tag_name = cmd.split(" ", 1)[1].strip()
            if tag_name and self._selected_task_id is not None:
                tag_cmds.add_tag_to_task(self._selected_task_id, tag_name)
                self._refresh_list()
                self._show_detail()
            return
        if cmd.startswith("untag "):
            tag_name = cmd.split(" ", 1)[1].strip()
            if tag_name and self._selected_task_id is not None:
                tag_cmds.remove_tag_from_task(self._selected_task_id, tag_name)
                self._refresh_list()
                self._show_detail()
            return
        if cmd.startswith("ft ") and self._level == Level.TASKS:
            self._filter_tag = cmd.split(" ", 1)[1].strip()
            self._refresh_list()
            self._show_detail()
            return
        if cmd in ("ftc",):
            self._filter_tag = None
            if self._level == Level.TASKS:
                self._refresh_list()
                self._show_detail()
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
                if mins > 0:
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
        if cmd in ("sn a", "sn d"):
            self._sort_field = "name"
            self._sort_dir = "asc" if cmd == "sn a" else "desc"
            if self._level == Level.TASKS:
                self._refresh_list()
            return
        if cmd in ("sdl a", "sdl d"):
            self._sort_field = "deadline"
            self._sort_dir = "asc" if cmd == "sdl a" else "desc"
            if self._level == Level.TASKS:
                self._refresh_list()
            return
        if cmd == "sr":
            self._sort_field = None
            self._sort_dir = "asc"
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
                "Task name (step 1): ",
                self._wiz_task_name,
            )
            return
        self._wiz_name = name
        self._start_wizard(
            "Description (step 2): ",
            partial(self._wiz_task_description, name),
        )

    def _wiz_task_description(self, name: str, desc: str) -> None:
        self._wiz_desc = desc.strip()
        self._start_wizard(
            "Urgency 1-5 (step 3): ",
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
                    "Urgency 1-5 (step 3): ",
                    partial(self._wiz_task_urgency, name),
                )
                return
        self._start_wizard(
            "Difficulty 1-5 (step 4): ",
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
                    "Difficulty 1-5 (step 4): ",
                    partial(self._wiz_task_difficulty, name, urgency),
                )
                return
        self._start_wizard(
            "Time budget minutes (step 5): ",
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
                    "Time budget minutes (step 5): ",
                    partial(self._wiz_task_time, name, urgency, difficulty),
                )
                return
        self._start_wizard(
            "Deadline dd/MM/yyyy or 'none' (step 6): ",
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
                    "Deadline dd/MM/yyyy or 'none' (step 6): ",
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
            "Repeatable? y/n (step 7): ",
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
                "Repeat type daily/weekly/biweekly/monthly/yearly (step 8): ",
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
                description=self._wiz_desc,
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
                "Repeat type daily/weekly/biweekly/monthly/yearly (step 8): ",
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
            "Auto-repeat on finish? y/n (step 9): ",
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
            description=self._wiz_desc,
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
        note_cmds.create_note(self._selected_task_id, today, content)
        self._end_wizard()

    def _cmd_remove(self) -> None:
        sid = self._get_selected_id()
        if sid is None:
            return
        name = self._get_selected_name() or str(sid)
        self._start_wizard(
            f"Delete '{name}'? (y/n): ",
            partial(self._wiz_confirm_delete, sid),
        )

    def _wiz_confirm_delete(self, sid: int, answer: str) -> None:
        if answer.lower() in ("y", "yes"):
            self._do_remove(sid)
        self._end_wizard()

    def _do_remove(self, sid: int) -> None:
        if self._level == Level.ARCHIVES:
            archive_cmds.delete_archive(sid)
        elif self._level == Level.DIRECTORIES:
            directory_cmds.delete_directory(sid)
        elif self._level == Level.TASKS:
            task_data = undo_cmds.get_task_data(sid)
            if task_data is not None:
                conn = db_mod.get_conn()
                notes = conn.execute(
                    "SELECT id, task_id, date, note FROM notes WHERE task_id = ?",
                    (sid,),
                ).fetchall()
                task_data["notes"] = [dict(n) for n in notes]
                undo_cmds.push("task_delete", task_data)
            task_cmds.delete_task(sid)
        elif self._level == Level.NOTES:
            note_cmds.delete_note(sid)
        self._refresh_list()

    def _wiz_bulk_delete(self, answer: str) -> None:
        if answer.lower() in ("y", "yes"):
            for tid in list(self._bulk_selection):
                task_data = undo_cmds.get_task_data(tid)
                if task_data is not None:
                    conn = db_mod.get_conn()
                    notes = conn.execute(
                        "SELECT id, task_id, date, note FROM notes WHERE task_id = ?",
                        (tid,),
                    ).fetchall()
                    task_data["notes"] = [dict(n) for n in notes]
                    undo_cmds.push("task_delete", task_data)
                task_cmds.delete_task(tid)
            self._bulk_selection.clear()
            self._refresh_list()
        self._end_wizard()

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
            "description": task.description,
            "urgency": task.urgency,
            "difficulty": task.difficulty,
            "time_dedicated": task.time_dedicated,
            "deadline": task.deadline,
            "repeatable": task.repeatable,
            "repeatable_type": task.repeatable_type,
            "has_to_be_completed_to_repeat": task.has_to_be_completed_to_repeat,
        }
        self._start_wizard(
            f"Name (step 1) [{task.name}]: ",
            self._wiz_edit_task_name,
        )

    def _wiz_edit_task_name(self, name: str) -> None:
        if name:
            self._edit_ctx["name"] = name
        cur = self._edit_ctx["description"]
        self._start_wizard(
            f"Description (step 2) [{cur}]: ",
            self._wiz_edit_task_description,
        )

    def _wiz_edit_task_description(self, desc: str) -> None:
        if desc:
            self._edit_ctx["description"] = desc
        self._start_wizard(
            f"Urgency 1-5 (step 3) [{self._edit_ctx['urgency']}]: ",
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
            f"Difficulty 1-5 (step 4) [{self._edit_ctx['difficulty']}]: ",
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
            f"Time budget minutes (step 5) [{self._edit_ctx['time_dedicated']}]: ",
            self._wiz_edit_task_time,
        )

    def _wiz_edit_task_time(self, time_str: str) -> None:
        if time_str:
            try:
                self._edit_ctx["time_dedicated"] = int(time_str)
            except ValueError:
                pass
        self._start_wizard(
            f"Deadline (step 6) [{self._edit_ctx['deadline']}]: ",
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
        old_task = task_cmds.get_task(ctx["task_id"])
        if old_task:
            undo_cmds.push("task_edit", {
                "task_id": ctx["task_id"],
                "name": old_task.name,
                "urgency": old_task.urgency,
                "difficulty": old_task.difficulty,
                "time_dedicated": old_task.time_dedicated,
                "deadline": old_task.deadline,
            })
        task_cmds.edit_task(
            ctx["task_id"],
            name=ctx["name"],
            description=ctx.get("description", ""),
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
            undo_cmds.push("task_unfinish", {"task_id": sid})
            task_cmds.mark_not_done(sid)
        else:
            undo_cmds.push("task_finish", {"task_id": sid})
            task_cmds.mark_done(sid)
        self._refresh_list()
        self._show_detail()

    def _enter_search_mode(self) -> None:
        self._in_search_mode = True
        self._filter_text = ""
        self._cmd.set_caption(("/ ", "/"))
        self._cmd.set_edit_text("")
        self._frame.focus_position = "footer"

    def _exit_search_mode(self) -> None:
        self._in_search_mode = False
        self._filter_text = ""
        self._cmd.set_caption(("standout", "\u276f "))
        self._cmd.set_edit_text("")
        self._refresh_list()
        self._show_detail()
        self._focus_body()

    def _on_search_change(self, text: str) -> None:
        self._filter_text = text
        self._refresh_list()
        self._show_detail()

    def _apply_search(self) -> None:
        self._in_search_mode = False
        self._cmd.set_caption(("standout", "\u276f "))
        self._cmd.set_edit_text("")
        self._focus_body()

    def _complete_command(self) -> None:
        text = self._cmd.get_edit_text().strip()
        if not text:
            return
        if not self._tab_matches:
            self._tab_matches = [c for c in COMMANDS if c.startswith(text) or (c.endswith(" ") and text.startswith(c.rstrip()))]
            self._tab_matches.sort()
            self._tab_index = -1
        if not self._tab_matches:
            return
        self._tab_index = (self._tab_index + 1) % len(self._tab_matches)
        completed = self._tab_matches[self._tab_index]
        self._cmd.set_edit_text(completed)
        self._cmd.set_edit_pos(len(completed))

    def _show_help(self) -> None:
        help_w = LineBox(VimListBox(SimpleFocusListWalker([SelectableText(HELP_TEXT)])))
        self._help_overlay = Overlay(
            help_w,
            self._frame,
            align="center",
            width=("relative", 80),
            valign="middle",
            height=("relative", 80),
        )
        self._loop.widget = self._help_overlay

    def _show_stats(self) -> None:
        import shutil

        s = stats_cmds.compute_stats()
        dirs = stats_cmds.all_directory_stats()

        term_width = shutil.get_terminal_size().columns
        internal_width = int(term_width * 0.72) - 2
        bar_width = max(10, min(30, internal_width - 40))

        total_h, total_m = divmod(s["total_time"], 60)

        lines = [
            ("head", "\n  \u2694  TaskWatch+ Stats  \u2694\n\n"),
            ("head", "  Total Tasks:    "),
            str(s["total"]),
            ("head", "         Tags:    "),
            str(s["total_tags"]),
            "\n",
            ("head", "  Time Budget:    "),
            f"{total_h}h {total_m:02d}m",
            "\n\n",
            ("head", "  "),
            *_pct_bar(s["completion_pct"], bar_width),
            f"  {s['completion_pct']:>3}%  {s['finished']}/{s['total']}  Completed\n\n",
            ("head", "  \u26a0 Overdue:  "),
            ("error" if s["overdue"] else "default", str(s["overdue"])),
            ("head", "     \u2713 Today:  "),
            str(s["today_completed"]),
            ("head", "     \u2713 Week:  "),
            str(s["completed_this_week"]),
            "\n\n",
        ]

        if dirs:
            lines.append(("head", "  \u2500\u2500 Directories \u2500\u2500\n\n"))
            for d in dirs[:8]:
                name = d["name"][:20]
                lines.append(f"  {name:<20} ")
                lines.extend(_pct_bar(d["pct"], bar_width))
                lines.append(f"  {d['pct']:>3}%  {d['done']}/{d['total']}\n")
            if len(dirs) > 8:
                lines.append(("dim", "  ... and more\n"))

        stats_w = LineBox(VimListBox(SimpleFocusListWalker([SelectableText(lines)])))
        self._stats_overlay = Overlay(
            stats_w,
            self._frame,
            align="center",
            width=("relative", 72),
            valign="middle",
            height=("relative", 78),
        )
        self._loop.widget = self._stats_overlay

    def _show_global_search(self, query: str) -> None:
        results = task_cmds.search_tasks_global(query)
        if not results:
            raw = [("head", "  Global Search\n\n"), ("dim", "  No tasks match your query.")]
        else:
            raw = [("head", f"  Global Search: {query}\n\n")]
            for i, r in enumerate(results, 1):
                task = r["task"]
                path = f"{r['arch_name']} \u25b8 {r['dir_name']}"
                status = "\u2713" if task.finished else "\u25cb"
                raw.append(f"  {i}. {status} {task.name}")
                raw.append(f"      {path}")
                if task.deadline != "none":
                    raw.append(f"      Deadline: {task.deadline}")
                raw.append("\n")
        gw = LineBox(VimListBox(SimpleFocusListWalker([SelectableText(raw)])))
        self._stats_overlay = Overlay(
            gw,
            self._frame,
            align="center",
            width=("relative", 60),
            valign="middle",
            height=("relative", 60),
        )
        self._loop.widget = self._stats_overlay

    def _show_week_view(self) -> None:
        from datetime import timedelta
        import shutil

        today = date.today()
        monday = today - timedelta(days=today.weekday())
        days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        raw = task_cmds.get_tasks_for_week()

        grouped: dict[str, list] = {d: [] for d in days}
        for r in raw:
            task = r["task"]
            dt = datetime.strptime(task.deadline, "%d/%m/%Y").date()
            day_name = days[dt.weekday()]
            grouped[day_name].append(r)

        term_width = shutil.get_terminal_size().columns
        internal_width = int(term_width * 0.95) - 2
        col_width = max(6, (internal_width - 18) // 7)

        max_tasks = max((len(t) for t in grouped.values()), default=0)
        if max_tasks == 0:
            max_tasks = 1

        date_labels = []
        for i, day_name in enumerate(days):
            day_date = monday + timedelta(days=i)
            if col_width >= 10:
                label = f"{day_name} {day_date.strftime('%d/%m')}"
            elif col_width >= 7:
                label = f"{day_name} {day_date.day:02d}"
            else:
                label = day_name
            if day_date == today:
                label += " \u25c9"
            date_labels.append(label.center(col_width))

        sep = "\u2500" * col_width
        header = " \u2502 ".join(date_labels)
        divider = " \u2502 ".join([sep] * 7)

        task_rows = []
        for row_idx in range(max_tasks):
            row_cells = []
            for day_name in days:
                day_tasks = grouped[day_name]
                if row_idx < len(day_tasks):
                    r = day_tasks[row_idx]
                    t = r["task"]
                    status = "\u2713" if t.finished else "\u25cb"
                    name = t.name[:col_width - 2]
                    cell = f"{status} {name}".ljust(col_width)
                elif row_idx == 0:
                    cell = "\u2014".center(col_width)
                else:
                    cell = " " * col_width
                row_cells.append(cell)
            task_rows.append(" \u2502 ".join(row_cells))

        content = f"  Week of {monday.strftime('%d/%m/%Y')}\n\n{header}\n{divider}\n" + "\n".join(task_rows)

        ww = LineBox(Text(content))
        self._stats_overlay = Overlay(
            ww,
            self._frame,
            align="center",
            width=("relative", 95),
            valign="middle",
            height=("relative", 85),
        )
        self._loop.widget = self._stats_overlay

    def _undo_last_action(self) -> None:
        entry = undo_cmds.pop()
        if entry is None:
            self._cmd.set_caption(("error", "Nothing to undo "))
            self._loop.set_alarm_in(2, lambda *a: self._cmd.set_caption(("standout", "\u276f ")))
            return
        action = entry["action"]
        data = entry["data"]
        success = True
        if action == "task_delete":
            success = undo_cmds.restore_task(data)
            if success and "notes" in data:
                for note_data in data["notes"]:
                    conn = db_mod.get_conn()
                    try:
                        conn.execute(
                            "INSERT INTO notes (id, task_id, date, note) VALUES (?, ?, ?, ?)",
                            (note_data["id"], note_data["task_id"], note_data["date"], note_data["note"]),
                        )
                        conn.commit()
                    except Exception:
                        pass
        elif action == "task_edit":
            t = task_cmds.edit_task(
                data["task_id"],
                name=data["name"],
                urgency=data["urgency"],
                difficulty=data["difficulty"],
                time_dedicated=data["time_dedicated"],
                deadline=data["deadline"],
            )
            success = t is not None
        elif action == "task_finish":
            t = task_cmds.mark_not_done(data["task_id"])
            success = t is not None
        elif action == "task_unfinish":
            t = task_cmds.mark_done(data["task_id"])
            success = t is not None
        if success:
            self._cmd.set_caption(("done", f"Undone: {action} "))
            self._loop.set_alarm_in(2, lambda *a: self._cmd.set_caption(("standout", "\u276f ")))
        self._refresh_list()
        self._show_detail()

    def _check_and_notify_deadlines(self) -> None:
        if not self._notify_deadlines_enabled:
            return
        today_str = date.today().strftime("%d/%m/%Y")
        due_today = task_cmds.get_tasks_due_on(today_str)
        for task in due_today:
            if task.id not in self._notified_deadlines:
                self._notified_deadlines.add(task.id)
                try:
                    subprocess.run(
                        ["notify-send", "-a", "TaskWatch+", "-u", "normal",
                         "Task Due Today", task.name],
                        capture_output=True,
                    )
                except FileNotFoundError:
                    pass
        overdue = task_cmds.get_overdue_tasks()
        for task in overdue:
            if task.id not in self._notified_deadlines:
                self._notified_deadlines.add(task.id)
                try:
                    subprocess.run(
                        ["notify-send", "-a", "TaskWatch+", "-u", "critical",
                         "Overdue Task", f"{task.name} (was due {task.deadline})"],
                        capture_output=True,
                    )
                except FileNotFoundError:
                    pass

    def _start_wizard(
        self, prompt: str, handler: Callable[[str], None]
    ) -> None:
        if self._prompt_handler is not None:
            self._wizard_stack.append({
                "prompt": self._cmd.get_caption(),
                "handler": self._prompt_handler,
            })
        self._prompt_handler = handler
        self._cmd.set_caption(prompt)
        self._cmd.set_edit_text("")
        self._frame.focus_position = "footer"

    def _wizard_back(self) -> None:
        if not self._wizard_stack:
            return
        entry = self._wizard_stack.pop()
        self._prompt_handler = entry["handler"]
        self._cmd.set_caption(entry["prompt"])
        self._cmd.set_edit_text("")

    def _end_wizard(self) -> None:
        self._prompt_handler = None
        self._wizard_stack.clear()
        self._cmd.set_caption(("standout", "\u276f "))
        self._refresh_list()
        self._show_detail()
        try:
            calcurse_cmds.sync_to_calcurse()
        except Exception:
            pass
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

    def _write_timer_file(self) -> None:
        try:
            if not self._timer_running:
                with open("/tmp/taskwatch_timer.json", "w") as f:
                    json.dump({"text": "", "class": "inactive"}, f)
                return
            if self._timer_schedule:
                segments = self._timer_schedule["segments"]
                seg_dur = segments[self._timer_segment_idx]
                remaining = max(0, seg_dur - self._timer_segment_elapsed)
                if self._timer_segment_idx == 0:
                    phase = "INTRO"
                elif self._timer_segment_idx % 2 == 1:
                    phase = "WORK"
                else:
                    phase = "BREAK"
            else:
                remaining = max(0, self._timer_seconds - self._timer_elapsed)
                phase = "TIMER"
            m, s = divmod(remaining, 60)
            pause = " ⏸" if self._timer_paused else ""
            data = {
                "text": f"⏱ {m:02d}:{s:02d}{pause}",
                "alt": phase,
                "class": f"timer-{phase.lower()}",
                "tooltip": f"Timer: {phase} ({m:02d}:{s:02d} remaining)",
            }
            with open("/tmp/taskwatch_timer.json", "w") as f:
                json.dump(data, f)
        except OSError:
            pass

    def _notify_timer_done(self, task_name: str) -> None:
        try:
            subprocess.run(
                ["notify-send", "-a", "TaskWatch+", "Timer Complete", task_name],
                capture_output=True,
            )
        except FileNotFoundError:
            pass

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
        self._write_timer_file()

    def _update_clock_display(self) -> None:
        now = datetime.now()
        if self._timer_running:
            if self._timer_schedule:
                segments = self._timer_schedule["segments"]
                seg_dur = segments[self._timer_segment_idx]
                remaining = max(0, seg_dur - self._timer_segment_elapsed)
                if self._timer_segment_idx == 0:
                    phase = "INTRO"
                    attr = "default"
                elif self._timer_segment_idx % 2 == 1:
                    phase = "WORK"
                    attr = "head"
                else:
                    phase = "BREAK"
                    attr = "dim"
            else:
                remaining = max(0, self._timer_seconds - self._timer_elapsed)
                phase = ""
                attr = "dim"
            m, s = divmod(remaining, 60)
            pause_ind = " \u23f8" if self._timer_paused else ""
            phase_ind = f"\u25b6 {phase}  " if phase else ""
            self._clock_text.set_text(f"{phase_ind}\u23f1 {m:02d}:{s:02d}{pause_ind}")
            self._clock_w.set_attr_map({None: attr})
        else:
            self._clock_text.set_text(now.strftime("%H:%M:%S"))
            self._clock_w.set_attr_map({None: "dim"})
        self._write_timer_file()

    def _tick(self, loop: object, data: object) -> None:
        timer_completed = False
        if self._timer_running and not self._timer_paused:
            if self._timer_schedule:
                segments = self._timer_schedule["segments"]
                self._timer_segment_elapsed += 1
                if self._timer_segment_elapsed >= segments[self._timer_segment_idx]:
                    self._timer_segment_elapsed = 0
                    self._timer_segment_idx += 1
                    if self._timer_segment_idx >= len(segments):
                        if self._timer_task_id is not None:
                            task_cmds.mark_done(self._timer_task_id)
                            task = task_cmds.get_task(self._timer_task_id)
                            if task is not None:
                                self._notify_timer_done(task.name)
                        self._stop_timer()
                        timer_completed = True
            else:
                self._timer_elapsed += 1
                if self._timer_elapsed >= self._timer_seconds:
                    self._timer_elapsed = self._timer_seconds
                    if self._timer_task_id is not None:
                        task_cmds.mark_done(self._timer_task_id)
                        task = task_cmds.get_task(self._timer_task_id)
                        if task is not None:
                            self._notify_timer_done(task.name)
                    self._stop_timer()
                    timer_completed = True

        if timer_completed:
            self._refresh_list()
            self._show_detail()

        self._tick_counter += 1
        if self._tick_counter % 60 == 0:
            task_cmds.reset_overdue_repeatables()
        if self._tick_counter % 300 == 0:
            self._check_and_notify_deadlines()

        self._update_clock_display()
        self._loop.set_alarm_in(1, self._tick)

    def _unhandled_input(self, key: str) -> None:
        if self._loop.widget is not self._frame:
            if key in ("esc", "q"):
                self._loop.widget = self._frame
            return
        if key == " " and self._level == Level.TASKS and self._frame.focus_position == "body":
            if self._current_items:
                idx = self._list_box.focus_position
                if idx < len(self._current_items):
                    item = self._current_items[idx]
                    if item.id in self._bulk_selection:
                        self._bulk_selection.discard(item.id)
                    else:
                        self._bulk_selection.add(item.id)
                    self._refresh_list()
            return
        if key in ("enter", "l") and self._frame.focus_position == "body":
            if self._level == Level.NOTES:
                self._show_detail()
            else:
                self._select()
            return


    def run(self) -> None:
        config_path = __import__("pathlib").Path(__file__).resolve().parent.parent / "config" / "config.txt"
        try:
            for line in open(config_path):
                if ":" in line:
                    k, v = line.split(":", 1)
                    if k.strip() == "NOTIFY_DEADLINES":
                        self._notify_deadlines_enabled = v.strip().lower() == "true"
        except OSError:
            pass
        self._refresh_list()
        self._check_and_notify_deadlines()
        urwid.connect_signal(self._list_walker, "modified", self._show_detail)
        self._loop.set_alarm_in(1, self._tick)
        self._frame.focus_position = "body"
        self._loop.run()


def run_tui() -> None:
    TaskWatchTUI().run()
