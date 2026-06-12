#!/bin/zsh
set -euo pipefail

PROJECT_DIR="/Users/choejeong-yeon/LUA BIM LABS"
RUNTIME_DIR="$PROJECT_DIR/runtime"
LOG_DIR="$PROJECT_DIR/logs"
LOG_FILE="$LOG_DIR/cloudflared-quick-revit-api.log"
URL_FILE="$RUNTIME_DIR/revit_luachat_backend_url.txt"
INSTALL_SNIPPET="$RUNTIME_DIR/install_revit_luachat_with_current_tunnel.bat"

mkdir -p "$RUNTIME_DIR" "$LOG_DIR"

if ! command -v cloudflared >/dev/null 2>&1; then
  echo "cloudflared is not installed."
  echo "Install it with: brew install cloudflared"
  exit 1
fi

if ! lsof -nP -iTCP:8000 -sTCP:LISTEN >/dev/null 2>&1; then
  echo "LUA BIM LABS backend is not listening on port 8000."
  echo "Start it first with: scripts/start_server.sh"
  exit 1
fi

pkill -f "cloudflared tunnel --url http://127.0.0.1:8000" >/dev/null 2>&1 || true
: > "$LOG_FILE"

nohup cloudflared tunnel --url http://127.0.0.1:8000 --no-autoupdate \
  >> "$LOG_FILE" 2>&1 &

echo "Waiting for Cloudflare Quick Tunnel URL..."
for _ in {1..60}; do
  URL="$(grep -Eo 'https://[-a-zA-Z0-9]+\.trycloudflare\.com' "$LOG_FILE" | tail -n 1 || true)"
  if [ -n "$URL" ]; then
    echo "$URL" > "$URL_FILE"
    cat > "$INSTALL_SNIPPET" <<EOF
@echo off
set BACKEND_URL=$URL
echo Installing RevitLUAChat with backend %BACKEND_URL%
RevitLUAChat_Setup_v1.2.1.exe /BackendUrl="%BACKEND_URL%"
EOF
    echo "Quick Tunnel URL: $URL"
    echo "Saved to: $URL_FILE"
    echo "Windows installer snippet: $INSTALL_SNIPPET"
    exit 0
  fi
  sleep 1
done

echo "Cloudflare Quick Tunnel URL was not detected."
echo "Check log: $LOG_FILE"
exit 2
