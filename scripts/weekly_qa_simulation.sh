#!/bin/zsh
# weekly_qa_simulation.sh — Q&A 품질 시뮬레이션 주간 실행 래퍼

PROJECT_DIR="/Users/choejeong-yeon/LUA BIM LABS"
PYTHON="$PROJECT_DIR/.venv/bin/python3"
[ ! -f "$PYTHON" ] && PYTHON=$(which python3)

LOG_DIR="$PROJECT_DIR/logs/qa_simulation"
TODAY=$(date +%Y-%m-%d)
LOG_FILE="$LOG_DIR/weekly_qa_simulation_${TODAY}.log"
DONE_MARKER="$LOG_DIR/.done_${TODAY}"

mkdir -p "$LOG_DIR"

if [ -f "$DONE_MARKER" ]; then
  echo "[$TODAY] 이미 오늘 실행 완료. 스킵." | tee -a "$LOG_FILE"
  exit 0
fi

echo "==== $(date '+%Y-%m-%d %H:%M:%S') QA 시뮬레이션 시작 ====" | tee -a "$LOG_FILE"
cd "$PROJECT_DIR"

"$PYTHON" scripts/simulate_qa_quality.py --verbose 2>&1 | tee -a "$LOG_FILE"
EXIT_CODE=${PIPESTATUS[0]}

echo "==== $(date '+%Y-%m-%d %H:%M:%S') QA 시뮬레이션 완료 (exit=$EXIT_CODE) ====" | tee -a "$LOG_FILE"

# 결과를 텔레그램으로 전송 (서버가 실행 중인 경우)
REPORT_FILE="$LOG_DIR/qa_simulation_${TODAY}.md"
if [ -f "$REPORT_FILE" ]; then
  SUMMARY=$(grep -E "^결과:|^판정:|^실행일:" "$REPORT_FILE" | head -5 | tr '\n' ' ')
  curl -s -X POST "http://127.0.0.1:8000/api/telegram/send" \
    -H "Content-Type: application/json" \
    -d "{\"text\": \"📊 주간 QA 시뮬레이션\\n$SUMMARY\\n리포트: logs/qa_simulation/qa_simulation_${TODAY}.md\"}" \
    2>/dev/null || true
fi

touch "$DONE_MARKER"
exit $EXIT_CODE
