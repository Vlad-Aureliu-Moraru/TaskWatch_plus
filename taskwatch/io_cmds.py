import json
from pathlib import Path
from .db import get_conn


def export_data(path: str) -> bool:
    conn = get_conn()
    try:
        data = {
            "archives": [dict(r) for r in conn.execute("SELECT * FROM archives").fetchall()],
            "directories": [dict(r) for r in conn.execute("SELECT * FROM directories").fetchall()],
            "tasks": [dict(r) for r in conn.execute("SELECT * FROM tasks").fetchall()],
            "notes": [dict(r) for r in conn.execute("SELECT * FROM notes").fetchall()],
            "tags": [dict(r) for r in conn.execute("SELECT * FROM tags").fetchall()],
            "task_tags": [dict(r) for r in conn.execute("SELECT * FROM task_tags").fetchall()],
        }
        Path(path).write_text(json.dumps(data, indent=2, default=str))
        return True
    except Exception:
        return False


def import_data(path: str) -> str:
    conn = get_conn()
    try:
        raw = Path(path).read_text()
        data = json.loads(raw)
    except Exception as e:
        return f"Failed to read file: {e}"

    required = {"archives", "directories", "tasks", "notes", "tags", "task_tags"}
    if not required.issubset(data.keys()):
        return "Missing required keys in import file"

    try:
        for table, rows in data.items():
            if not rows:
                continue
            columns = list(rows[0].keys())
            placeholders = ", ".join("?" for _ in columns)
            col_list = ", ".join(columns)
            for row in rows:
                conn.execute(
                    f"INSERT OR IGNORE INTO {table} ({col_list}) VALUES ({placeholders})",
                    [row[c] for c in columns],
                )
        conn.commit()
        return f"Imported {sum(len(v) for v in data.values())} records"
    except Exception as e:
        return f"Import failed: {e}"
