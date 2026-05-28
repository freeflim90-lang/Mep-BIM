#!/usr/bin/env python3
"""Collect lightweight hourly AX signals and mirror them into Obsidian.

Hourly collection is intentionally small:
- gather RSS/news signals from the existing industry briefing sources
- record only new high-value items
- update a compact AX signal knowledge-base note
- rebuild the global Obsidian map so the new note is searchable

Daily curation remains the place for deeper synthesis.
"""

from __future__ import annotations

import datetime as dt
import json
import subprocess
import sys
from pathlib import Path

import daily_industry_briefing as briefing


PROJECT_ROOT = Path(__file__).resolve().parents[1]
HOURLY_DIR = PROJECT_ROOT / "docs" / "industry_intelligence" / "hourly"
STATE_FILE = PROJECT_ROOT / "logs" / "hourly_ax_signal_monitor_state.json"
KB_FILE = PROJECT_ROOT / "data" / "knowledge_base" / "AX_시간별_신호모니터링.md"
RUNNING_MARKER = PROJECT_ROOT / "logs" / ".hourly_ax_signal_monitor_running"


AX_TAGS = {
    "AX/AI Transformation": ["ax", "ai transformation", "ai 전환", "ai 대전환", "ai+X", "AI+X"],
    "Smart Construction": ["smart construction", "스마트건설", "digital construction", "디지털 건설"],
    "BIM Automation": ["bim", "revit", "navisworks", "ifc", "ids", "openbim", "자동화"],
    "Quality/Product": ["quality", "audit", "clash", "품질", "간섭", "검토", "납품"],
}


def load_sources() -> list[dict]:
    data = json.loads(briefing.SOURCE_CONFIG.read_text(encoding="utf-8"))
    return data.get("sources", [])


def load_state() -> dict:
    if not STATE_FILE.exists():
        return {"seen": []}
    try:
        return json.loads(STATE_FILE.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {"seen": []}


def save_state(state: dict) -> None:
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    seen = list(dict.fromkeys(state.get("seen", [])))[-1000:]
    state["seen"] = seen
    state["updated_at"] = dt.datetime.now().isoformat(timespec="seconds")
    STATE_FILE.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")


def item_key(item: briefing.FeedItem) -> str:
    return f"{item.source}|{item.title}|{item.url}"[:500]


def ax_tags_for(item: briefing.FeedItem) -> list[str]:
    haystack = f"{item.title} {item.summary} {' '.join(item.tags)}".lower()
    tags = []
    for tag, keywords in AX_TAGS.items():
        if any(keyword.lower() in haystack for keyword in keywords):
            tags.append(tag)
    return tags or ["Watch"]


def collect_items() -> tuple[list[briefing.FeedItem], list[str]]:
    items: list[briefing.FeedItem] = []
    failures: list[str] = []
    for source in load_sources():
        try:
            items.extend(briefing.parse_feed(source))
        except Exception as exc:  # noqa: BLE001 - signal monitor must be resilient
            failures.append(f"{source.get('name', 'unknown')}: {exc}")
    selected = briefing.balanced_selection(items, total=8, per_source=2)
    selected = [item for item in selected if item.score >= 6]
    return selected, failures


def write_hourly_note(now: dt.datetime, new_items: list[briefing.FeedItem], failures: list[str]) -> Path:
    day_dir = HOURLY_DIR / now.strftime("%Y-%m-%d")
    note_path = day_dir / f"{now.strftime('%H%M')}_AX_SIGNAL_MONITOR.md"
    rows = "\n".join(
        "| {idx} | {category} | {title} | {score} | {tags} | {source} | [link]({url}) |".format(
            idx=idx,
            category=item.category,
            title=item.title.replace("|", "/"),
            score=item.score,
            tags=", ".join(ax_tags_for(item)),
            source=item.source.replace("|", "/"),
            url=item.url,
        )
        for idx, item in enumerate(new_items, 1)
    ) or "| - | - | 신규 고신호 없음 | - | - | - | - |"
    failure_text = "\n".join(f"- {failure}" for failure in failures) or "- 없음"
    content = f"""---
type: hourly-ax-signal
date: {now.strftime('%Y-%m-%d')}
hour: {now.strftime('%H:%M')}
status: generated
tags:
  - ax
  - hourly-signal
  - construction
  - bim
  - ai
---

# {now.strftime('%Y-%m-%d %H:%M')} AX 시간별 신호 모니터

이 노트는 매시간 수집되는 가벼운 신호 기록이다. 깊은 판단은 일일 큐레이션과 주간 AX 전략 리뷰에서 수행한다.

## 신규 고신호

| No. | 분류 | 제목 | 점수 | AX 태그 | 출처 | 링크 |
|---:|---|---|---:|---|---|---|
{rows}

## 처리 기준

- `AX/AI Transformation`: 회사 비전, 전략기획, 제품패키징 후보로 검토한다.
- `Smart Construction`: 시공 BIM, 안전/공정/품질 자동화 사례로 분해한다.
- `BIM Automation`: Revit/Navisworks/IFC/IDS 자동화 후보로 검토한다.
- `Quality/Product`: Model Quality Auditor 또는 고객 서비스 패키지 후보로 검토한다.
- 신규 고신호가 없으면 노트만 남기고 KB에는 과도하게 누적하지 않는다.

## 수집 실패

{failure_text}

## 연결

- [[LUA BIM LABS AX BIM 선도기업 성장 비전]]
- [[AX 전환을 위한 건설 BIM AI 지식 축적 전략]]
- [[산업동향_데일리브리핑]]
- [[Global Knowledge Map]]
"""
    note_path.parent.mkdir(parents=True, exist_ok=True)
    note_path.write_text(content, encoding="utf-8")
    return note_path


def update_kb(now: dt.datetime, note_path: Path, new_items: list[briefing.FeedItem]) -> None:
    if not KB_FILE.exists():
        KB_FILE.parent.mkdir(parents=True, exist_ok=True)
        KB_FILE.write_text(
            "# AX 시간별 신호모니터링 지식 베이스\n\n"
            "AX 기업 성장을 위해 건설, 설계, 시공, BIM, AI 관련 시간별 신호를 가볍게 기록한다.\n"
            "깊은 판단은 일일 큐레이션과 주간 AX 전략 리뷰에서 수행한다.\n",
            encoding="utf-8",
        )
    if not new_items:
        return
    rel = note_path.relative_to(PROJECT_ROOT).as_posix()
    top_lines = "\n".join(
        f"- {item.title} ({', '.join(ax_tags_for(item))})"
        for item in new_items[:5]
    )
    with KB_FILE.open("a", encoding="utf-8") as handle:
        handle.write(
            f"\n\n## {now.strftime('%Y-%m-%d %H:%M')} AX 시간별 고신호\n"
            f"- Source: `{rel}`\n"
            "- Tags: ax,hourly-signal,construction,bim,ai\n\n"
            f"{top_lines}\n\n"
            "운영 판단: 반복 노출되거나 제품/교육/품질검토와 연결되는 항목은 일일 큐레이션에서 승격한다.\n"
        )


def rebuild_obsidian() -> None:
    script = PROJECT_ROOT / "scripts" / "build_global_obsidian_map.py"
    subprocess.run([sys.executable, str(script)], cwd=PROJECT_ROOT, check=False, timeout=120)


def main() -> int:
    if RUNNING_MARKER.exists():
        print("hourly AX signal monitor already running; skip")
        return 0
    RUNNING_MARKER.parent.mkdir(parents=True, exist_ok=True)
    RUNNING_MARKER.write_text(dt.datetime.now().isoformat(timespec="seconds"), encoding="utf-8")
    try:
        now = dt.datetime.now()
        state = load_state()
        seen = set(state.get("seen", []))
        selected, failures = collect_items()
        new_items = []
        for item in selected:
            key = item_key(item)
            if key in seen:
                continue
            new_items.append(item)
            seen.add(key)
        state["seen"] = list(seen)
        note_path = write_hourly_note(now, new_items, failures)
        update_kb(now, note_path, new_items)
        save_state(state)
        rebuild_obsidian()
        print(f"hourly_note={note_path}")
        print(f"new_items={len(new_items)} failures={len(failures)}")
        return 0
    finally:
        RUNNING_MARKER.unlink(missing_ok=True)


if __name__ == "__main__":
    raise SystemExit(main())
