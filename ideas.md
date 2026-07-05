# TaskWatch+ — Ideas for future nice touches

## Micro-UX (small, quick wins)

- **Natural language deadlines** — accept "tomorrow", "next friday", "in 3 days" when creating/editing tasks instead of only `dd/MM/yyyy`.
- **Relative deadline display** — show "Due in 2 days" or "Overdue by 1 day" in the task detail pane instead of raw dates.
- **Fuzzy global search** — `:gs` currently does substring matching; fuzzy scoring would feel much snappier.
- **Task snooze** — `:snooze 3` to bump a task's deadline forward N days without going through the edit wizard.
- **Quick duplicate** — `:dup` to clone the selected task with the same urgency/difficulty/time budget.
- **Context-sensitive help** — pressing `?` shows only shortcuts relevant to the current level (archives vs tasks vs notes), rather than the full wall of text.
- **Search highlighting** — highlight the matching substring inside task/note names when filtering.

## Gamification / Delight

- **Completion streak tracker** — count consecutive days with finished tasks; show a small flame indicator in the status bar.
- **Completion celebration** — brief ASCII confetti or a random celebratory phrase when finishing a task (e.g., "Crushed it!", "Another one down").
- **Daily standup generator** — `:standup` generates a markdown bullet list of yesterday's completed tasks for copying into Slack/stand-up notes.
- **Focus score** — a simple metric combining timer usage + tasks completed today, shown in stats.

## Timer & Focus

- **Idle auto-pause** — query X11/Wayland idle time; if the user is AFK for >5 min, auto-pause the timer and notify.
- **Focus mode** — `:focus` hides the list pane and shows only the current task name + a big centered timer countdown.
- **Timer session logging** — actually store how many minutes the timer ran per task, then show "Budgeted 60m / Spent 45m" in task detail.
- **Timer presets** — save common durations (e.g., "pomodoro = 25m", "deep work = 90m") and start with `:st pomodoro`.

## Organization

- **Task pinning** — pin important tasks so they float to the top regardless of sort order.
- **Task dependencies** — simple `blocks`/`blocked-by` fields; blocked tasks show a 🔒 icon and dimmed color.
- **Directory default properties** — new tasks in a directory inherit its average urgency/difficulty unless overridden.
- **Smart bulk selection** — `:select all overdue` or `:select all due today` to bulk-select matching tasks.
- **Subtasks / checklists** — lightweight checkbox items within a task (separate table or parsed from note markdown).

## System Integration

- **Shell completions** — generate bash/zsh/fish completions for `taskwatch` subcommands.
- **Terminal title updates** — set the window title to "TaskWatch+ (12 pending)" so it shows in the window manager.
- **Waybar badge when idle** — show the count of overdue tasks in Waybar even when no timer is running.
- **Mouse support in TUI** — urwid supports it; clicking archives/directories/tasks to navigate feels surprisingly good.

## Data & Export

- **Export to Markdown** — `:export-md` generates a clean markdown report of an archive/directory with task statuses.
- **Completion heatmap** — GitHub-style contribution calendar in stats showing which days had task completions.
- **Task time estimate quality** — track budgeted vs actual timer time and show "Estimate accuracy: 85%" in stats.
