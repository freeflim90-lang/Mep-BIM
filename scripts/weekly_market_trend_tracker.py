#!/usr/bin/env python3
"""Weekly construction market trend tracker.

Collects market signals from RSS feeds and appends a dated summary
to the KB files 건설시장_트렌드.md, BIM_시장_규모분석.md, and 시장선도_전략.md.
Designed to run weekly (every Monday) via LaunchAgent or cron.
"""

from __future__ import annotations

import datetime as dt
import html
import json
import re
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path
from dataclasses import dataclass, field

PROJECT_ROOT = Path(__file__).resolve().parents[1]
KB_DIR = PROJECT_ROOT / "data" / "knowledge_base"
LOG_DIR = PROJECT_ROOT / "logs"
LOG_DIR.mkdir(exist_ok=True)

MARKET_SOURCES = [
    # 국내 건설 시장
    {"name": "Google News - 건설수주", "category": "korea_market",
     "url": "https://news.google.com/rss/search?q=%EA%B1%B4%EC%84%A4+%EC%88%98%EC%A3%BC+%EC%8B%9C%EC%9E%A5+when:7d&hl=ko&gl=KR&ceid=KR:ko"},
    {"name": "Google News - 스마트건설", "category": "smart_construction",
     "url": "https://news.google.com/rss/search?q=%EC%8A%A4%EB%A7%88%ED%8A%B8%EA%B1%B4%EC%84%A4+BIM+%EB%94%94%EC%A7%80%ED%84%B8%EC%A0%84%ED%99%98+when:7d&hl=ko&gl=KR&ceid=KR:ko"},
    {"name": "Google News - BIM 의무화", "category": "bim_regulation",
     "url": "https://news.google.com/rss/search?q=BIM+%EC%9D%98%EB%AC%B4%ED%99%94+%EA%B5%AD%ED%86%A0%EB%B6%80+when:7d&hl=ko&gl=KR&ceid=KR:ko"},
    # 글로벌 BIM 시장
    {"name": "Google News - BIM Market Growth", "category": "global_market",
     "url": "https://news.google.com/rss/search?q=BIM+market+growth+construction+digital+when:7d&hl=en-US&gl=US&ceid=US:en"},
    {"name": "Google News - AEC AI Trend", "category": "ai_aec",
     "url": "https://news.google.com/rss/search?q=AEC+AI+construction+automation+when:7d&hl=en-US&gl=US&ceid=US:en"},
    {"name": "Google News - Digital Twin Construction", "category": "digital_twin",
     "url": "https://news.google.com/rss/search?q=digital+twin+construction+BIM+when:7d&hl=en-US&gl=US&ceid=US:en"},
    {"name": "Google News - Autodesk Earnings", "category": "autodesk",
     "url": "https://news.google.com/rss/search?q=Autodesk+earnings+revenue+AEC+when:30d&hl=en-US&gl=US&ceid=US:en"},
    {"name": "buildingSMART News", "category": "openbim",
     "url": "https://www.buildingsmart.org/feed/"},
]

CATEGORY_KO = {
    "korea_market": "국내 건설 시장",
    "smart_construction": "스마트건설·디지털전환",
    "bim_regulation": "BIM 의무화·규제",
    "global_market": "글로벌 BIM 시장",
    "ai_aec": "AI·AEC 자동화",
    "digital_twin": "디지털 트윈",
    "autodesk": "Autodesk 동향",
    "openbim": "OpenBIM·표준",
}

USER_AGENT = "LUA-BIM-LAB-MarketTracker/1.0"
MAX_ITEMS_PER_SOURCE = 3


@dataclass
class SignalItem:
    title: str
    url: str
    pub_date: str
    source: str
    category: str


def fetch_feed(url: str, source_name: str, category: str) -> list[SignalItem]:
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            content = resp.read()
        root = ET.fromstring(content)
    except Exception as e:
        print(f"[WARN] {source_name}: {e}")
        return []

    items = []
    for item in root.iter("item"):
        title_el = item.find("title")
        link_el = item.find("link")
        pub_el = item.find("pubDate")
        if title_el is None:
            continue
        title = html.unescape(title_el.text or "")
        url_val = (link_el.text or "") if link_el is not None else ""
        pub = (pub_el.text or "") if pub_el is not None else ""
        items.append(SignalItem(title, url_val, pub, source_name, category))
        if len(items) >= MAX_ITEMS_PER_SOURCE:
            break
    return items


def collect_all_signals() -> dict[str, list[SignalItem]]:
    by_category: dict[str, list[SignalItem]] = {}
    for src in MARKET_SOURCES:
        items = fetch_feed(src["url"], src["name"], src["category"])
        cat = src["category"]
        if cat not in by_category:
            by_category[cat] = []
        by_category[cat].extend(items)
    return by_category


def build_weekly_section(by_category: dict[str, list[SignalItem]], date_str: str) -> str:
    lines = [
        f"\n## 주간 건설·BIM 시장 신호 ({date_str})",
        "- Source: weekly-market-tracker auto-generated",
        f"- Tags: market-trend,weekly,construction,bim,{date_str}",
        "",
    ]

    for cat, items in by_category.items():
        if not items:
            continue
        ko_cat = CATEGORY_KO.get(cat, cat)
        lines.append(f"**{ko_cat}:**")
        for item in items[:MAX_ITEMS_PER_SOURCE]:
            clean_title = re.sub(r"\s+", " ", item.title).strip()
            lines.append(f"- {clean_title}")
        lines.append("")

    # 시장 선도 시사점
    lines.append("**이번 주 시사점:**")
    total = sum(len(v) for v in by_category.values())
    dominant = max(by_category.items(), key=lambda x: len(x[1]), default=(None, []))
    if dominant[0]:
        lines.append(f"- 이번 주 가장 활발한 트렌드 카테고리: {CATEGORY_KO.get(dominant[0], dominant[0])} ({len(dominant[1])}건)")
    lines.append(f"- 수집 총 신호: {total}건 → AX_전략승격리뷰에서 제품화 후보 검토")
    lines.append("")
    return "\n".join(lines)


def append_to_kb(kb_file: Path, section: str) -> None:
    if not kb_file.exists():
        print(f"[SKIP] KB 파일 없음: {kb_file}")
        return
    with open(kb_file, "a", encoding="utf-8") as f:
        f.write(section)
    print(f"[OK] 업데이트: {kb_file.name}")


def main() -> None:
    today = dt.date.today().isoformat()
    week = dt.date.today().strftime("%Y-W%U")
    log_path = LOG_DIR / f"market_tracker_{today}.log"

    print(f"[{today}] 주간 건설시장 트렌드 수집 시작")
    by_category = collect_all_signals()

    section = build_weekly_section(by_category, today)

    # 업데이트할 KB 파일 목록
    target_files = [
        KB_DIR / "건설시장_트렌드.md",
        KB_DIR / "산업동향_데일리브리핑.md",
    ]

    for kb_file in target_files:
        append_to_kb(kb_file, section)

    # 로그 저장
    total = sum(len(v) for v in by_category.values())
    log_path.write_text(
        f"date={today} week={week} total_signals={total}\n"
        + "\n".join(f"{k}={len(v)}" for k, v in by_category.items()),
        encoding="utf-8"
    )
    print(f"[{today}] 완료: 총 {total}개 신호 수집, 로그: {log_path.name}")


if __name__ == "__main__":
    main()
