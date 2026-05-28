#!/bin/zsh
set -euo pipefail

PROJECT_DIR="/Users/choejeong-yeon/LUA BIM LABS"
LOG_DIR="$PROJECT_DIR/logs"
LOG_FILE="$LOG_DIR/weekly_ax_strategy_review.log"
PYTHON="$PROJECT_DIR/.dev-venv/bin/python"

mkdir -p "$LOG_DIR"

{
  echo "==== $(date '+%Y-%m-%d %H:%M:%S') weekly AX strategy review start ===="
  cd "$PROJECT_DIR"
  "$PYTHON" scripts/weekly_ax_strategy_review.py
  echo "==== $(date '+%Y-%m-%d %H:%M:%S') weekly AX strategy review done ===="
} >> "$LOG_FILE" 2>&1
