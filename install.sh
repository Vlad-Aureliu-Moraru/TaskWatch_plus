#!/bin/sh
set -e

BIN_DIR="${HOME}/.local/bin"
APP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons/hicolor/256x256/apps"
TASKWATCH_DIR="${HOME}/.local/share/taskwatch"

if [ -f "taskwatch/__main__.py" ]; then
    # Installing from source — use pip
    pip install . --quiet --break-system-packages 2>/dev/null || pip install . --quiet
    ENTRY_POINT=$(command -v taskwatch) || "${HOME}/.local/bin/taskwatch" 2>/dev/null || echo "taskwatch"
    echo "  (installed via pip, entry point: ${ENTRY_POINT})"
else
    # Installing from a release tarball with pre-built binary
    mkdir -p "$BIN_DIR"
    cp taskwatch "$BIN_DIR/"
    chmod +x "$BIN_DIR/taskwatch"
    ENTRY_POINT="${BIN_DIR}/taskwatch"
fi

mkdir -p "$APP_DIR" "$ICON_DIR" "$TASKWATCH_DIR"

cp update.sh "$TASKWATCH_DIR/" 2>/dev/null || true
chmod +x "$TASKWATCH_DIR/update.sh" 2>/dev/null || true

cp TaskWatch+.png "$ICON_DIR/" 2>/dev/null || true

sed -e "s|^Exec=.*|Exec=${ENTRY_POINT} tui|" taskwatch.desktop > "$APP_DIR/taskwatch.desktop"

command -v update-desktop-database >/dev/null 2>&1 && update-desktop-database "$APP_DIR"
command -v gtk-update-icon-cache >/dev/null 2>&1 && gtk-update-icon-cache -f -t "$HOME/.local/share/icons" 2>/dev/null || true

echo "Installed. Launch: taskwatch tui"
