#!/usr/bin/env python3
"""Promote daily news trend signals into deeper Obsidian/KB knowledge.

This script is intentionally deterministic. It reads the daily industry
briefing, groups signals by strategic themes, writes an Obsidian NAS note, and
updates the key strategy KB files with managed sections.
"""

from __future__ import annotations

import sys
import argparse
import datetime as dt
import re
from dataclasses import dataclass
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))
from backend.core.paths import AGENT_KB_DIR  # noqa: E402

DAILY_DIR = PROJECT_ROOT / "docs" / "industry_intelligence" / "daily"
NAS_DIR = PROJECT_ROOT / "obsidian_vaults" / "lua_bim_lab_global_map" / "NAS_Knowledge"
KB_DIR = AGENT_KB_DIR
MARKET_KB = KB_DIR / "건설시장_트렌드.md"
AX_KB = KB_DIR / "AX_전략승격리뷰.md"
KNOWLEDGE_UPDATE_KB = KB_DIR / "지식업데이트.md"


@dataclass
class Signal:
    no: int
    category: str
    title: str
    connection: str
    source: str
    url: str


@dataclass
class Theme:
    key: str
    title: str
    keywords: tuple[str, ...]
    interpretation: str
    action: str
    ax_action: str
    confidence: str
    urgency: str
    fit: str


THEMES: list[Theme] = [
    Theme(
        key="openbim",
        title="OpenBIM 검증형 납품",
        keywords=("openbim", "ifc", "ids", "bcf", "buildingsmart", "validation", "certification", "표준"),
        interpretation=(
            "OpenBIM은 파일 교환을 넘어 IDS 요구사항, BCF 이슈 추적, 검증 서비스, "
            "소프트웨어 인증까지 포함하는 납품 계약 언어로 이동한다."
        ),
        action=(
            "[[BIM_납품검수]]와 [[Model Quality Auditor]]에 IFC/IDS/BCF 기반 "
            "납품 반려 리스크 진단 후보를 연결한다."
        ),
        ax_action="Model Quality Auditor 장기 백로그로 승격하고 ifctester/IDS PoC 후보를 만든다.",
        confidence="높음",
        urgency="높음",
        fit="높음",
    ),
    Theme(
        key="automation_training",
        title="Python-Dynamo-Grasshopper-Revit API 자동화 교육",
        keywords=("python", "dynamo", "grasshopper", "tekla", "automation", "api", "자동화", "revit"),
        interpretation=(
            "AEC 자동화는 전문 개발자만의 영역이 아니라 실무자가 반복 업무를 줄이는 "
            "단계형 역량으로 바뀌고 있다."
        ),
        action=(
            "[[교육컨설팅]]에 Python 업무 자동화, Dynamo/Grasshopper 모델 자동화, "
            "Revit API/Add-in 제품화의 3단계 교육 사다리를 연결한다."
        ),
        ax_action="Starter/PM 교육 상품에 장비표, 파라미터, 시트/뷰 자동화 실습을 추가한다.",
        confidence="중상",
        urgency="높음",
        fit="높음",
    ),
    Theme(
        key="aeco_ax",
        title="국내 건설 AX 생태계",
        keywords=("aeco", "ax", "ai", "원가", "견적", "공정", "응용솔루션", "건설 ai"),
        interpretation=(
            "국내 건설 AI는 설계 자동화, 원가·견적·공정관리, 응용솔루션으로 "
            "분화되는 단계에 들어섰다."
        ),
        action=(
            "[[AX_전략승격리뷰]]에서 설계/BIM 자동화, 견적·공정 데이터 자동화, "
            "운영/CS 응용솔루션으로 제품 후보를 분리한다."
        ),
        ax_action="국내 AX 기업/기술 카테고리 표와 파트너십 후보 분류를 생성한다.",
        confidence="중상",
        urgency="중간",
        fit="중상",
    ),
    Theme(
        key="autodesk_cloud",
        title="Autodesk Forma/Revit 클라우드 연결",
        keywords=("autodesk", "forma", "construction cloud", "acc", "cloud", "revit", "store", "add-in", "addin"),
        interpretation=(
            "Autodesk가 Forma 중심 AECO 클라우드와 Revit 연결을 강화할수록 "
            "Add-in은 단독 버튼 기능보다 데이터 내보내기와 협업 흐름이 중요해진다."
        ),
        action=(
            "[[Revit_Addin]] 로드맵에서 CSV/JSON/BCF/IFC/Excel export와 "
            "협업 연동 가능성을 별도 점검한다."
        ),
        ax_action="Add-in 결과물 export 형식과 Autodesk Store 문구를 점검한다.",
        confidence="높음",
        urgency="중간",
        fit="중간",
    ),
    Theme(
        key="robotics",
        title="로봇·현장 자동화",
        keywords=("robot", "robotics", "spot", "boston dynamics", "drone", "lidar", "로봇", "드론", "현장", "시공"),
        interpretation=(
            "현장 로봇은 BIM의 대체재가 아니라 as-built 현장 상태를 BIM/디지털트윈과 "
            "정렬하는 데이터 수집 계층으로 보는 것이 적합하다."
        ),
        action=(
            "[[시공_지침서]], [[Navisworks_Addin]], [[FM_자산관리]]에 현장 검측 "
            "데이터 입력값 후보로 연결한다."
        ),
        ax_action="직접 상품화는 Watch 유지, 스마트시공 교육 사례로만 활용한다.",
        confidence="중간",
        urgency="낮음",
        fit="낮음",
    ),
    Theme(
        key="netzero",
        title="넷제로·친환경 BIM 데이터",
        keywords=("net zero", "net-zero", "sustainability", "carbon", "green", "sips", "탄소", "친환경", "넷제로"),
        interpretation=(
            "친환경 건축은 인증 문구가 아니라 재료·수량·열성능·탄소계수 데이터 관리 "
            "문제로 바뀌고 있다."
        ),
        action=(
            "[[BIM_납품검수]], [[패시브하우스_PHIKO]], [[설비기초]]에 자재 속성, "
            "열성능, 탄소 파라미터 누락 검토 후보를 둔다."
        ),
        ax_action="납품검수 파라미터 후보로 보관하고 반복 노출 시 제안서 고급 옵션으로 승격한다.",
        confidence="중간",
        urgency="중간",
        fit="중상",
    ),
]


def report_path_for(date: str) -> Path:
    return DAILY_DIR / f"{date}_CONSTRUCTION_DESIGN_BIM_DAILY_BRIEFING.md"


def split_markdown_row(line: str) -> list[str]:
    # The source table can contain pipe characters in article titles. The first
    # two and last three columns are stable, so keep the middle as the title.
    parts = [part.strip() for part in line.strip().strip("|").split("|")]
    if len(parts) < 6:
        return []
    no = parts[0]
    category = parts[1]
    title = " | ".join(parts[2 : len(parts) - 3])
    connection = parts[-3]
    source = parts[-2]
    link = parts[-1]
    return [no, category, title, connection, source, link]


def parse_signals(report: Path) -> list[Signal]:
    signals: list[Signal] = []
    row_re = re.compile(r"^\|\s*\d+\s*\|")
    link_re = re.compile(r"\[link\]\((.*?)\)")
    for line in report.read_text(encoding="utf-8", errors="ignore").splitlines():
        if not row_re.match(line):
            continue
        cols = split_markdown_row(line)
        if not cols:
            continue
        match = link_re.search(cols[5])
        signals.append(
            Signal(
                no=int(cols[0]),
                category=cols[1],
                title=cols[2],
                connection=cols[3],
                source=cols[4],
                url=match.group(1) if match else "",
            )
        )
    return signals


def matched_themes(signals: list[Signal]) -> list[tuple[Theme, list[Signal]]]:
    matched: list[tuple[Theme, list[Signal]]] = []
    for theme in THEMES:
        items = []
        for signal in signals:
            haystack = f"{signal.category} {signal.title} {signal.connection} {signal.source}".lower()
            if any(keyword.lower() in haystack for keyword in theme.keywords):
                items.append(signal)
        if items:
            matched.append((theme, items))
    return matched


def wikilink_title_for(date: str) -> str:
    return f"{date} 건설 설계 시공 BIM 데일리 브리핑"


def note_path_for(date: str, count: int) -> Path:
    return NAS_DIR / f"{date} 뉴스 트렌드 {count}항목 지식 업데이트.md"


def signal_table(signals: list[Signal]) -> str:
    rows = [
        "| No. | 분류 | 항목 | 지식 반영 |",
        "|---:|---|---|---|",
    ]
    for signal in signals:
        title = f"[{signal.title}]({signal.url})" if signal.url else signal.title
        rows.append(f"| {signal.no} | {signal.category} | {title} | {signal.connection} |")
    return "\n".join(rows)


def theme_sections(matches: list[tuple[Theme, list[Signal]]]) -> str:
    sections: list[str] = []
    for idx, (theme, items) in enumerate(matches, 1):
        refs = ", ".join(f"{item.no}번" for item in items[:8])
        sections.append(
            f"""### {idx}. {theme.title}

관련 신호: {refs}

해석: {theme.interpretation}

LUA BIM LABS 적용:
- {theme.action}
- AX/제품화 판단: {theme.ax_action}
"""
        )
    return "\n".join(sections)


def matrix(matches: list[tuple[Theme, list[Signal]]]) -> str:
    rows = ["| 트렌드 묶음 | 신뢰도 | 긴급도 | 내부 적합성 | 다음 행동 |", "|---|---:|---:|---:|---|"]
    for theme, _items in matches:
        rows.append(f"| {theme.title} | {theme.confidence} | {theme.urgency} | {theme.fit} | {theme.ax_action} |")
    return "\n".join(rows)


def source_grade(signals: list[Signal]) -> str:
    official = []
    professional = []
    watch = []
    for signal in signals:
        source = signal.source.lower()
        if any(key in source for key in ("buildingsmart", "autodesk", "boston dynamics")):
            official.append(signal.source)
        elif any(key in source for key in ("bim corner", "bim+", "zdnet", "construction")):
            professional.append(signal.source)
        else:
            watch.append(signal.source)
    def uniq(values: list[str]) -> str:
        return ", ".join(sorted(set(values))) or "-"
    return f"""- 1등급 공식 출처: {uniq(official)}
- 2등급 전문/산업 출처: {uniq(professional)}
- 3등급 참고 출처: {uniq(watch)}. 반복 노출 전까지 전략 판단의 단독 근거로 쓰지 않는다."""


def build_note(date: str, report: Path, signals: list[Signal], matches: list[tuple[Theme, list[Signal]]]) -> str:
    count = len(signals)
    now = dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    top_summary = "\n".join(
        f"{idx}. {theme.title}: {theme.interpretation}"
        for idx, (theme, _items) in enumerate(matches[:6], 1)
    ) or "1. 수집 신호가 부족하여 심화 해석은 보류한다."
    return f"""---
type: knowledge-update
date: {date}
status: reflected
generated_by: news_trend_knowledge_deepener.py
source_path: "{report.relative_to(PROJECT_ROOT).as_posix()}"
tags:
  - 뉴스트렌드
  - 산업동향
  - BIM
  - AI
  - OpenBIM
  - 스마트건설
  - Obsidian
---

# {date} 뉴스 트렌드 {count}항목 지식 업데이트

## 수집 기준

- 기준일: {date}
- 생성 시각: {now}
- 원본: [[{wikilink_title_for(date)}]]
- 반영 대상: [[산업동향 데일리 브리핑 지식 베이스]], [[건설시장 트렌드 지식 베이스]], [[AX 전략승격리뷰 지식 베이스]]
- 목적: 단순 뉴스 보관이 아니라 LUA BIM LABS의 교육, Model Quality Auditor, OpenBIM 납품검증, Add-in 로드맵, AX 전략 후보로 전환한다.

## 핵심 트렌드 요약

{top_summary}

## {count}개 수집 항목

{signal_table(signals)}

## 심화 해석

{theme_sections(matches) or "심화 해석 대상이 부족하여 Watch로 보관한다."}

## 심화 승격 매트릭스

{matrix(matches)}

## 출처 검증 메모

{source_grade(signals)}

## 자동 수집·심화 반영 상태

- [x] 일일 브리핑 신호 파싱
- [x] 뉴스 트렌드 심화 노트 생성
- [x] 건설시장 트렌드 KB 반영
- [x] AX 전략승격리뷰 KB 반영
- [x] 전역 Obsidian 맵 재생성 대상 등록

## 관련 링크

- [[산업동향 데일리 브리핑 지식 베이스]]
- [[건설시장 트렌드 지식 베이스]]
- [[AX 시간별 신호모니터링 지식 베이스]]
- [[AX 전략승격리뷰 지식 베이스]]
- [[지식큐레이터 지식 베이스]]
"""


def replace_section(text: str, heading: str, block: str) -> str:
    pattern = rf"\n## {re.escape(heading)}\n.*?(?=\n## |\Z)"
    replacement = f"\n## {heading}\n{block.strip()}\n"
    if re.search(pattern, text, flags=re.S):
        return re.sub(pattern, replacement, text, flags=re.S)
    return text.rstrip() + "\n\n" + replacement


def ensure_file(path: Path, title: str) -> str:
    if not path.exists():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(f"# {title}\n", encoding="utf-8")
    return path.read_text(encoding="utf-8")


def update_market_kb(date: str, note_path: Path, matches: list[tuple[Theme, list[Signal]]]) -> None:
    text = ensure_file(MARKET_KB, "건설시장 트렌드 지식 베이스")
    bullets = "\n\n".join(
        f"{theme.interpretation} {theme.action}"
        for theme, _items in matches[:6]
    ) or "자동 심화 대상 신호가 부족하여 Watch로 보관한다."
    block = f"""- Source: `{note_path.relative_to(PROJECT_ROOT).as_posix()}`
- Tags: news-trend,auto-deepening,openbim,ai-aec,construction-robotics

이번 업데이트는 일일 뉴스 신호를 자동 분류해 시장 트렌드 KB로 승격한 결과다.

{bullets}

- 관련: [[산업동향_데일리브리핑]] · [[AX_전략승격리뷰]] · [[시장선도_전략]] · [[Revit_Addin]] · [[BIM_납품검수]]
"""
    MARKET_KB.write_text(replace_section(text, f"{date} 뉴스 트렌드 자동 심화 반영", block), encoding="utf-8")


def update_ax_kb(date: str, note_path: Path, matches: list[tuple[Theme, list[Signal]]]) -> None:
    text = ensure_file(AX_KB, "AX 전략승격리뷰 지식 베이스")
    lines = [f"- Source: `{note_path.relative_to(PROJECT_ROOT).as_posix()}`", "- Tags: ax,strategy-review,auto-deepening,news-trend", ""]
    for idx, (theme, items) in enumerate(matches[:6], 1):
        lines.append(f"**승격/관찰 후보 {idx}: {theme.title}**")
        lines.append(f"- 관련 신호: {', '.join(str(item.no) + '번' for item in items[:8])}")
        lines.append(f"- 판단: {theme.ax_action}")
        lines.append(f"- 이유: {theme.interpretation}")
        lines.append("")
    AX_KB.write_text(replace_section(text, f"{date} 뉴스 트렌드 자동 전략 승격 판단", "\n".join(lines)), encoding="utf-8")


def update_operating_kb(date: str) -> None:
    text = ensure_file(KNOWLEDGE_UPDATE_KB, "지식업데이트 지식 베이스")
    block = f"""- Source: `scripts/news_trend_knowledge_deepener.py`
- Tags: knowledge-update,news-trend,obsidian,automation

일일 산업 브리핑 생성 후 `news_trend_knowledge_deepener.py`를 실행해 뉴스 신호를 심화 지식으로 자동 승격한다. 처리 순서는 ① `docs/industry_intelligence/daily/`의 당일 브리핑 파싱 ② `NAS_Knowledge/YYYY-MM-DD 뉴스 트렌드 N항목 지식 업데이트.md` 생성 ③ `건설시장_트렌드.md`와 `AX_전략승격리뷰.md`의 자동 심화 섹션 갱신 ④ 전역 Obsidian 맵 재생성이다.

운영 원칙:
- 공식·전문 출처가 확인된 항목은 승격 후보로 둔다.
- Google News RSS만 확인된 단신은 Watch로 보관하고 반복 노출 시 재검증한다.
- OpenBIM, AEC 자동화 교육, 국내 AX 생태계, Autodesk/Revit 흐름, 현장 자동화, 넷제로 BIM 데이터는 기본 심화 분류 축으로 유지한다.
- 관련: [[산업동향_데일리브리핑]] · [[건설시장_트렌드]] · [[AX_전략승격리뷰]] · [[지식큐레이터]]
"""
    KNOWLEDGE_UPDATE_KB.write_text(replace_section(text, f"{date} 뉴스 트렌드 심화 자동 반영 운영 기준", block), encoding="utf-8")


def run(date: str) -> Path:
    report = report_path_for(date)
    if not report.exists():
        raise FileNotFoundError(f"daily briefing not found: {report}")
    signals = parse_signals(report)
    if not signals:
        raise RuntimeError(f"no signals parsed from {report}")
    matches = matched_themes(signals)
    note_path = note_path_for(date, len(signals))
    NAS_DIR.mkdir(parents=True, exist_ok=True)
    note_path.write_text(build_note(date, report, signals, matches), encoding="utf-8")
    update_market_kb(date, note_path, matches)
    update_ax_kb(date, note_path, matches)
    update_operating_kb(date)
    print(f"news_trend_note={note_path}")
    print(f"news_trend_signals={len(signals)} themes={len(matches)}")
    return note_path


def main() -> int:
    parser = argparse.ArgumentParser(description="Deepen daily news trend knowledge")
    parser.add_argument("--date", default=dt.date.today().isoformat())
    args = parser.parse_args()
    run(args.date)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
