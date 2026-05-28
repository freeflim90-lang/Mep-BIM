#!/bin/bash
# LUA BIM LABS 백엔드 서버 시작 스크립트

PROJECT_DIR="/Users/choejeong-yeon/LUA BIM LABS"
VENV_UVICORN="$PROJECT_DIR/.dev-venv/bin/uvicorn"
LOG_DIR="$PROJECT_DIR/logs"

mkdir -p "$LOG_DIR"

# .env 환경변수 로드
if [ -f "$PROJECT_DIR/.env" ]; then
    set -a
    source "$PROJECT_DIR/.env"
    set +a
fi

cd "$PROJECT_DIR"
exec "$VENV_UVICORN" backend.server_total:app \
    --host 0.0.0.0 \
    --port 8000 \
    >> "$LOG_DIR/server.log" 2>&1
