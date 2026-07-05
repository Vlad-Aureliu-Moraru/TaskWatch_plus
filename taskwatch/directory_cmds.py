import sqlite3

from .db import get_conn
from .models import Directory


def list_directories(archive_id: int | None = None) -> list[Directory]:
    conn = get_conn()
    if archive_id is not None:
        rows = conn.execute(
            "SELECT id, archive_id, name FROM directories WHERE archive_id = ? ORDER BY id",
            (archive_id,),
        ).fetchall()
    else:
        rows = conn.execute(
            "SELECT id, archive_id, name FROM directories ORDER BY id"
        ).fetchall()
    return [Directory(id=r["id"], archive_id=r["archive_id"], name=r["name"]) for r in rows]


def create_directory(archive_id: int, name: str) -> Directory | None:
    conn = get_conn()
    try:
        cur = conn.execute(
            "INSERT INTO directories (archive_id, name) VALUES (?, ?)",
            (archive_id, name),
        )
        conn.commit()
        return Directory(id=cur.lastrowid, archive_id=archive_id, name=name)
    except sqlite3.IntegrityError:
        return None


def rename_directory(directory_id: int, name: str) -> Directory | None:
    conn = get_conn()
    try:
        cur = conn.execute(
            "UPDATE directories SET name = ? WHERE id = ?", (name, directory_id)
        )
        conn.commit()
    except sqlite3.IntegrityError:
        return None
    if cur.rowcount == 0:
        return None
    row = conn.execute("SELECT id, archive_id, name FROM directories WHERE id = ?", (directory_id,)).fetchone()
    if row is None:
        return None
    return Directory(id=row["id"], archive_id=row["archive_id"], name=row["name"])


def delete_directory(directory_id: int) -> bool:
    conn = get_conn()
    cur = conn.execute("DELETE FROM directories WHERE id = ?", (directory_id,))
    conn.commit()
    return cur.rowcount > 0


def get_directory(dir_id: int) -> Directory | None:
    conn = get_conn()
    row = conn.execute(
        "SELECT id, archive_id, name FROM directories WHERE id = ?", (dir_id,)
    ).fetchone()
    if row is None:
        return None
    return Directory(id=row["id"], archive_id=row["archive_id"], name=row["name"])


def get_directory_defaults(directory_id: int) -> dict:
    conn = get_conn()
    row = conn.execute(
        "SELECT ROUND(AVG(urgency), 0) AS avg_u, ROUND(AVG(difficulty), 0) AS avg_d "
        "FROM tasks WHERE directory_id = ?",
        (directory_id,),
    ).fetchone()
    avg_u = int(row["avg_u"]) if row and row["avg_u"] is not None else 1
    avg_d = int(row["avg_d"]) if row and row["avg_d"] is not None else 1
    return {"urgency": max(1, min(5, avg_u)), "difficulty": max(1, min(5, avg_d))}


def search_directories_global(query: str, limit: int = 10) -> list[Directory]:
    conn = get_conn()
    like = f"%{query}%"
    rows = conn.execute(
        "SELECT id, archive_id, name FROM directories WHERE LOWER(name) LIKE LOWER(?) ORDER BY name LIMIT ?",
        (like, limit),
    ).fetchall()
    return [Directory(id=r["id"], archive_id=r["archive_id"], name=r["name"]) for r in rows]


def move_directory(dir_id: int, new_archive_id: int) -> Directory | None:
    conn = get_conn()
    arch_exists = conn.execute(
        "SELECT id FROM archives WHERE id = ?", (new_archive_id,)
    ).fetchone()
    if arch_exists is None:
        return None
    conn.execute(
        "UPDATE directories SET archive_id = ? WHERE id = ?",
        (new_archive_id, dir_id),
    )
    conn.commit()
    row = conn.execute("SELECT id, archive_id, name FROM directories WHERE id = ?", (dir_id,)).fetchone()
    if row is None:
        return None
    return Directory(id=row["id"], archive_id=row["archive_id"], name=row["name"])
