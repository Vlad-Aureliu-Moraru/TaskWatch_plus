<img src="TaskWatch+.png" alt="TaskWatch+" width="64" height="64">

# TaskWatch+

A system-integrated terminal task tracker with Waybar support.

- TUI task management (urwid-based)
- Calendar integration (calcurse)
- Directory-based task organization
- Tagging, stats, undo, notes
- Waybar-compatible status display

## Installation

### From a release (recommended)

1. Download `taskwatch-v0.1.1-linux-x86_64.tar.gz` from [Releases](https://github.com/Vlad-Aureliu-Moraru/TaskWatch-/releases)
2. Extract: `tar xzf taskwatch-v0.1.1-linux-x86_64.tar.gz`
3. Install: `cd taskwatch-v0.1.1 && ./install.sh`
4. Launch: `taskwatch`

### From source

```bash
git clone https://github.com/Vlad-Aureliu-Moraru/TaskWatch-.git
cd TaskWatch-
pip install -e .
taskwatch
```

## Desktop Integration

The install script places:
- Binary → `~/.local/bin/taskwatch`
- Desktop entry → `~/.local/share/applications/taskwatch.desktop` (Rofi visible)
- Icon → `~/.local/share/icons/hicolor/256x256/apps/TaskWatch+.png`
