#!/usr/bin/env python3
"""Create a weekly AX strategy review from hourly and daily signals."""

from __future__ import annotations

import datetime as dt
import re
import subprocess
import sys
from collections import Counter
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
HOURLY_DIR = PROJECT_ROOT / "docs" / "industry_intelligence" / "hourly"
DAILY_DIR = PROJECT_ROOT / "docs" / "industry_intelligence" / "daily"
WEEKLY_DIR = PROJECT_ROOT / "docs" / "knowledge_updates" / "weekly"
KB_FILE = PROJECT_ROOT / "data" / "knowledge_base" / "AX_전략승격리뷰.md"


def week_start(today: dt.date) -> dt.date:
    return today - dt.timedelta(days=today.weekday())


def iter_recent_markdown(start: dt.date, end: dt.date) -> list[Path]:
    paths: list[Path] = []
    current = start
    while current <= end:
        day = current.isoformat()
        paths.extend((HOURLY_DIR / day).glob("*_AX_SIGNAL_MONITOR.md"))
        paths.extend(DAILY_DIR.glob(f"{day}_CONSTRUCTION_DESIGN_BIM_DAILY_BRIEFING.md"))
        current += dt.timedelta(days=1)
    return sorted(paths)


def extract_signal_lines(text: str) -> list[str]:
    lines = []
    for raw in text.splitlines():
        line = raw.strip()
        if not line.startswith("|") and not line.startswith("- "):
            continue
        lowered = line.lower()
        if any(keyword in lowered for keyword in ["ax", "ai", "bim", "revit", "ifc", "ids", "스마트건설", "품질", "자동화"]):
            lines.append(line)
    return lines


def classify(line: str) -> str:
    lowered = line.lower()
    if any(k in lowered for k in ["ifc", "ids", "openbim", "표준"]):
        return "OpenBIM/납품검증"
    if any(k in lowered for k in ["quality", "audit", "clash", "품질", "간섭", "검토"]):
        return "Model Quality Auditor"
    if any(k in lowered for k in ["revit", "navisworks", "addin", "api"]):
        return "BIM 자동화/Add-in"
    if any(k in lowered for k in ["스마트건설", "construction", "시공", "현장", "safety", "안전"]):
        return "시공 BIM/스마트건설"
    if any(k in lowered for k in ["교육", "training", "curriculum"]):
        return "교육/확산"
    return "AX 전략 신호"


def table_cell(value: str, limit: int = 220) -> str:
    return re.sub(r"\|", "/", value).strip()[:limit]


def write_review(today: dt.date | None = None) -> Path:
    today = today or dt.date.today()
    start = week_start(today)
    end = today
    sources = iter_recent_markdown(start, end)
    collected: list[tuple[str, str, Path]] = []
    for path in sources:
        text = path.read_text(encoding="utf-8", errors="ignore")
        for line in extract_signal_lines(text):
            collected.append((classify(line), line, path))

    category_counts = Counter(category for category, _, _ in collected)
    top = collected[:40]
    week_id = f"{today.isocalendar().year}-W{today.isocalendar().week:02d}"
    report_path = WEEKLY_DIR / f"{week_id}_AX_STRATEGY_REVIEW.md"
    rows = "\n".join(
        f"| {idx} | {category} | {table_cell(line)} | `{path.relative_to(PROJECT_ROOT).as_posix()}` |"
        for idx, (category, line, path) in enumerate(top, 1)
    ) or "| - | - | 수집 신호 없음 | - |"
    counts = "\n".join(f"- {category}: {count}" for category, count in category_counts.most_common()) or "- 없음"
    content = f"""---
type: weekly-ax-strategy-review
week: {week_id}
date: {today.isoformat()}
status: generated
tags:
  - ax
  - weekly-review
  - strategy
  - bim
---

# {week_id} AX 전략 승격 리뷰

검토 범위: {start.isoformat()} ~ {end.isoformat()}

## 분류 요약

{counts}

## 승격 후보 신호

| No. | 분류 | 신호 | 출처 |
|---:|---|---|---|
{rows}

## 승격 판단 기준

- `Model Quality Auditor`: 품질검토 룰, 리포트 템플릿, Store 제품 기능 후보로 검토한다.
- `BIM 자동화/Add-in`: Revit/Navisworks 자동화 백로그로 전환한다.
- `OpenBIM/납품검증`: IFC/IDS 납품 체크리스트와 데이터 검증 규칙 후보로 전환한다.
- `시공 BIM/스마트건설`: 안전, 공정, 품질, 물량, 준공 데이터 자동화 축으로 분해한다.
- `교육/확산`: 연차별 커리큘럼과 팀원 실습 자료로 전환한다.

## 연결

- [[LUA BIM LABS AX BIM 선도기업 성장 비전]]
- [[AX 전환을 위한 건설 BIM AI 지식 축적 전략]]
- [[AX_시간별_신호모니터링]]
- [[Global Knowledge Map]]
"""
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(content, encoding="utf-8")
    update_kb(today, report_path, category_counts)
    rebuild_obsidian()
    return report_path


def update_kb(today: dt.date, report_path: Path, counts: Counter) -> None:
    if not KB_FILE.exists():
        KB_FILE.parent.mkdir(parents=True, exist_ok=True)
        KB_FILE.write_text(
            "# AX 전략승격리뷰 지식 베이스\n\n"
            "시간별 신호와 일일 브리핑을 주간 단위로 묶어 AX 전략, 제품, 교육, 자동화 후보로 승격한다.\n",
            encoding="utf-8",
        )
    rel = report_path.relative_to(PROJECT_ROOT).as_posix()
    count_line = ", ".join(f"{key} {value}" for key, value in counts.most_common()) or "신호 없음"
    with KB_FILE.open("a", encoding="utf-8") as handle:
        handle.write(
            f"\n\n## {today.isoformat()} 주간 AX 전략 리뷰\n"
            f"- Source: `{rel}`\n"
            "- Tags: ax,weekly-review,strategy,bim\n\n"
            f"분류 요약: {count_line}\n\n"
            "운영 판단: 상위 반복 신호는 CSO, 제품패키징, Model Quality Auditor, 교육컨설팅 지식으로 연결한다.\n"
        )


def rebuild_obsidian() -> None:
    script = PROJECT_ROOT / "scripts" / "build_global_obsidian_map.py"
    subprocess.run([sys.executable, str(script)], cwd=PROJECT_ROOT, check=False, timeout=120)


def main() -> int:
    report = write_review()
    print(f"weekly_ax_strategy_review={report}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
