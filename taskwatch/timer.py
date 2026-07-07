import json
import re
from pathlib import Path

from .models import Task
from .paths import CONFIG_PATH


_TIME_RE = re.compile(r"^(?:(\d+)h)?(?:(\d+)m)?(?:(\d+)s)?$")


def parse_time_string(s: str) -> float:
    """Parse a human-readable time string into minutes (float).

    Accepts: "15s", "30m", "1h", "1h30m", "1h30m15s", "45" (bare = minutes).
    """
    s = s.strip().lower()
    if not s:
        raise ValueError("empty string")
    if s.isdigit() or (s.startswith("-") and s[1:].isdigit()):
        return float(s)
    m = _TIME_RE.match(s)
    if not m:
        raise ValueError(f"unrecognized time format: {s!r}")
    h, mn, sec = m.groups()
    total = 0.0
    if h:
        total += int(h) * 60.0
    if mn:
        total += int(mn)
    if sec:
        total += int(sec) / 60.0
    return total

WORK_PERCENTAGE_MATRIX = [
    [68, 61, 74, 77, 90],
    [63, 56, 69, 72, 85],
    [58, 52, 66, 67, 80],
    [53, 49, 54, 62, 75],
    [46, 48, 49, 57, 70],
]


def compute_schedule(task: Task) -> dict:
    urgency = max(1, min(5, task.urgency))
    difficulty = max(1, min(5, task.difficulty))
    total_seconds = task.time_dedicated * 60

    if total_seconds <= 0:
        return {"error": "time_dedicated must be > 0"}

    pct = WORK_PERCENTAGE_MATRIX[difficulty - 1][urgency - 1]
    working_seconds = int(round(total_seconds * (pct / 100.0)))
    break_seconds = total_seconds - working_seconds

    intro = 15
    break_seconds -= intro
    if break_seconds < 0:
        intro += break_seconds
        break_seconds = 0

    base_work = working_seconds // difficulty
    rem_work = working_seconds % difficulty
    base_break = break_seconds // difficulty
    rem_break = break_seconds % difficulty

    segments = [intro]
    for i in range(difficulty):
        segments.append(base_work + (1 if i < rem_work else 0))
        segments.append(base_break + (1 if i < rem_break else 0))

    work_min = working_seconds // 60
    break_min = break_seconds // 60

    return {
        "total_minutes": task.time_dedicated,
        "total_seconds": total_seconds,
        "work_pct": pct,
        "working_seconds": working_seconds,
        "work_minutes": work_min,
        "break_seconds": break_seconds,
        "break_minutes": break_min,
        "difficulty": difficulty,
        "urgency": urgency,
        "segments": segments,
        "segment_count": len(segments),
    }


def format_schedule(task: Task) -> str:
    s = compute_schedule(task)
    if "error" in s:
        return f"Error: {s['error']}"

    lines = [
        f"Task:           {task.name} (urgency={s['urgency']}, difficulty={s['difficulty']})",
        f"Total time:     {s['total_minutes']} min ({s['total_seconds']}s)",
        f"Work/Break:     {s['work_pct']}% work → {s['work_minutes']}m work + {s['break_minutes']}m break",
        f"Segments:       {s['segment_count']} total",
    ]

    lines.append(f"  {'0':>3}: {_fmt_duration(s['segments'][0]):>8}  intro")
    idx = 1
    diff = max(1, s["difficulty"])
    for i in range(diff):
        wk = s["segments"][1 + i * 2]
        br = s["segments"][1 + i * 2 + 1]
        lines.append(f"  {idx:>3}: {_fmt_duration(wk):>8}  work ({s['work_minutes'] // diff}m)")
        idx += 1
        lines.append(f"  {idx:>3}: {_fmt_duration(br):>8}  break ({s['break_minutes'] // diff}m)")
        idx += 1

    return "\n".join(lines)


def _fmt_duration(seconds: int) -> str:
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)
    if h:
        return f"{h}h{m:02}m{s:02}s"
    return f"{m}m{s:02}s"


def fmt_timer_val(v: float) -> str:
    if v == int(v):
        return str(int(v))
    return f"{v:.2f}".rstrip("0").rstrip(".")


def read_presets() -> dict[str, dict]:
    presets: dict[str, dict] = {}
    try:
        for line in CONFIG_PATH.read_text().splitlines():
            if line.startswith("TIMER_PRESET:"):
                _, rest = line.split(":", 1)
                if "=" in rest:
                    name, val = rest.split("=", 1)
                    name = name.strip()
                    if "," in val:
                        parts = val.split(",")
                        if len(parts) == 4:
                            try:
                                presets[name] = {
                                    "prep": float(parts[0]),
                                    "work": float(parts[1]),
                                    "break": float(parts[2]),
                                    "laps": int(parts[3]),
                                }
                            except ValueError:
                                pass
                    else:
                        try:
                            mins = float(val)
                            presets[name] = {"prep": 0.0, "work": mins, "break": 0.0, "laps": 1}
                        except ValueError:
                            pass
    except (OSError, ValueError):
        pass
    return presets


def write_presets(presets: dict[str, dict]) -> None:
    cfg = CONFIG_PATH
    existing_clean: list[str] = []
    try:
        for line in cfg.read_text().splitlines():
            if not line.startswith("TIMER_PRESET:"):
                existing_clean.append(line)
    except OSError:
        pass
    for name, p in sorted(presets.items()):
        existing_clean.append(
            f"TIMER_PRESET:{name}={fmt_timer_val(p['prep'])},{fmt_timer_val(p['work'])},{fmt_timer_val(p['break'])},{p['laps']}"
        )
    cfg.parent.mkdir(parents=True, exist_ok=True)
    cfg.write_text("\n".join(existing_clean) + "\n")


def atomic_write_json(path: Path, data: object) -> None:
    tmp = path.with_suffix(".tmp")
    with open(tmp, "w") as f:
        json.dump(data, f)
    tmp.rename(path)
