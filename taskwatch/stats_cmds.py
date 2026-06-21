from datetime import date, timedelta
from .db import get_conn


def compute_stats() -> dict:
    conn = get_conn()

    total = conn.execute("SELECT COUNT(*) FROM tasks").fetchone()[0]
    finished = conn.execute("SELECT COUNT(*) FROM tasks WHERE finished = 1").fetchone()[0]
    pending = total - finished

    today_str = date.today().strftime("%d/%m/%Y")
    today_completed = conn.execute(
        "SELECT COUNT(*) FROM tasks WHERE finished = 1 AND finished_date = ?",
        (today_str,),
    ).fetchone()[0]

    monday = (date.today() - timedelta(days=date.today().weekday())).strftime("%d/%m/%Y")
    completed_this_week = conn.execute(
        "SELECT COUNT(*) FROM tasks WHERE finished = 1 AND finished_date >= ?",
        (monday,),
    ).fetchone()[0]

    overdue = conn.execute(
        """SELECT COUNT(*) FROM tasks
           WHERE finished = 0 AND deadline != 'none' AND deadline < ?""",
        (today_str,),
    ).fetchone()[0]

    total_time = conn.execute(
        "SELECT COALESCE(SUM(time_dedicated), 0) FROM tasks"
    ).fetchone()[0]

    completion_pct = round((finished / total * 100) if total else 0)

    total_tags = conn.execute("SELECT COUNT(*) FROM tags").fetchone()[0]

    return {
        "total": total,
        "finished": finished,
        "pending": pending,
        "today_completed": today_completed,
        "completed_this_week": completed_this_week,
        "overdue": overdue,
        "total_time": total_time,
        "completion_pct": completion_pct,
        "total_tags": total_tags,
    }


def directory_stats(directory_id: int) -> tuple[int, int]:
    conn = get_conn()
    total = conn.execute(
        "SELECT COUNT(*) FROM tasks WHERE directory_id = ?",
        (directory_id,),
    ).fetchone()[0]
    finished = conn.execute(
        "SELECT COUNT(*) FROM tasks WHERE directory_id = ? AND finished = 1",
        (directory_id,),
    ).fetchone()[0]
    return (total, finished)


def all_directory_stats() -> list[dict]:
    conn = get_conn()
    rows = conn.execute(
        """SELECT d.name, a.name AS arch_name,
                  COUNT(t.id) AS total,
                  SUM(CASE WHEN t.finished THEN 1 ELSE 0 END) AS done
           FROM directories d
           JOIN archives a ON d.archive_id = a.id
           LEFT JOIN tasks t ON t.directory_id = d.id
           GROUP BY d.id
           ORDER BY done * 1.0 / MAX(total, 1) DESC"""
    ).fetchall()
    return [
        {
            "name": f"{r['arch_name']} \u25b8 {r['name']}",
            "total": r["total"],
            "done": r["done"],
            "pct": round((r["done"] / r["total"] * 100) if r["total"] else 0),
        }
        for r in rows
    ]
