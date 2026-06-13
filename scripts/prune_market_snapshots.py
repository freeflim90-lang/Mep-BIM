#!/usr/bin/env python3
"""products/autodesk_market/ 의 날짜별 마켓 스냅샷 보존 정책.

market_YYYYMMDD_HHMM.json 누적분 중 최신 N개만 남기고 정리한다.
market_latest.json·priority_backlog.json·analysis_prompt_latest.txt 는 항상 보존.
기본은 dry-run(목록만 출력). 실제 삭제는 --apply.

사용:
    python scripts/prune_market_snapshots.py            # 미리보기
    python scripts/prune_market_snapshots.py --apply     # 실제 삭제
    python scripts/prune_market_snapshots.py --keep 5 --apply
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from backend.core.paths import AUTODESK_MARKET_DIR  # noqa: E402

_SNAPSHOT_RE = re.compile(r"^market_\d{8}_\d{4}\.json$")


def prune(keep: int, apply: bool) -> list[Path]:
    snapshots = sorted(
        (p for p in AUTODESK_MARKET_DIR.glob("market_*.json") if _SNAPSHOT_RE.match(p.name)),
        key=lambda p: p.name,
    )
    to_remove = snapshots[:-keep] if keep > 0 else []
    for path in to_remove:
        print(("삭제: " if apply else "삭제 예정: ") + path.name)
        if apply:
            path.unlink()
    print(f"\n보존 {min(keep, len(snapshots))}개 / 전체 {len(snapshots)}개 / "
          f"{'삭제' if apply else '삭제예정'} {len(to_remove)}개  (market_latest.json 등은 항상 보존)")
    return to_remove


def main() -> None:
    ap = argparse.ArgumentParser(description="마켓 스냅샷 보존 정책")
    ap.add_argument("--keep", type=int, default=3, help="보존할 최신 날짜 스냅샷 개수 (기본 3)")
    ap.add_argument("--apply", action="store_true", help="실제 삭제 (기본은 dry-run)")
    args = ap.parse_args()
    prune(args.keep, args.apply)


if __name__ == "__main__":
    main()
