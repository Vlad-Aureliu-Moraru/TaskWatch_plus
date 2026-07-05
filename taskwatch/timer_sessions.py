from datetime import date

from .db import get_conn


def log_session(task_id: int | None, duration_seconds: int) -> None:
    if task_id is None:
        return
    conn = get_conn()
    conn.execute(
        "INSERT INTO timer_sessions (task_id, duration_seconds, date) VALUES (?, ?, ?)",
        (task_id, duration_seconds, date.today().isoformat()),
    )
    conn.commit()


def get_total_time_for_task(task_id: int) -> int:
    conn = get_conn()
    row = conn.execute(
        "SELECT COALESCE(SUM(duration_seconds), 0) FROM timer_sessions WHERE task_id = ?",
        (task_id,),
    ).fetchone()
    return row[0]
