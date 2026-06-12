#!/usr/bin/env python3
"""data/knowledge_base → knowledge/ 트리 이동 (git mv 기반, Phase 2 일회성).

- 최상위 *.md       → knowledge/10_agents/<팀폴더>/  (ORGANIZATION 매핑, 그 외 90_확장에이전트)
- qa/               → knowledge/20_qa/
- 기타 하위 폴더     → knowledge/10_agents/<폴더명>/  (시설유형, conflict_resolution 등)

실행 전 git working tree 가 클린해야 한다. --dry-run 으로 미리보기.
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from backend.core.paths import EXTRA_AGENTS_DIR_NAME, TEAM_DIR_NAMES  # noqa: E402
from backend.knowledge_store import ORGANIZATION  # noqa: E402

OLD_KB = PROJECT_ROOT / "data" / "knowledge_base"
NEW_AGENTS = PROJECT_ROOT / "knowledge" / "10_agents"
NEW_QA = PROJECT_ROOT / "knowledge" / "20_qa"


def safe_name(agent: str) -> str:
    return "".join(ch for ch in agent if ch.isalnum() or ch in ("_", "-"))


def build_stem_to_team() -> dict[str, str]:
    mapping: dict[str, str] = {}
    for team, agents in ORGANIZATION.items():
        for agent in agents:
            mapping[safe_name(agent)] = TEAM_DIR_NAMES[team]
    return mapping


def run(cmd: list[str], dry: bool) -> None:
    print(" ".join(cmd))
    if not dry:
        subprocess.run(cmd, cwd=PROJECT_ROOT, check=True)


def main() -> int:
    dry = "--dry-run" in sys.argv
    stem_to_team = build_stem_to_team()

    moves: list[tuple[Path, Path]] = []

    for md in sorted(OLD_KB.glob("*.md")):
        team_dir = stem_to_team.get(md.stem, EXTRA_AGENTS_DIR_NAME)
        moves.append((md, NEW_AGENTS / team_dir / md.name))

    qa_dir = OLD_KB / "qa"
    if qa_dir.exists():
        for f in sorted(qa_dir.iterdir()):
            if f.is_file():
                moves.append((f, NEW_QA / f.name))

    for sub in sorted(OLD_KB.iterdir()):
        if sub.is_dir() and sub.name != "qa":
            moves.append((sub, NEW_AGENTS / sub.name))

    targets = {dst.parent for _, dst in moves}
    for t in sorted(targets):
        print(f"mkdir -p {t}")
        if not dry:
            t.mkdir(parents=True, exist_ok=True)

    for src, dst in moves:
        run(["git", "mv", str(src), str(dst)], dry)

    print(f"\n총 {len(moves)}건 이동 ({'dry-run' if dry else '실행 완료'})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
