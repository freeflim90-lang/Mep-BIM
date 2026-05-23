#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from backend.qwen_product_drafts import run_next_sync


def main() -> int:
    parser = argparse.ArgumentParser(description="Run Qwen product draft queue for Model Quality Auditor.")
    parser.add_argument("--max-tasks", type=int, default=1, help="Number of queued draft tasks to attempt.")
    parser.add_argument("--no-telegram", action="store_true", help="Do not send Telegram progress report.")
    parser.add_argument("--advance-on-blocked", action="store_true", help="Mark blocked tasks complete and continue.")
    args = parser.parse_args()

    result = run_next_sync(
        max_tasks=args.max_tasks,
        send_reports=not args.no_telegram,
        advance_on_blocked=args.advance_on_blocked,
    )
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
