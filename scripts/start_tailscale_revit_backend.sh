#!/bin/zsh
set -euo pipefail

PROJECT_DIR="/Users/choejeong-yeon/LUA BIM LABS"
TAILSCALE="/opt/homebrew/bin/tailscale"
TAILSCALED="/opt/homebrew/opt/tailscale/bin/tailscaled"
SOCKET="$HOME/.local/run/tailscale/tailscaled.sock"
STATE_DIR="$HOME/.local/share/tailscale"
LOG_DIR="$PROJECT_DIR/logs"
TS_LOG="$LOG_DIR/tailscaled-userspace.log"
LAUNCH_AGENT="$HOME/Library/LaunchAgents/com.luabimlabs.tailscale-userspace.plist"
PLIST="$PROJECT_DIR/scripts/com.luabimlabs.tailscale-userspace.plist"

mkdir -p "$(dirname "$SOCKET")" "$STATE_DIR" "$LOG_DIR"

if ! lsof -nP -iTCP:8000 -sTCP:LISTEN >/dev/null 2>&1; then
  echo "LUA BIM LABS backend is not listening on port 8000."
  echo "Start it first with: scripts/start_server.sh"
  exit 1
fi

if ! "$TAILSCALE" --socket="$SOCKET" status >/dev/null 2>&1; then
  mkdir -p "$HOME/Library/LaunchAgents"
  cp "$PLIST" "$LAUNCH_AGENT"
  launchctl bootout "gui/$(id -u)" "$LAUNCH_AGENT" >/dev/null 2>&1 || true
  launchctl bootstrap "gui/$(id -u)" "$LAUNCH_AGENT"
  sleep 3
fi

if ! "$TAILSCALE" --socket="$SOCKET" status >/dev/null 2>&1; then
  echo "Tailscale needs login. Run:"
  echo "$TAILSCALE --socket=\"$SOCKET\" up --accept-routes=false --accept-dns=false"
  exit 2
fi

"$TAILSCALE" --socket="$SOCKET" serve --bg --http=8000 8000
"$TAILSCALE" --socket="$SOCKET" serve status
