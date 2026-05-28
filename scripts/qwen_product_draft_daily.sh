#!/usr/bin/env zsh
set -euo pipefail

cd "/Users/choejeong-yeon/LUA BIM LABS"

if [[ -x ".dev-venv/bin/python" ]]; then
  PY=".dev-venv/bin/python"
else
  PY="python3"
fi

"$PY" scripts/qwen_product_draft_runner.py --max-tasks 1 --no-telegram
