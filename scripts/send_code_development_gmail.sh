#!/bin/zsh
set -euo pipefail

PROJECT_DIR="/Users/choejeong-yeon/LUA BIM LABS"
PYTHON="$PROJECT_DIR/.dev-venv/bin/python"

cd "$PROJECT_DIR"
"$PYTHON" scripts/send_code_development_gmail.py "$@"
