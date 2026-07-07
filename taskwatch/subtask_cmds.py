from .db import get_conn
from .models import Subtask


def create_subtask(task_id: int, content: str) -> Subtask:
    conn = get_conn()
    max_pos = conn.execute(
        "SELECT COALESCE(MAX(position), -1) FROM subtasks WHERE task_id = ?",
        (task_id,),
    ).fetchone()[0]
    cur = conn.execute(
        "INSERT INTO subtasks (task_id, content, position) VALUES (?, ?, ?)",
        (task_id, content, max_pos + 1),
    )
    conn.commit()
    return Subtask(id=cur.lastrowid, task_id=task_id, content=content, position=max_pos + 1)


def delete_subtask(subtask_id: int) -> bool:
    conn = get_conn()
    cur = conn.execute("DELETE FROM subtasks WHERE id = ?", (subtask_id,))
    conn.commit()
    return cur.rowcount > 0


def list_subtasks(task_id: int) -> list[Subtask]:
    conn = get_conn()
    rows = conn.execute(
        "SELECT * FROM subtasks WHERE task_id = ? ORDER BY position, id",
        (task_id,),
    ).fetchall()
    return [Subtask(id=r["id"], task_id=r["task_id"], content=r["content"],
                    finished=bool(r["finished"]), position=r["position"])
            for r in rows]


def mark_done(subtask_id: int) -> Subtask | None:
    conn = get_conn()
    cur = conn.execute(
        "UPDATE subtasks SET finished = 1 WHERE id = ?", (subtask_id,),
    )
    conn.commit()
    if cur.rowcount == 0:
        return None
    row = conn.execute("SELECT * FROM subtasks WHERE id = ?", (subtask_id,)).fetchone()
    return Subtask(id=row["id"], task_id=row["task_id"], content=row["content"],
                   finished=bool(row["finished"]), position=row["position"])


def mark_not_done(subtask_id: int) -> Subtask | None:
    conn = get_conn()
    cur = conn.execute(
        "UPDATE subtasks SET finished = 0 WHERE id = ?", (subtask_id,),
    )
    conn.commit()
    if cur.rowcount == 0:
        return None
    row = conn.execute("SELECT * FROM subtasks WHERE id = ?", (subtask_id,)).fetchone()
    return Subtask(id=row["id"], task_id=row["task_id"], content=row["content"],
                   finished=bool(row["finished"]), position=row["position"])


def update_subtask(subtask_id: int, content: str) -> Subtask | None:
    conn = get_conn()
    cur = conn.execute(
        "UPDATE subtasks SET content = ? WHERE id = ?", (content, subtask_id),
    )
    conn.commit()
    if cur.rowcount == 0:
        return None
    row = conn.execute("SELECT * FROM subtasks WHERE id = ?", (subtask_id,)).fetchone()
    return Subtask(id=row["id"], task_id=row["task_id"], content=row["content"],
                   finished=bool(row["finished"]), position=row["position"])

