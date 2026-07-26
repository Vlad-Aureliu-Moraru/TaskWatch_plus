import json
from pathlib import Path

THEMES_DIR = Path(__file__).resolve().parent.parent / "config" / "themes"

_FOCUS_NAMES = {"focus"}
_FOCUS_SUFFIX = "_focus"


def list_themes() -> list[dict]:
    if not THEMES_DIR.is_dir():
        return []
    themes = []
    for p in sorted(THEMES_DIR.glob("*.json")):
        try:
            with open(p) as f:
                data = json.load(f)
            themes.append({
                "file": p.name,
                "name": data.get("name", p.stem),
            })
        except (json.JSONDecodeError, OSError):
            pass
    return themes


def load_theme(name: str) -> dict:
    path = THEMES_DIR / f"{name}.json"
    if not path.exists():
        path = THEMES_DIR / "default.json"
    with open(path) as f:
        return json.load(f)


def apply_theme(palette: list, theme_data: dict) -> None:
    overrides = theme_data.get("palette", {})
    for i, entry in enumerate(palette):
        ename = entry[0]
        if ename in _FOCUS_NAMES or ename.endswith(_FOCUS_SUFFIX):
            continue
        if ename in overrides:
            palette[i] = (ename, *overrides[ename])
