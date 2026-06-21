import re
from pathlib import Path
from datetime import datetime
from . import task_cmds
from .models import Task

CALCURSE_DIR = Path.home() / ".local" / "share" / "calcurse"
APTS_FILE = CALCURSE_DIR / "apts"
TW_TAG = "[TW]"
TW_RE = re.compile(r"^\d{2}/\d{2}/\d{4}.*\|" + re.escape(TW_TAG))


def _ddmmyyyy_to_mmddyyyy(d: str) -> str:
    parts = d.split("/")
    return f"{parts[1]}/{parts[0]}/{parts[2]}"


def read_apts() -> list[str]:
    if not APTS_FILE.exists():
        return []
    return [line.rstrip("\n") for line in APTS_FILE.read_text().splitlines() if line.strip()]


def task_to_apt_line(task: Task) -> str | None:
    if task.deadline in (None, "", "none"):
        return None
    mmddyy = _ddmmyyyy_to_mmddyyyy(task.deadline)
    return f"{mmddyy} @ 00:00 -> {mmddyy} @ 23:59|{TW_TAG} {task.name}"


def sync_to_calcurse() -> int:
    tasks = task_cmds.list_tasks()
    new_lines = []
    for t in tasks:
        line = task_to_apt_line(t)
        if line:
            new_lines.append(line)

    existing = read_apts()
    existing = [l for l in existing if not TW_RE.match(l)]

    all_lines = existing + new_lines

    CALCURSE_DIR.mkdir(parents=True, exist_ok=True)
    APTS_FILE.write_text("\n".join(all_lines) + "\n")

    return len(new_lines)
