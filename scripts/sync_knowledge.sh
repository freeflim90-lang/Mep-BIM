#!/bin/bash
# LUA BIM LABS 지식 베이스 동기화 스크립트
# GitHub ↔ 로컬 동기화 (속도 영향 없음 - 로컬 캐시 방식)

PROJECT_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
LOG_FILE="$PROJECT_ROOT/logs/sync_knowledge.log"
RUNNING_MARKER="$PROJECT_ROOT/logs/.daily_knowledge_update_running"
mkdir -p "$PROJECT_ROOT/logs"

echo "[$(date '+%Y-%m-%d %H:%M:%S')] 동기화 시작" >> "$LOG_FILE"

cd "$PROJECT_ROOT" || exit 1

if [ -f "$RUNNING_MARKER" ]; then
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] 지식 업데이트 실행 중 - 동기화 스킵" >> "$LOG_FILE"
    exit 0
fi

# 로컬 변경사항 있으면 먼저 커밋
if ! git diff --quiet || ! git diff --cached --quiet; then
    git add \
        .gitignore \
        data/knowledge_base/ \
        data/qa_dataset/ \
        data/technical_pdfs/ \
        scripts/*.py \
        scripts/*.sh \
        scripts/requirements*.txt \
        scripts/bim_education/ \
        scripts/outbound_sales/*.py \
        scripts/outbound_sales/*.sh \
        scripts/outbound_sales/requirements.txt \
        scripts/outbound_sales/templates/
    git commit -m "자동 동기화: $(date '+%Y-%m-%d %H:%M')"
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] 로컬 변경사항 커밋" >> "$LOG_FILE"
fi

# push 전 outgoing commit에 민감 파일이 섞였으면 중단
if git rev-parse --verify origin/main >/dev/null 2>&1; then
    if git diff --name-only origin/main..HEAD | grep -Eq '(^|/)service_account\.json$|(^|/)client_secret\.json$|(^|/)token\.json$|(^|/)\.env$'; then
        echo "[$(date '+%Y-%m-%d %H:%M:%S')] push 중단: outgoing commit에 민감 파일 포함" >> "$LOG_FILE"
        exit 1
    fi
fi

# GitHub에서 최신 내용 가져오기
git pull origin main --rebase --autostash 2>> "$LOG_FILE"
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
