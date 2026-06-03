#!/usr/bin/env zsh
set -euo pipefail

cd "/Users/choejeong-yeon/LUA BIM LABS"

if [[ -x ".dev-venv/bin/python" ]]; then
  PY=".dev-venv/bin/python"
else
  PY="python3"
fi

"$PY" scripts/seed_qwen_addin_idea_queue.py
"$PY" scripts/qwen_product_draft_runner.py --max-tasks 5 --no-telegram
