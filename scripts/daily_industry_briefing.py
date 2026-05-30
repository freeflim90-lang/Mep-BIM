#!/usr/bin/env python3
"""Collect daily construction/design/BIM signals and send a Telegram brief.

The script intentionally uses RSS/Atom feeds and stores a local markdown record.
It does not require paid APIs and it does not fail the daily update if Telegram
or an individual feed is unavailable.
"""

from __future__ import annotations

import argparse
import datetime as dt
import html
import json
import os
import re
import textwrap
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from dataclasses import dataclass
from email.utils import parsedate_to_datetime
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SOURCE_CONFIG = PROJECT_ROOT / "config" / "daily_industry_briefing_sources.json"
REPORT_DIR = PROJECT_ROOT / "docs" / "industry_intelligence" / "daily"
KB_FILE = PROJECT_ROOT / "data" / "knowledge_base" / "산업동향_데일리브리핑.md"
SENT_STATE_FILE = PROJECT_ROOT / "runtime" / "daily_industry_briefing_sent_state.json"
USER_AGENT = "LUA-BIM-LAB-Daily-Briefing/1.0"

FOCUS_KEYWORDS = [
    "bim", "revit", "autodesk", "navisworks", "ifc", "openbim", "ids",
    "construction cloud", "digital construction", "vdc", "mep", "clash",
    "prefab", "modular", "scan", "digital twin",
    "건설", "설계", "시공", "감리", "bim", "스마트건설", "디지털트윈",
    "자동화", "품질", "간섭", "물량", "모듈러", "프리패브",
]

NEGATIVE_KEYWORDS = [
    "stock", "shares", "share price", "ytd decline", "investor", "investment",
    "market cap", "earnings", "pricing guide", "how much do", "vocal.media",
    "law review", "securities", "lawsuit", "dividend", "marketbeat",
    "takes position", "$adsk", "private banking",
    "주가", "투자", "증권", "실적", "배당",
]

STRATEGIC_TAGS = {
    "Model Quality Auditor": ["quality", "audit", "clash", "model", "검토", "품질", "간섭"],
    "MEP BIM 교육": ["mep", "revit", "bim", "교육", "설계", "시공"],
    "Autodesk Store/Add-in": ["autodesk", "revit", "api", "addin", "add-in", "construction cloud"],
    "OpenBIM/표준": ["ifc", "openbim", "ids", "buildingsmart", "표준"],
    "AI/자동화": ["ai", "automation", "자동화", "생산성", "digital"],
}


@dataclass
class FeedItem:
    source: str
    category: str
    title: str
    url: str
    published: str
    summary: str
    score: int
    tags: list[str]


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


def strip_html(text: str) -> str:
    text = re.sub(r"<[^>]+>", " ", text or "")
    text = html.unescape(text)
    return re.sub(r"\s+", " ", text).strip()


def normalize_date(value: str) -> str:
    if not value:
        return ""
    try:
        parsed = parsedate_to_datetime(value)
        if parsed.tzinfo:
            parsed = parsed.astimezone(dt.timezone(dt.timedelta(hours=9)))
        return parsed.strftime("%Y-%m-%d %H:%M")
    except (TypeError, ValueError, IndexError):
        return value[:32]


def fetch_xml(url: str, timeout: int = 12) -> ET.Element:
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(request, timeout=timeout) as response:
        data = response.read()
    return ET.fromstring(data)


def child_text(node: ET.Element, names: list[str]) -> str:
    for name in names:
        found = node.find(name)
        if found is not None and found.text:
            return found.text.strip()
    for child in node:
        local = child.tag.rsplit("}", 1)[-1]
        if local in names and child.text:
            return child.text.strip()
    return ""


def item_link(node: ET.Element) -> str:
    direct = child_text(node, ["link"])
    if direct:
        return direct
    for child in node:
        local = child.tag.rsplit("}", 1)[-1]
        if local == "link":
            href = child.attrib.get("href")
            if href:
                return href
    return ""


def parse_feed(source: dict) -> list[FeedItem]:
    root = fetch_xml(source["url"])
    channel = root.find("channel")
    raw_items = channel.findall("item") if channel is not None else root.findall("{http://www.w3.org/2005/Atom}entry")
    if not raw_items and root.tag.rsplit("}", 1)[-1] == "feed":
        raw_items = [child for child in root if child.tag.rsplit("}", 1)[-1] == "entry"]

    items: list[FeedItem] = []
    for node in raw_items[:20]:
        title = strip_html(child_text(node, ["title"]))
        url = item_link(node)
        summary = strip_html(child_text(node, ["description", "summary", "content"]))
        published = normalize_date(child_text(node, ["pubDate", "published", "updated"]))
        if not title:
            continue
        score, tags = score_item(title, summary, source.get("category", "general"))
        items.append(FeedItem(
            source=source.get("name", "unknown"),
            category=source.get("category", "general"),
            title=title,
            url=clean_google_news_url(url),
            published=published,
            summary=summary[:260],
            score=score,
            tags=tags,
        ))
    return items


def clean_google_news_url(url: str) -> str:
    # Google News RSS URLs are acceptable as source links. Keep the original if
    # the canonical URL is not easily exposed.
    return url


def normalize_title_key(title: str) -> str:
    return re.sub(r"\W+", "", title.lower())[:140]


def normalize_url_key(url: str) -> str:
    if not url:
        return ""
    parsed = urllib.parse.urlsplit(url)
    query = urllib.parse.parse_qsl(parsed.query, keep_blank_values=True)
    filtered_query = [
        (key, value)
        for key, value in query
        if not key.lower().startswith("utm_") and key.lower() not in {"fbclid", "gclid"}
    ]
    return urllib.parse.urlunsplit(
        (
            parsed.scheme.lower(),
            parsed.netloc.lower(),
            parsed.path.rstrip("/"),
            urllib.parse.urlencode(filtered_query),
            "",
        )
    )


def item_fingerprint(item: FeedItem) -> dict[str, str]:
    return {
        "url": normalize_url_key(item.url),
        "title": normalize_title_key(item.title),
    }


def seed_sent_state_from_reports() -> dict:
    state = {
        "version": 1,
        "seeded_from_reports": True,
        "seen_urls": [],
        "seen_titles": [],
        "sent_items": [],
    }
    seen_urls: set[str] = set()
    seen_titles: set[str] = set()
    sent_items: list[dict[str, str]] = []
    if not REPORT_DIR.exists():
        return state

    row_re = re.compile(r"^\|\s*\d+\s*\|\s*[^|]*\|\s*(.*?)\s*\|.*?\[link\]\((.*?)\)\s*\|")
    for path in sorted(REPORT_DIR.glob("*_CONSTRUCTION_DESIGN_BIM_DAILY_BRIEFING.md")):
        for line in path.read_text(encoding="utf-8", errors="ignore").splitlines():
            match = row_re.match(line)
            if not match:
                continue
            title = strip_html(match.group(1)).strip()
            url = match.group(2).strip()
            url_key = normalize_url_key(url)
            title_key = normalize_title_key(title)
            if url_key:
                seen_urls.add(url_key)
            if title_key:
                seen_titles.add(title_key)
            sent_items.append({
                "date": path.name[:10],
                "title": title,
                "url": url,
            })
    state["seen_urls"] = sorted(seen_urls)
    state["seen_titles"] = sorted(seen_titles)
    state["sent_items"] = sent_items[-500:]
    return state


def load_sent_state() -> dict:
    if SENT_STATE_FILE.exists():
        return json.loads(SENT_STATE_FILE.read_text(encoding="utf-8"))
    return seed_sent_state_from_reports()


def save_sent_state(state: dict) -> None:
    SENT_STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    state["seen_urls"] = sorted(set(state.get("seen_urls", [])))
    state["seen_titles"] = sorted(set(state.get("seen_titles", [])))
    state["sent_items"] = state.get("sent_items", [])[-500:]
    SENT_STATE_FILE.write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def filter_new_items(items: list[FeedItem], state: dict) -> list[FeedItem]:
    seen_urls = set(state.get("seen_urls", []))
    seen_titles = set(state.get("seen_titles", []))
    fresh: list[FeedItem] = []
    for item in items:
        keys = item_fingerprint(item)
        if keys["url"] and keys["url"] in seen_urls:
            continue
        if keys["title"] and keys["title"] in seen_titles:
            continue
        fresh.append(item)
    return fresh


def mark_items_sent(items: list[FeedItem], state: dict, today: str) -> None:
    seen_urls = set(state.get("seen_urls", []))
    seen_titles = set(state.get("seen_titles", []))
    sent_items = list(state.get("sent_items", []))
    for item in items:
        keys = item_fingerprint(item)
        if keys["url"]:
            seen_urls.add(keys["url"])
        if keys["title"]:
            seen_titles.add(keys["title"])
        sent_items.append({
            "date": today,
            "source": item.source,
            "title": item.title,
            "url": item.url,
        })
    state["seen_urls"] = sorted(seen_urls)
    state["seen_titles"] = sorted(seen_titles)
    state["sent_items"] = sent_items[-500:]


def score_item(title: str, summary: str, category: str) -> tuple[int, list[str]]:
    haystack = f"{title} {summary} {category}".lower()
    score = 0
    matched = []
    for keyword in FOCUS_KEYWORDS:
        if keyword.lower() in haystack:
            score += 2
    for tag, keywords in STRATEGIC_TAGS.items():
        if any(keyword.lower() in haystack for keyword in keywords):
            matched.append(tag)
            score += 3
    if category in {"bim", "construction", "revit", "autodesk", "openbim"}:
        score += 2
    for keyword in NEGATIVE_KEYWORDS:
        if keyword.lower() in haystack:
            score -= 8
    return score, matched or ["산업동향"]


def dedupe(items: list[FeedItem]) -> list[FeedItem]:
    seen: set[str] = set()
    unique = []
    for item in items:
        key = re.sub(r"\W+", "", item.title.lower())[:90]
        if key in seen:
            continue
        seen.add(key)
        unique.append(item)
    return unique


def balanced_selection(items: list[FeedItem], total: int = 12, per_source: int = 3) -> list[FeedItem]:
    sorted_items = sorted(
        [item for item in dedupe(items) if item.score >= 4],
        key=lambda item: (-item.score, item.published, item.title),
    )
    selected: list[FeedItem] = []
    source_counts: dict[str, int] = {}
    for item in sorted_items:
        if source_counts.get(item.source, 0) >= per_source:
            continue
        selected.append(item)
        source_counts[item.source] = source_counts.get(item.source, 0) + 1
        if len(selected) >= total:
            return selected
    for item in sorted_items:
        if item in selected:
            continue
        selected.append(item)
        if len(selected) >= total:
            break
    return selected


def strategic_commentary(items: list[FeedItem]) -> list[str]:
    tag_counts: dict[str, int] = {}
    for item in items:
        for tag in item.tags:
            tag_counts[tag] = tag_counts.get(tag, 0) + 1
    comments = []
    if tag_counts.get("Model Quality Auditor"):
        comments.append("품질검토, 간섭, 모델 데이터 관련 신호는 Model Quality Auditor 진단 룰 후보로 검토한다.")
    if tag_counts.get("MEP BIM 교육"):
        comments.append("MEP BIM/Revit 실무 흐름은 연차별 교육 커리큘럼의 사례 또는 실습 주제로 전환한다.")
    if tag_counts.get("Autodesk Store/Add-in"):
        comments.append("Autodesk/Revit/Add-in 관련 변화는 Store 제출 문구와 기능 로드맵에 영향 여부를 점검한다.")
    if tag_counts.get("OpenBIM/표준"):
        comments.append("IFC, IDS, openBIM 표준 변화는 납품 기준과 품질검사 항목에 반영 가능성을 검토한다.")
    if tag_counts.get("AI/자동화"):
        comments.append("AI/자동화 사례는 생산성 개선 아이템과 내부 자동화 카탈로그 후보로 분류한다.")
    return comments or ["오늘 수집된 신호는 참고 수준으로 유지하고, 반복 노출 시 표준문서 또는 교육자료로 승격한다."]


def markdown_report(today: str, now: str, selected: list[FeedItem], failures: list[str]) -> str:
    rows = "\n".join(
        f"| {idx} | {item.category} | {item.title} | {', '.join(item.tags)} | {item.source} | [link]({item.url}) |"
        for idx, item in enumerate(selected, 1)
    ) or "|  |  | 수집 항목 없음 |  |  |  |"
    comments = "\n".join(f"- {line}" for line in strategic_commentary(selected))
    fail_text = "\n".join(f"- {failure}" for failure in failures) or "- 없음"
    return f"""---
type: daily-industry-briefing
date: {today}
status: generated
tags:
  - construction
  - design
  - bim
  - daily-briefing
  - telegram
---

# {today} 건설·설계·시공·BIM 데일리 브리핑

생성 시각: {now}

## 주요 신호

| No. | 분류 | 제목 | LUA BIM LAB 연결 | 출처 | 링크 |
|---:|---|---|---|---|---|
{rows}

## 조직 관점 요약

{comments}

## 지식 승격 기준

- 반복적으로 등장하는 품질검토, 간섭, 납품 기준 이슈는 `Model Quality Auditor` 룰 후보로 등록한다.
- 설계/시공/BIM 협업 사례는 연차별 교육 커리큘럼과 현업 배포 자료로 전환한다.
- Autodesk, Revit, openBIM, IDS, IFC 관련 변화는 표준문서와 Add-in 로드맵 영향도를 점검한다.
- 단발성 뉴스는 보관하되, 같은 주제가 3회 이상 반복되면 지식 큐레이션 회의의 승격 후보로 올린다.

## 수집 실패

{fail_text}
"""


def telegram_message(today: str, selected: list[FeedItem]) -> str:
    lines = [f"[LUA BIM LABS] {today} 건설·설계·시공·BIM 브리핑", ""]
    for idx, item in enumerate(selected[:7], 1):
        tags = ", ".join(item.tags[:2])
        lines.append(f"{idx}. {item.title}")
        lines.append(f"   - 연결: {tags}")
        if item.url:
            lines.append(f"   - {item.url}")
    lines.append("")
    lines.extend(f"- {line}" for line in strategic_commentary(selected)[:3])
    return "\n".join(lines)[:3900]


def append_knowledge_base(today: str, report_path: Path, selected: list[FeedItem]) -> None:
    KB_FILE.parent.mkdir(parents=True, exist_ok=True)
    if not KB_FILE.exists():
        KB_FILE.write_text("# 산업동향 데일리 브리핑 지식 베이스\n\n", encoding="utf-8")
    top_titles = "\n".join(f"- {item.title} ({', '.join(item.tags)})" for item in selected[:5]) or "- 수집 항목 없음"
    existing = KB_FILE.read_text(encoding="utf-8")
    heading = f"## {today} 건설·설계·시공·BIM 브리핑"
    pattern = rf"\n## {re.escape(today)} 건설·설계·시공·BIM 브리핑\n.*?(?=\n## |\Z)"
    existing = re.sub(pattern, "", existing, flags=re.S)
    entry = f"""
## {today} 건설·설계·시공·BIM 브리핑
- Source: `{report_path.relative_to(PROJECT_ROOT).as_posix()}`
- Tags: construction,design,bim,daily-briefing,telegram

주요 수집 항목:
{top_titles}

조직 관점:
{chr(10).join(f"- {line}" for line in strategic_commentary(selected))}
"""
    if heading not in existing:
        KB_FILE.write_text(existing.rstrip() + "\n\n" + entry, encoding="utf-8")


def send_telegram(message: str) -> bool:
    token = os.environ.get("TELEGRAM_BOT_TOKEN")
    chat_id = os.environ.get("TELEGRAM_CHAT_ID")
    if not token or not chat_id:
        print("telegram=skipped missing TELEGRAM_BOT_TOKEN or TELEGRAM_CHAT_ID")
        return False
    payload = urllib.parse.urlencode({"chat_id": chat_id, "text": message}).encode("utf-8")
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    request = urllib.request.Request(url, data=payload, method="POST")
    try:
        with urllib.request.urlopen(request, timeout=10) as response:
            print(f"telegram=sent status={response.status}")
        return True
    except Exception as exc:  # noqa: BLE001 - keep daily job non-fatal.
        print(f"telegram=failed {type(exc).__name__}: {exc}")
        return False


def run(send: bool) -> Path:
    load_local_env()
    today = dt.datetime.now().strftime("%Y-%m-%d")
    now = dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    config = json.loads(SOURCE_CONFIG.read_text(encoding="utf-8"))
    collected: list[FeedItem] = []
    failures: list[str] = []

    for source in config.get("sources", []):
        try:
            collected.extend(parse_feed(source))
        except Exception as exc:  # noqa: BLE001 - source failures are logged.
            failures.append(f"{source.get('name', 'unknown')}: {type(exc).__name__} {exc}")

    selected = balanced_selection(collected, total=12, per_source=3)
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    report_path = REPORT_DIR / f"{today}_CONSTRUCTION_DESIGN_BIM_DAILY_BRIEFING.md"
    report_path.write_text(markdown_report(today, now, selected, failures), encoding="utf-8")
    append_knowledge_base(today, report_path, selected)

    if send:
        sent_state = load_sent_state()
        new_items = filter_new_items(selected, sent_state)
        telegram_items = new_items[:7]
        if telegram_items:
            if send_telegram(telegram_message(today, telegram_items)):
                mark_items_sent(telegram_items, sent_state, today)
                save_sent_state(sent_state)
                print(f"telegram_new_items={len(telegram_items)} skipped_duplicates={len(selected) - len(new_items)}")
        else:
            save_sent_state(sent_state)
            print(f"telegram=skipped reason=no_new_items skipped_duplicates={len(selected)}")

    print(f"report={report_path}")
    print(f"items={len(selected)} failures={len(failures)}")
    return report_path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--no-telegram", action="store_true", help="Generate reports without sending Telegram.")
    args = parser.parse_args()
    run(send=not args.no_telegram)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
