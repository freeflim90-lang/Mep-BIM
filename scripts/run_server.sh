#!/bin/zsh
set -euo pipefail

PROJECT_DIR="/Users/choejeong-yeon/LUA BIM LABS"
cd "$PROJECT_DIR"

/usr/bin/python3 -m uvicorn backend.server_total:app --host 0.0.0.0 --port 8000
