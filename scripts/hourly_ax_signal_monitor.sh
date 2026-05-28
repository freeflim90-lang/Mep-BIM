#!/bin/zsh
set -euo pipefail

PROJECT_DIR="/Users/choejeong-yeon/LUA BIM LABS"
LOG_DIR="$PROJECT_DIR/logs"
LOG_FILE="$LOG_DIR/hourly_ax_signal_monitor.log"
PYTHON="$PROJECT_DIR/.dev-venv/bin/python"

mkdir -p "$LOG_DIR"

{
  echo "==== $(date '+%Y-%m-%d %H:%M:%S') hourly AX signal monitor start ===="
  cd "$PROJECT_DIR"
  "$PYTHON" scripts/hourly_ax_signal_monitor.py
  echo "==== $(date '+%Y-%m-%d %H:%M:%S') hourly AX signal monitor done ===="
} >> "$LOG_FILE" 2>&1
