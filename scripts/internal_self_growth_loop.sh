#!/bin/zsh
set -euo pipefail

PROJECT_DIR="/Users/choejeong-yeon/LUA BIM LABS"
LOG_DIR="$PROJECT_DIR/logs"
LOG_FILE="$LOG_DIR/internal_self_growth_loop.log"
PYTHON="$PROJECT_DIR/.dev-venv/bin/python"
RUNNING_MARKER="$LOG_DIR/.internal_self_growth_loop_running"

mkdir -p "$LOG_DIR"

if [[ -f "$RUNNING_MARKER" ]]; then
  echo "[$(date '+%Y-%m-%d %H:%M:%S')] internal self growth loop already running - skip" >> "$LOG_FILE"
  exit 0
fi

touch "$RUNNING_MARKER"
trap 'rm -f "$RUNNING_MARKER"' EXIT

{
  echo "==== $(date '+%Y-%m-%d %H:%M:%S') internal self growth loop start ===="
  cd "$PROJECT_DIR"
  "$PYTHON" scripts/internal_self_growth_loop.py
  echo "==== $(date '+%Y-%m-%d %H:%M:%S') internal self growth loop done ===="
} >> "$LOG_FILE" 2>&1
