#!/usr/bin/env python3
"""Autodesk Marketplace 크롤러 — AEC 애드인 전량 수집 + AI 갭 분석

수집 대상:
  - AEC 산업, Revit / AutoCAD / Navisworks 제품군 (약 2900개)

수집 내용:
  - 앱 기본 정보 (이름, 퍼블리셔, 설명, 플랫폼, 언어)
  - 평점 / 리뷰 수 (배치 API)
  - 가격 플랜 (FREE / SUBSCRIPTION / ONE_TIME 등)

실행:
    python3 scripts/crawl_autodesk_market.py                 # 전체 수집 + 분석
    python3 scripts/crawl_autodesk_market.py --no-ai         # 수집만 (AI 분석 생략)
    python3 scripts/crawl_autodesk_market.py --no-telegram   # Telegram 발송 생략
    python3 scripts/crawl_autodesk_market.py --dry-run       # 1페이지만 테스트
"""

from __future__ import annotations

import argparse
import json
import os
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime
from pathlib import Path

# ─────────────── 경로 ───────────────────────────────────────────
PROJECT_ROOT = Path(__file__).resolve().parents[1]
import sys as _sys  # noqa: E402
if str(PROJECT_ROOT) not in _sys.path:
    _sys.path.insert(0, str(PROJECT_ROOT))
from backend.core.paths import AUTODESK_MARKET_DIR  # noqa: E402

DATA_DIR     = AUTODESK_MARKET_DIR
REPORT_DIR   = PROJECT_ROOT / "docs" / "autodesk_market"
BACKLOG_FILE = DATA_DIR / "priority_backlog.json"
ADDINS_DIR   = PROJECT_ROOT / "commercial_addins"

DATA_DIR.mkdir(parents=True, exist_ok=True)
REPORT_DIR.mkdir(parents=True, exist_ok=True)

# ─────────────── API ─────────────────────────────────────────────
API_BASE    = "https://developer.api.autodesk.com/ngappapi"
SEARCH_URL  = f"{API_BASE}/public/search"
RATING_URL  = f"{API_BASE}/public/apps/comments/batch-rating-summary"
PRICE_URL   = f"{API_BASE}/public/apps/price-plans/batch"

SEARCH_PARAMS = {
    "industries": "AEC",
    "productIds": "RVT,ACD,NAVMAN,NAVSIM",
    "limit": "50",
}

HEADERS = {
    "Accept": "application/json",
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
    ),
    "Referer": "https://marketplace.autodesk.com/",
    "Origin": "https://marketplace.autodesk.com",
}

BATCH_SIZE = 50   # 배치 API 최대 처리 수
REQ_DELAY  = 0.4  # 페이지 간 딜레이 (초)


# ─────────────── HTTP 유틸 ──────────────────────────────────────
def _get(url: str, params: dict | None = None, retries: int = 3) -> dict | list:
    if params:
        url = url + "?" + urllib.parse.urlencode(params)
    for attempt in range(retries):
        try:
            req = urllib.request.Request(url, headers=HEADERS)
            with urllib.request.urlopen(req, timeout=20) as r:
                return json.loads(r.read().decode("utf-8"))
        except (urllib.error.URLError, OSError) as exc:
            if attempt < retries - 1:
                time.sleep(2 ** attempt)
                continue
            raise RuntimeError(f"HTTP GET 실패 ({url[:80]}): {exc}") from exc
    return {}


def _batch_get(url: str, id_list: list[str], id_param: str = "appIds") -> dict:
    result: dict = {}
    for i in range(0, len(id_list), BATCH_SIZE):
        chunk = id_list[i : i + BATCH_SIZE]
        params = {id_param: ",".join(chunk)}
        try:
            data = _get(url, params)
            if isinstance(data, dict):
                result.update(data.get("results", data))
        except Exception as exc:
            print(f"  배치 요청 실패 (offset={i}): {exc}")
        time.sleep(REQ_DELAY)
    return result


# ─────────────── 수집 ─────────────────────────────────────────
def collect_all_apps(dry_run: bool = False) -> list[dict]:
    apps: list[dict] = []
    page = 1
    total = None

    while True:
        params = {**SEARCH_PARAMS, "page": str(page)}
        data = _get(SEARCH_URL, params)
        results = data.get("results", [])
        if total is None:
            total = data.get("total", 0)
            print(f"  전체 앱 수: {total:,}")

        apps.extend(results)
        print(f"  page={page} collected={len(results)} cumulative={len(apps)}/{total}")

        if not data.get("hasMore") or not results:
            break
        if dry_run and page >= 1:
            print("  (dry-run: 1페이지만 수집)")
            break
        page += 1
        time.sleep(REQ_DELAY)

    return apps


def enrich_with_ratings_and_prices(apps: list[dict]) -> list[dict]:
    app_ids = [a["appId"] for a in apps]

    print(f"  평점 배치 조회 ({len(app_ids)}개)...")
    ratings = _batch_get(RATING_URL, app_ids)

    print(f"  가격 배치 조회 ({len(app_ids)}개)...")
    prices  = _batch_get(PRICE_URL, app_ids)

    for app in apps:
        aid = app["appId"]
        r = ratings.get(aid, {})
        app["averageRating"]  = r.get("averageRating", 0)
        app["totalRatings"]   = r.get("totalRatings", 0)

        plan_list = prices.get(aid, [])
        if not plan_list:
            app["priceType"]   = "UNKNOWN"
            app["priceUSD"]    = None
        else:
            types = [p.get("type", "") for p in plan_list]
            if "FREE" in types:
                app["priceType"] = "FREE"
                app["priceUSD"]  = 0
            else:
                app["priceType"] = types[0] if types else "UNKNOWN"
                first_prices = plan_list[0].get("prices", [])
                if first_prices:
                    app["priceUSD"] = first_prices[0].get("amount")
                else:
                    app["priceUSD"] = None

    return apps


# ─────────────── 저장 ─────────────────────────────────────────
def save_snapshot(apps: list[dict], ts: str) -> Path:
    fname = DATA_DIR / f"market_{ts}.json"
    payload = {
        "crawled_at": datetime.now().isoformat(),
        "total": len(apps),
        "source": "marketplace.autodesk.com",
        "apps": apps,
    }
    fname.write_text(json.dumps(payload, ensure_ascii=False, indent=2))
    # latest 심볼릭
    latest = DATA_DIR / "market_latest.json"
    latest.write_text(json.dumps(payload, ensure_ascii=False, indent=2))
    print(f"  저장: {fname.name}")
    return fname


def load_previous_snapshot() -> list[dict]:
    latest = DATA_DIR / "market_latest.json"
    if not latest.exists():
        return []
    data = json.loads(latest.read_text())
    return data.get("apps", [])


def find_new_apps(current: list[dict], previous: list[dict]) -> list[dict]:
    prev_ids = {a["appId"] for a in previous}
    return [a for a in current if a["appId"] not in prev_ids]


# ─────────────── 분석 프롬프트 생성 ──────────────────────────
def _get_existing_addins() -> list[str]:
    addins = []
    if ADDINS_DIR.exists():
        for d in ADDINS_DIR.iterdir():
            if d.is_dir() and not d.name.startswith("_") and not d.name.startswith("."):
                addins.append(d.name.replace("_", " "))
    return addins


def build_analysis_prompt(apps: list[dict], new_apps: list[dict]) -> str:
    """Claude에 붙여넣을 분석 프롬프트 텍스트 생성."""
    existing = _get_existing_addins()
    top_rated = sorted(apps, key=lambda a: (a.get("totalRatings", 0), a.get("averageRating", 0)), reverse=True)[:30]

    top_summary = "\n".join(
        f"- {a['appName']} ({a.get('publisherName','?')}) | "
        f"평점={a.get('averageRating',0):.1f} 리뷰={a.get('totalRatings',0)} "
        f"가격={a.get('priceType','?')} ${a.get('priceUSD','?')} | {a.get('shortDescription','')[:80]}"
        for a in top_rated
    )

    new_summary = "\n".join(
        f"- {a['appName']} ({a.get('publisherName','?')}) | {a.get('shortDescription','')[:80]}"
        for a in new_apps[:20]
    ) or "- 없음 (첫 수집 또는 변경 없음)"

    price_dist: dict[str, int] = {}
    for a in apps:
        pt = a.get("priceType", "UNKNOWN")
        price_dist[pt] = price_dist.get(pt, 0) + 1

    existing_str = "\n".join(f"- {a}" for a in existing) if existing else "- (아직 없음)"

    return f"""당신은 BIM 소프트웨어 회사 LUA BIM LABS의 제품 전략 분석가입니다.
Autodesk Marketplace에서 AEC 분야 앱 {len(apps):,}개를 수집했습니다.

## 현재 LUA BIM LABS 보유 애드인
{existing_str}

## 상위 30개 인기 앱 (평점/리뷰 기준)
{top_summary}

## 가격 분포
{json.dumps(price_dist, ensure_ascii=False)}

## 이번 크롤링에서 새로 발견된 앱 ({len(new_apps)}개)
{new_summary}

## 분석 요청
다음 형식으로 한국어로 분석해주세요:

### 1. 시장 갭 (우리가 개발할 수 있는 미개척 영역, 3~5개)
각 갭마다: 기능 설명, 왜 기회인지, 난이도 (하/중/상)

### 2. 검증된 수요 (높은 평점·리뷰를 가진 카테고리, 진입 가능성 있는 것 3개)
각 항목마다: 경쟁 앱 이름, 우리가 차별화할 수 있는 포인트

### 3. 한국 시장 특화 기회 (한국어 지원 없거나 한국 시장 특화가 필요한 기능)
2~3개

### 4. 우선순위 개발 추천 (종합, 1~3위)
순위, 앱 컨셉, 예상 개발 기간, 수익 모델
"""


# ─────────────── 백로그 업데이트 ─────────────────────────────
def update_priority_backlog(analysis_text: str, new_apps: list[dict], ts: str) -> list[dict]:
    existing: list[dict] = []
    if BACKLOG_FILE.exists():
        try:
            existing = json.loads(BACKLOG_FILE.read_text())
        except Exception:
            existing = []

    entry = {
        "date": ts[:8],
        "source": "autodesk_marketplace_crawl",
        "new_apps_count": len(new_apps),
        "analysis_summary": analysis_text[:500] if analysis_text else "",
        "new_app_samples": [
            {"name": a["appName"], "publisher": a.get("publisherName", ""), "desc": a.get("shortDescription", "")[:100]}
            for a in new_apps[:10]
        ],
    }
    existing.insert(0, entry)
    existing = existing[:30]  # 최근 30개 유지
    BACKLOG_FILE.write_text(json.dumps(existing, ensure_ascii=False, indent=2))
    return existing


# ─────────────── 리포트 생성 ──────────────────────────────────
def generate_report(apps: list[dict], new_apps: list[dict], ts: str) -> Path:
    top = sorted(apps, key=lambda a: (a.get("totalRatings", 0), a.get("averageRating", 0)), reverse=True)[:20]
    dt = f"{ts[:4]}-{ts[4:6]}-{ts[6:8]} {ts[9:11]}:{ts[11:13]}"

    lines = [
        "---",
        "type: autodesk-market-analysis",
        f"date: {ts[:4]}-{ts[4:6]}-{ts[6:8]}",
        f"total_apps: {len(apps)}",
        f"new_apps: {len(new_apps)}",
        "---",
        "",
        f"# Autodesk Marketplace 분석 — {dt}",
        "",
        f"수집: {len(apps):,}개 | 신규: {len(new_apps)}개",
        "",
        "## 상위 20개 인기 앱",
        "",
        "| 앱 이름 | 퍼블리셔 | 평점 | 리뷰 | 가격 |",
        "|---|---|---|---|---|",
    ]
    for a in top:
        price = f"${a.get('priceUSD','?')}" if a.get("priceType") not in ("FREE","UNKNOWN") else a.get("priceType","?")
        lines.append(
            f"| {a['appName'][:40]} | {a.get('publisherName','?')[:25]} "
            f"| {a.get('averageRating',0):.1f} | {a.get('totalRatings',0)} | {price} |"
        )

    if new_apps:
        lines += ["", f"## 신규 앱 ({len(new_apps)}개)", ""]
        for a in new_apps[:20]:
            lines.append(f"- **{a['appName']}** ({a.get('publisherName','?')}) — {a.get('shortDescription','')[:80]}")

    lines += [
        "",
        "## 분석 대기",
        "",
        "_Claude로 분석 후 `python3 scripts/send_market_analysis_telegram.py <분석파일>` 실행_",
    ]

    report_path = REPORT_DIR / f"{ts[:8]}_market_analysis.md"
    report_path.write_text("\n".join(lines), encoding="utf-8")
    print(f"  리포트: {report_path.name}")
    return report_path


# ─────────────── Telegram ─────────────────────────────────────
def send_telegram(message: str) -> bool:
    token   = os.environ.get("TELEGRAM_BOT_TOKEN", "")
    chat_id = os.environ.get("TELEGRAM_CHAT_ID", "")
    if not token or not chat_id:
        print("  telegram=skipped (env vars missing)")
        return False
    url  = f"https://api.telegram.org/bot{token}/sendMessage"
    body = json.dumps({"chat_id": chat_id, "text": message, "parse_mode": "HTML"}).encode()
    req  = urllib.request.Request(url, data=body, headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=15) as r:
            print(f"  telegram=sent status={r.status}")
            return True
    except Exception as exc:
        print(f"  telegram=failed {exc}")
        return False


def build_crawl_done_message(apps: list[dict], new_apps: list[dict], ts: str) -> str:
    """크롤링 완료 후 Telegram 체크리스트 메시지 (분석은 Claude가 직접)."""
    dt = f"{ts[:4]}-{ts[4:6]}-{ts[6:8]}"
    top = sorted(apps, key=lambda a: (a.get("totalRatings", 0), a.get("averageRating", 0)), reverse=True)[:5]

    lines = [
        f"<b>🔍 Autodesk Marketplace 수집 완료 — {dt}</b>",
        f"수집: {len(apps):,}개 | 신규: {len(new_apps)}개",
        "",
        "<b>📊 인기 앱 TOP 5</b>",
    ]
    for i, a in enumerate(top, 1):
        price = "FREE" if a.get("priceType") == "FREE" else f"${a.get('priceUSD','?')}"
        lines.append(
            f"{i}. {a['appName'][:35]}\n"
            f"   ⭐{a.get('averageRating',0):.1f}({a.get('totalRatings',0)}리뷰) | {price}"
        )

    if new_apps:
        lines += ["", f"<b>✨ 신규 앱 {len(new_apps)}개</b>"]
        for a in new_apps[:3]:
            lines.append(f"• {a['appName'][:40]}")

    lines += [
        "",
        "<b>📋 분석 체크리스트</b>",
        "☐ 1. Claude에서 갭 분석 실행",
        f"    파일: {AUTODESK_MARKET_DIR.name}/market_{ts}.json",
        "☐ 2. 분석 완료 후 Telegram 발송:",
        "    python3 scripts/send_market_analysis_telegram.py",
    ]
    return "\n".join(lines)


# ─────────────── 메인 ─────────────────────────────────────────
def run(dry_run: bool = False, no_telegram: bool = False) -> None:
    ts = datetime.now().strftime("%Y%m%d_%H%M")
    print(f"=== Autodesk Marketplace 크롤링 시작 ({ts}) ===")

    print("[1/4] 앱 목록 수집 중...")
    previous_apps = load_previous_snapshot()
    apps = collect_all_apps(dry_run=dry_run)
    if not apps:
        print("  수집된 앱 없음 — 종료")
        return

    print(f"[2/4] 평점·가격 보강 중 ({len(apps)}개)...")
    apps = enrich_with_ratings_and_prices(apps)

    print("[3/4] 스냅샷 저장...")
    save_snapshot(apps, ts)
    new_apps = find_new_apps(apps, previous_apps)
    print(f"  신규 앱: {len(new_apps)}개 (이전 스냅샷 대비)")

    # 분석 프롬프트를 파일로 저장 (Claude에서 직접 사용)
    prompt_path = DATA_DIR / "analysis_prompt_latest.txt"
    prompt_path.write_text(build_analysis_prompt(apps, new_apps), encoding="utf-8")
    print(f"  분석 프롬프트 저장: {prompt_path.name}")

    print("[4/4] 리포트 생성 및 Telegram 발송...")
    generate_report(apps, new_apps, ts)
    update_priority_backlog("", new_apps, ts)

    if not no_telegram:
        msg = build_crawl_done_message(apps, new_apps, ts)
        send_telegram(msg)
    else:
        print("  telegram=skipped (--no-telegram)")

    print(f"\n=== 완료: {len(apps):,}개 수집, 신규 {len(new_apps)}개 ===")
    print(f"  분석 준비: {AUTODESK_MARKET_DIR}/analysis_prompt_latest.txt")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Autodesk Marketplace 크롤러")
    parser.add_argument("--dry-run", action="store_true", help="1페이지만 테스트 수집")
    parser.add_argument("--no-telegram", action="store_true", help="Telegram 발송 생략")
    args = parser.parse_args()
    run(dry_run=args.dry_run, no_telegram=args.no_telegram)
