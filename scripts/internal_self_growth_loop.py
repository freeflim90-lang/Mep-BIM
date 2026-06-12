#!/usr/bin/env python3
"""Generate an internal self-growth pulse for LUA BIM LABS.

This loop turns collected knowledge into internal growth candidates:
- productization candidates
- automation/Add-in candidates
- education/curriculum candidates
- quality rule candidates
- knowledge gaps

It is deterministic and conservative. It does not activate development queues;
it creates a reviewable growth pulse and updates the Obsidian map.
"""

from __future__ import annotations

import datetime as dt
import json
import re
import subprocess
import sys
from collections import Counter, defaultdict
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))
from backend.core.paths import AGENT_KB_DIR, KNOWLEDGE_UPDATES_DIR  # noqa: E402
from backend.knowledge_store import knowledge_file_path  # noqa: E402

GROWTH_DIR = PROJECT_ROOT / "docs" / "internal_growth"
KB_FILE = Path(knowledge_file_path("내부성장루프"))
BACKLOG_FILE = PROJECT_ROOT / "docs" / "internal_growth" / "AX_INTERNAL_GROWTH_BACKLOG.md"

_KB_REL = AGENT_KB_DIR.relative_to(PROJECT_ROOT).as_posix()
_UPDATES_REL = KNOWLEDGE_UPDATES_DIR.relative_to(PROJECT_ROOT).as_posix()
SOURCE_GLOBS = [
    f"{_UPDATES_REL}/daily/*_DAILY_KNOWLEDGE_UPDATE.md",
    f"{_UPDATES_REL}/weekly/*_AX_STRATEGY_REVIEW.md",
    "docs/industry_intelligence/hourly/**/*.md",
    "docs/industry_intelligence/daily/*_CONSTRUCTION_DESIGN_BIM_DAILY_BRIEFING.md",
    f"{_KB_REL}/**/AX_*.md",
    f"{_KB_REL}/**/최고전략CSO.md",
    f"{_KB_REL}/**/아이디어발굴.md",
    f"{_KB_REL}/**/지식업데이트.md",
]

BUCKETS = {
    "제품화": ["product", "store", "상품", "제품", "mvp", "패키지", "model quality auditor"],
    "자동화": ["automation", "addin", "add-in", "revit", "navisworks", "api", "자동화", "스크립트"],
    "교육": ["training", "curriculum", "교육", "온보딩", "커리큘럼", "실습"],
    "품질룰": ["quality", "audit", "clash", "ids", "ifc", "품질", "검토", "간섭", "납품"],
    "전략": ["ax", "strategy", "시장", "정책", "지원사업", "스마트건설", "디지털트윈"],
    "지식공백": ["gap", "보강", "needs-review", "공백", "확인 필요", "미검증"],
}


def recent_paths(days: int = 7) -> list[Path]:
    cutoff = dt.datetime.now() - dt.timedelta(days=days)
    paths: list[Path] = []
    for pattern in SOURCE_GLOBS:
        for path in PROJECT_ROOT.glob(pattern):
            if not path.is_file():
                continue
            try:
                modified = dt.datetime.fromtimestamp(path.stat().st_mtime)
            except OSError:
                continue
            if modified >= cutoff:
                paths.append(path)
    return sorted(set(paths))


def interesting_lines(path: Path) -> list[str]:
    text = path.read_text(encoding="utf-8", errors="ignore")
    lines = []
    for raw in text.splitlines():
        line = raw.strip()
        if len(line) < 12:
            continue
        lowered = line.lower()
        if any(keyword in lowered for words in BUCKETS.values() for keyword in words):
            line = re.sub(r"\s+", " ", line)
            lines.append(line[:260])
    return lines[:80]


def classify(line: str) -> list[str]:
    lowered = line.lower()
    buckets = []
    for bucket, keywords in BUCKETS.items():
        if any(keyword.lower() in lowered for keyword in keywords):
            buckets.append(bucket)
    return buckets or ["전략"]


def load_queue_status() -> dict:
    queue_file = PROJECT_ROOT / "config" / "qwen_product_draft_queue.json"
    if not queue_file.exists():
        return {"product": "", "total": 0, "completed": 0, "remaining": []}
    queue = json.loads(queue_file.read_text(encoding="utf-8"))
    task_ids = [task.get("id") for task in queue.get("tasks", []) if task.get("id")]
    state_file = (
        PROJECT_ROOT
        / "obsidian_vaults"
        / "model_quality_auditor"
        / "06_Qwen_Drafts"
        / f"{queue_file.stem}_state.json"
    )
    state = json.loads(state_file.read_text(encoding="utf-8")) if state_file.exists() else {"completed": []}
    completed = set(state.get("completed", []))
    remaining = [task_id for task_id in task_ids if task_id not in completed]
    return {
        "product": queue.get("product", ""),
        "selected_item": queue.get("selected_item", ""),
        "total": len(task_ids),
        "completed": len(task_ids) - len(remaining),
        "remaining": remaining,
    }


def build_pulse() -> tuple[str, dict]:
    now = dt.datetime.now()
    paths = recent_paths()
    bucket_lines: dict[str, list[tuple[str, Path]]] = defaultdict(list)
    counter: Counter[str] = Counter()
    for path in paths:
        for line in interesting_lines(path):
            for bucket in classify(line):
                bucket_lines[bucket].append((line, path))
                counter[bucket] += 1

    queue_status = load_queue_status()
    summary_rows = "\n".join(
        f"| {bucket} | {counter.get(bucket, 0)} |"
        for bucket in BUCKETS
    )
    sections = []
    for bucket in BUCKETS:
        items = bucket_lines.get(bucket, [])[:8]
        body = "\n".join(
            f"- {line} (`{path.relative_to(PROJECT_ROOT).as_posix()}`)"
            for line, path in items
        ) or "- 신규 후보 없음"
        sections.append(f"## {bucket} 후보\n\n{body}")

    content = f"""---
type: internal-self-growth-pulse
date: {now.strftime('%Y-%m-%d')}
status: generated
tags:
  - ax
  - internal-growth
  - self-improvement
  - bim
---

# {now.strftime('%Y-%m-%d %H:%M')} LUA BIM LABS 내부 성장 펄스

이 문서는 LUA BIM LABS가 AX 기업으로 내부적으로 자동 성장하기 위한 일일 운영 펄스다.
수집된 지식을 제품화, 자동화, 교육, 품질룰, 전략, 지식공백 후보로 분류한다.

## 현재 개발 큐

- 제품: {queue_status.get('product') or '미설정'}
- 선택 항목: {queue_status.get('selected_item') or '미설정'}
- 완료: {queue_status.get('completed', 0)} / {queue_status.get('total', 0)}
- 남은 항목: {', '.join(queue_status.get('remaining', [])) or '없음'}

## 분류 요약

| 성장 축 | 후보 신호 |
|---|---:|
{summary_rows}

{chr(10).join(sections)}

## 오늘의 운영 판단

- 제품화 후보는 `아이디어발굴`, `제품패키징`, `CSO` 지식으로 연결한다.
- 자동화 후보는 Revit/Navisworks Add-in 백로그 또는 Qwen 개발 큐 후보로 전환한다.
- 교육 후보는 연차별 커리큘럼과 실무 실습 자료로 전환한다.
- 품질룰 후보는 Model Quality Auditor 룰, 체크리스트, 리포트 템플릿으로 승격한다.
- 지식공백은 공식 출처 확인 전 고객 답변에 단정하지 않는다.

## 연결

- [[LUA BIM LABS AX BIM 선도기업 성장 비전]]
- [[AX 전환을 위한 건설 BIM AI 지식 축적 전략]]
- [[AX_시간별_신호모니터링]]
- [[AX_전략승격리뷰]]
- [[Global Knowledge Map]]
"""
    metadata = {
        "timestamp": now.isoformat(timespec="seconds"),
        "paths": len(paths),
        "counts": dict(counter),
        "queue_status": queue_status,
    }
    return content, metadata


def update_backlog(pulse_path: Path, metadata: dict) -> None:
    if not BACKLOG_FILE.exists():
        BACKLOG_FILE.parent.mkdir(parents=True, exist_ok=True)
        BACKLOG_FILE.write_text(
            "# AX Internal Growth Backlog\n\n"
            "LUA BIM LABS가 AX 기업으로 내부 성장하기 위해 매일 생성되는 성장 펄스의 누적 인덱스다.\n\n",
            encoding="utf-8",
        )
    counts = ", ".join(f"{k}:{v}" for k, v in sorted(metadata.get("counts", {}).items())) or "none"
    with BACKLOG_FILE.open("a", encoding="utf-8") as handle:
        handle.write(
            f"- {metadata['timestamp']} | `{pulse_path.relative_to(PROJECT_ROOT).as_posix()}` | {counts}\n"
        )


def update_kb(pulse_path: Path, metadata: dict) -> None:
    if not KB_FILE.exists():
        KB_FILE.parent.mkdir(parents=True, exist_ok=True)
        KB_FILE.write_text(
            "# 내부성장루프 지식 베이스\n\n"
            "LUA BIM LABS가 AX 기업으로 자동 성장하기 위한 내부 운영 루프를 기록한다.\n",
            encoding="utf-8",
        )
    counts = ", ".join(f"{k} {v}" for k, v in sorted(metadata.get("counts", {}).items())) or "신규 후보 없음"
    with KB_FILE.open("a", encoding="utf-8") as handle:
        handle.write(
            f"\n\n## {metadata['timestamp']} 내부 성장 펄스\n"
            f"- Source: `{pulse_path.relative_to(PROJECT_ROOT).as_posix()}`\n"
            "- Tags: ax,internal-growth,self-improvement,bim\n\n"
            f"분류 요약: {counts}\n\n"
            "운영 판단: 후보는 제품화, 자동화, 교육, 품질룰, 전략, 지식공백 축으로 검토한다.\n"
        )


def rebuild_obsidian() -> None:
    script = PROJECT_ROOT / "scripts" / "build_global_obsidian_map.py"
    subprocess.run([sys.executable, str(script)], cwd=PROJECT_ROOT, check=False, timeout=120)


def main() -> int:
    content, metadata = build_pulse()
    date_dir = GROWTH_DIR / dt.date.today().isoformat()
    date_dir.mkdir(parents=True, exist_ok=True)
    pulse_path = date_dir / f"{dt.datetime.now().strftime('%H%M')}_INTERNAL_SELF_GROWTH_PULSE.md"
    pulse_path.write_text(content, encoding="utf-8")
    update_backlog(pulse_path, metadata)
    update_kb(pulse_path, metadata)
    rebuild_obsidian()
    print(f"internal_growth_pulse={pulse_path}")
    print(json.dumps(metadata, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
