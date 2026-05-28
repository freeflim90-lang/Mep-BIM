#!/bin/bash
# ================================================================
# run_monthly.sh — 매월 1일 자동 업체 수집 실행 스크립트
# cron: 0 9 1 * * /bin/bash "/Users/choejeong-yeon/LUA BIM LABS/scripts/outbound_sales/run_monthly.sh"
# ================================================================

SCRIPT_DIR="/Users/choejeong-yeon/LUA BIM LABS/scripts/outbound_sales"
VENV="$SCRIPT_DIR/.venv/bin/python3"
LOG_DIR="$SCRIPT_DIR/data/logs"
LOG_FILE="$LOG_DIR/$(date '+%Y%m').log"

mkdir -p "$LOG_DIR"

echo "======================================" >> "$LOG_FILE"
echo "[$(date '+%Y-%m-%d %H:%M:%S')] 월간 업체 수집 시작" >> "$LOG_FILE"
echo "======================================" >> "$LOG_FILE"

cd "$SCRIPT_DIR"

# 1) 업체 수집 + 이메일 추출
"$VENV" main.py update >> "$LOG_FILE" 2>&1

echo "[$(date '+%Y-%m-%d %H:%M:%S')] 수집 완료" >> "$LOG_FILE"

# 2) 구글 시트 동기화 (신규 업체만 추가)
"$VENV" main.py sheets-sync >> "$LOG_FILE" 2>&1

echo "[$(date '+%Y-%m-%d %H:%M:%S')] 구글 시트 동기화 완료" >> "$LOG_FILE"
echo "" >> "$LOG_FILE"
