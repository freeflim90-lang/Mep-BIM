#!/bin/zsh
set -euo pipefail

PROJECT_DIR="/Users/choejeong-yeon/LUA BIM LABS"
WEBSITE_DIR="$PROJECT_DIR/website"

source "$PROJECT_DIR/.env"

cd "$WEBSITE_DIR"
CLOUDFLARE_API_TOKEN="$CLOUDFLARE_API_TOKEN" npx wrangler pages deploy . \
  --project-name luabimlabs \
  --commit-dirty=true \
  >> "$PROJECT_DIR/logs/deploy_website.log" 2>&1

echo "✅ $(date '+%Y-%m-%d %H:%M:%S') 배포 완료" >> "$PROJECT_DIR/logs/deploy_website.log"
echo "배포 완료: https://luabimlabs.com"
