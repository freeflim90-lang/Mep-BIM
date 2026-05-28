#!/bin/zsh
set -euo pipefail

PROJECT_DIR="/Users/choejeong-yeon/LUA BIM LABS"
LOG_DIR="$PROJECT_DIR/logs"
TUNNEL_NAME="${CLOUDFLARE_TUNNEL_NAME:-lua-bim-labs-revit-api}"
CONFIG_FILE="${CLOUDFLARE_TUNNEL_CONFIG:-$HOME/.cloudflared/config.yml}"

mkdir -p "$LOG_DIR"

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

if [ ! -f "$CONFIG_FILE" ]; then
  echo "Cloudflare Tunnel is not configured yet."
  echo "Follow docs/revit_luachat_commercial_api_setup.md first, then rerun this script."
  echo "Expected config: $CONFIG_FILE"
  exit 2
fi

exec cloudflared tunnel --config "$CONFIG_FILE" run "$TUNNEL_NAME" \
  >> "$LOG_DIR/cloudflared-revit-api.log" 2>&1
