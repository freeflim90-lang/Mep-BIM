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
import os
import re
import urllib.parse
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
    {"name": "Google News - 건설 AI 자동화", "category": "ai_korea",
     "url": "https://news.google.com/rss/search?q=%EA%B1%B4%EC%84%A4+AI+%EC%9E%90%EB%8F%99%ED%99%94+%EB%94%94%EC%A7%80%ED%84%B8%ED%8A%B8%EC%9C%88+when:7d&hl=ko&gl=KR&ceid=KR:ko"},
    {"name": "Google News - 스마트건설 드론 로봇", "category": "contech_korea",
     "url": "https://news.google.com/rss/search?q=%EC%8A%A4%EB%A7%88%ED%8A%B8%EA%B1%B4%EC%84%A4+%EB%93%9C%EB%A1%A0+%EB%A1%9C%EB%B4%87+3D%ED%94%84%EB%A6%B0%ED%8C%85+when:7d&hl=ko&gl=KR&ceid=KR:ko"},
    # 글로벌 BIM·AEC 시장
    {"name": "Google News - BIM Market Growth", "category": "global_market",
     "url": "https://news.google.com/rss/search?q=BIM+market+growth+construction+digital+when:7d&hl=en-US&gl=US&ceid=US:en"},
    {"name": "Google News - AEC AI Trend", "category": "ai_aec",
     "url": "https://news.google.com/rss/search?q=AEC+AI+construction+automation+when:7d&hl=en-US&gl=US&ceid=US:en"},
    {"name": "Google News - Generative AI AEC", "category": "ai_aec",
     "url": "https://news.google.com/rss/search?q=generative+AI+architecture+design+AEC+when:7d&hl=en-US&gl=US&ceid=US:en"},
    {"name": "Google News - Digital Twin Construction", "category": "digital_twin",
     "url": "https://news.google.com/rss/search?q=digital+twin+construction+BIM+when:7d&hl=en-US&gl=US&ceid=US:en"},
    {"name": "Google News - ConTech Startup", "category": "contech_global",
     "url": "https://news.google.com/rss/search?q=construction+technology+contech+startup+innovation+when:7d&hl=en-US&gl=US&ceid=US:en"},
    {"name": "Google News - Construction Robotics Drone", "category": "contech_global",
     "url": "https://news.google.com/rss/search?q=construction+robotics+drone+3D+printing+prefab+when:7d&hl=en-US&gl=US&ceid=US:en"},
    # AEC 플랫폼 경쟁
    {"name": "Google News - Autodesk AEC", "category": "autodesk",
     "url": "https://news.google.com/rss/search?q=Autodesk+Construction+Cloud+BIM+AEC+when:7d&hl=en-US&gl=US&ceid=US:en"},
    {"name": "Google News - Trimble Bentley Procore", "category": "aec_platform",
     "url": "https://news.google.com/rss/search?q=Trimble+OR+Bentley+OR+Procore+AEC+BIM+construction+when:7d&hl=en-US&gl=US&ceid=US:en"},
    # 지역별 BIM 트렌드
    {"name": "Google News - BIM UK Europe", "category": "global_bim_region",
     "url": "https://news.google.com/rss/search?q=BIM+construction+UK+Europe+when:7d&hl=en-US&gl=GB&ceid=GB:en"},
    {"name": "Google News - BIM Asia Pacific", "category": "global_bim_region",
     "url": "https://news.google.com/rss/search?q=BIM+construction+Asia+Singapore+Australia+when:7d&hl=en-US&gl=US&ceid=US:en"},
    # 표준·지속가능성
    {"name": "Google News - IFC OpenBIM Global", "category": "openbim",
     "url": "https://news.google.com/rss/search?q=IFC+openBIM+buildingSMART+standard+when:7d&hl=en-US&gl=US&ceid=US:en"},
    {"name": "buildingSMART News", "category": "openbim",
     "url": "https://www.buildingsmart.org/feed/"},
    {"name": "Google News - Green Building Net Zero", "category": "sustainability",
     "url": "https://news.google.com/rss/search?q=green+building+BIM+net+zero+construction+when:7d&hl=en-US&gl=US&ceid=US:en"},
    # 전문 미디어 RSS
    {"name": "Construction Dive", "category": "global_market",
     "url": "https://www.constructiondive.com/feeds/news/"},
    {"name": "BIM+", "category": "global_bim_region",
     "url": "https://www.bimplus.co.uk/news/rss"},
    {"name": "BIM Corner", "category": "ai_aec",
     "url": "https://bimcorner.com/feed/"},
]

CATEGORY_KO = {
    "korea_market": "국내 건설 시장",
    "smart_construction": "스마트건설·디지털전환",
    "bim_regulation": "BIM 의무화·규제",
    "ai_korea": "국내 건설 AI·자동화",
    "contech_korea": "국내 스마트건설·드론·로봇",
    "global_market": "글로벌 BIM 시장",
    "ai_aec": "AI·AEC 자동화",
    "digital_twin": "디지털 트윈",
    "contech_global": "글로벌 ConTech·현장 자동화",
    "autodesk": "Autodesk 동향",
    "aec_platform": "AEC 플랫폼 경쟁 (Trimble·Bentley·Procore)",
    "global_bim_region": "지역별 BIM 트렌드 (UK·유럽·아시아)",
    "openbim": "OpenBIM·IFC 표준",
    "sustainability": "친환경·넷제로 건축",
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


def _node_text(node: ET.Element, names: list[str]) -> str:
    for name in names:
        found = node.find(name)
        if found is not None and found.text:
            return found.text.strip()
    for child in node:
        local = child.tag.rsplit("}", 1)[-1]
        if local in names and child.text:
            return child.text.strip()
    return ""


def _node_link(node: ET.Element) -> str:
    direct = _node_text(node, ["link"])
    if direct:
        return direct
    for child in node:
        if child.tag.rsplit("}", 1)[-1] == "link":
            href = child.attrib.get("href", "")
            if href:
                return href
    return ""


def fetch_feed(url: str, source_name: str, category: str) -> list[SignalItem]:
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            content = resp.read()
        root = ET.fromstring(content)
    except Exception as e:
        print(f"[WARN] {source_name}: {e}")
        return []

    # RSS <item> 또는 Atom <entry> 모두 처리
    raw_nodes = list(root.iter("item"))
    if not raw_nodes:
        raw_nodes = [n for n in root.iter() if n.tag.rsplit("}", 1)[-1] == "entry"]

    items = []
    for node in raw_nodes:
        title = html.unescape(_node_text(node, ["title"]))
        url_val = _node_link(node)
        pub = _node_text(node, ["pubDate", "published", "updated"])
        if not title:
            continue
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
        f"\n## 주간 건설·BIM·AI 글로벌 시장 신호 ({date_str})",
        "- Source: weekly-market-tracker auto-generated",
        f"- Tags: market-trend,weekly,construction,bim,ai,{date_str}",
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

    lines.append("**이번 주 시사점:**")
    total = sum(len(v) for v in by_category.values())
    dominant = max(by_category.items(), key=lambda x: len(x[1]), default=(None, []))
    if dominant[0]:
        lines.append(f"- 이번 주 가장 활발한 트렌드 카테고리: {CATEGORY_KO.get(dominant[0], dominant[0])} ({len(dominant[1])}건)")
    lines.append(f"- 수집 총 신호: {total}건 → AX_전략승격리뷰에서 제품화 후보 검토")
    lines.append("")
    return "\n".join(lines)


CAT_PRIORITY_WEEKLY = [
    "ai_aec", "ai_korea", "digital_twin", "contech_global", "contech_korea",
    "global_market", "aec_platform", "autodesk",
    "global_bim_region", "openbim", "sustainability",
    "korea_market", "smart_construction", "bim_regulation",
]


def _title_key_weekly(title: str) -> str:
    """중복 감지용 정규화 키 — 앞 6 단어 기준."""
    words = re.sub(r"\W+", " ", title.lower()).split()
    return " ".join(words[:6])


def build_telegram_weekly_message(by_category: dict[str, list[SignalItem]], date_str: str, week: str) -> str:
    """주간: 카테고리 구분 없이 이번 주 중복 제거 top 7 리마인드."""
    total = sum(len(v) for v in by_category.values())
    dominant = max(by_category.items(), key=lambda x: len(x[1]), default=(None, []))

    # 우선순위 순서로 전체 항목 평탄화 후 중복 제거
    flat: list[SignalItem] = []
    seen: set[str] = set()
    for cat in CAT_PRIORITY_WEEKLY:
        for item in by_category.get(cat, []):
            key = _title_key_weekly(item.title)
            if key not in seen:
                flat.append(item)
                seen.add(key)
    # 나머지 카테고리 보충
    for items in by_category.values():
        for item in items:
            key = _title_key_weekly(item.title)
            if key not in seen:
                flat.append(item)
                seen.add(key)

    top7 = flat[:7]

    lines = [
        f"[LUA BIM LABS] {week} 이번 주 건설·BIM·AI 주요 뉴스",
        f"({date_str} 기준 · 총 {total}개 신호 중 7선)",
        "",
    ]
    for idx, item in enumerate(top7, 1):
        title = item.title[:72] + ("…" if len(item.title) > 72 else "")
        lines.append(f"{idx}. {title}")
        if item.url:
            lines.append(f"   → {item.url}")
        lines.append("")

    if dominant[0]:
        lines.append(f"이번 주 핵심 분야: {CATEGORY_KO.get(dominant[0], dominant[0])} ({len(dominant[1])}건)")

    return "\n".join(lines).strip()[:3900]


def load_local_env() -> None:
    env_path = PROJECT_ROOT / ".env"
    if not env_path.exists():
        return
    for raw in env_path.read_text(encoding="utf-8", errors="ignore").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))


def send_telegram(message: str) -> bool:
    token = os.environ.get("TELEGRAM_BOT_TOKEN")
    chat_id = os.environ.get("TELEGRAM_CHAT_ID")
    if not token or not chat_id:
        print("telegram=skipped missing TELEGRAM_BOT_TOKEN or TELEGRAM_CHAT_ID")
        return False
    payload = urllib.parse.urlencode({"chat_id": chat_id, "text": message}).encode("utf-8")
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    req = urllib.request.Request(url, data=payload, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            print(f"telegram=sent status={resp.status}")
        return True
    except Exception as exc:
        print(f"telegram=failed {type(exc).__name__}: {exc}")
        return False


def append_to_kb(kb_file: Path, section: str) -> None:
    if not kb_file.exists():
        print(f"[SKIP] KB 파일 없음: {kb_file}")
        return
    with open(kb_file, "a", encoding="utf-8") as f:
        f.write(section)
    print(f"[OK] 업데이트: {kb_file.name}")


def main() -> None:
    load_local_env()
    today = dt.date.today().isoformat()
    week = dt.date.today().strftime("%Y-W%U")
    log_path = LOG_DIR / f"market_tracker_{today}.log"

    print(f"[{today}] 주간 건설·BIM·AI 트렌드 수집 시작")
    by_category = collect_all_signals()

    section = build_weekly_section(by_category, today)

    target_files = [
        KB_DIR / "건설시장_트렌드.md",
        KB_DIR / "산업동향_데일리브리핑.md",
    ]
    for kb_file in target_files:
        append_to_kb(kb_file, section)

    total = sum(len(v) for v in by_category.values())
    log_path.write_text(
        f"date={today} week={week} total_signals={total}\n"
        + "\n".join(f"{k}={len(v)}" for k, v in by_category.items()),
        encoding="utf-8"
    )
    print(f"[{today}] 완료: 총 {total}개 신호 수집, 로그: {log_path.name}")


if __name__ == "__main__":
    main()
