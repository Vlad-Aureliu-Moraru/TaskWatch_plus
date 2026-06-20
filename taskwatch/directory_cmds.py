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


def create_directory(archive_id: int, name: str) -> Directory:
    conn = get_conn()
    cur = conn.execute(
        "INSERT INTO directories (archive_id, name) VALUES (?, ?)",
        (archive_id, name),
    )
    conn.commit()
    return Directory(id=cur.lastrowid, archive_id=archive_id, name=name)


def rename_directory(directory_id: int, name: str) -> Directory | None:
    conn = get_conn()
    cur = conn.execute(
        "UPDATE directories SET name = ? WHERE id = ?", (name, directory_id)
    )
    conn.commit()
    if cur.rowcount == 0:
        return None
    return Directory(id=directory_id, archive_id=0, name=name)


def delete_directory(directory_id: int) -> bool:
    conn = get_conn()
    cur = conn.execute("DELETE FROM directories WHERE id = ?", (directory_id,))
    conn.commit()
    return cur.rowcount > 0
