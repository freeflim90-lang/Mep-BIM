#!/bin/bash
# LUA BIM LABS 지식 베이스 동기화 스크립트
# GitHub ↔ 로컬 동기화 (속도 영향 없음 - 로컬 캐시 방식)

PROJECT_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
LOG_FILE="$PROJECT_ROOT/logs/sync_knowledge.log"
mkdir -p "$PROJECT_ROOT/logs"

echo "[$(date '+%Y-%m-%d %H:%M:%S')] 동기화 시작" >> "$LOG_FILE"

cd "$PROJECT_ROOT" || exit 1

# 로컬 변경사항 있으면 먼저 커밋
if ! git diff --quiet || ! git diff --cached --quiet; then
    git add data/knowledge_base/ data/qa_dataset/ data/technical_pdfs/ data/bim_scripts/ scripts/
    git commit -m "자동 동기화: $(date '+%Y-%m-%d %H:%M')"
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] 로컬 변경사항 커밋" >> "$LOG_FILE"
fi

# GitHub에서 최신 내용 가져오기
git pull origin main --rebase 2>> "$LOG_FILE"
if [ $? -eq 0 ]; then
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] pull 성공" >> "$LOG_FILE"
else
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] pull 실패" >> "$LOG_FILE"
fi

# 로컬 변경사항 push
git push origin main 2>> "$LOG_FILE"
if [ $? -eq 0 ]; then
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] push 성공" >> "$LOG_FILE"
else
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] push 실패 (무시)" >> "$LOG_FILE"
fi

echo "[$(date '+%Y-%m-%d %H:%M:%S')] 동기화 완료" >> "$LOG_FILE"
