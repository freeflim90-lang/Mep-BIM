#!/bin/zsh
set -euo pipefail

PROJECT_DIR="/Users/choejeong-yeon/LUA BIM LABS"
LOG_DIR="$PROJECT_DIR/logs"
LOG_FILE="$LOG_DIR/monthly_knowledge_update.log"

mkdir -p "$LOG_DIR"

{
  echo "==== $(date '+%Y-%m-%d %H:%M:%S') monthly script deprecated; forwarding to daily knowledge update ===="
  "$PROJECT_DIR/scripts/daily_knowledge_update.sh"
  echo "==== $(date '+%Y-%m-%d %H:%M:%S') monthly compatibility forwarding done ===="
} >> "$LOG_FILE" 2>&1
