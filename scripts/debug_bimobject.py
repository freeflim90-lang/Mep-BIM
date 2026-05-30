#!/usr/bin/env python3
"""BIMobject API 엔드포인트 탐지 — 네트워크 요청 캡처"""

from pathlib import Path
from playwright.sync_api import sync_playwright
import time, json

DEBUG_DIR = Path(__file__).resolve().parents[1] / "data" / "bimobject" / "debug"
DEBUG_DIR.mkdir(parents=True, exist_ok=True)

URL = "https://www.bimobject.com/ko/search?categories=mep&software=revit&sort=downloads"

api_calls = []

with sync_playwright() as pw:
    browser = pw.chromium.launch(headless=True, args=[
        "--no-sandbox",
        "--disable-blink-features=AutomationControlled",
    ])
    ctx = browser.new_context(
        user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
        viewport={"width": 1440, "height": 900},
        locale="ko-KR",
    )

    # 네트워크 요청 인터셉트
    def on_response(response):
        url = response.url
        ct = response.headers.get("content-type", "")
        if "json" in ct and any(k in url for k in ["api", "search", "product", "bim", "graphql"]):
            try:
                body = response.json()
                api_calls.append({
                    "url": url,
                    "status": response.status,
                    "body_preview": json.dumps(body, ensure_ascii=False)[:300],
                    "body": body,
                })
                print(f"  [API] {response.status} {url[:100]}")
            except:
                api_calls.append({"url": url, "status": response.status, "body_preview": "parse error"})

    page = ctx.new_page()
    page.add_init_script("Object.defineProperty(navigator, 'webdriver', { get: () => undefined });")
    page.on("response", on_response)

    print(f"접속 중: {URL}")
    page.goto(URL, wait_until="networkidle", timeout=45000)
    time.sleep(5)  # Angular 렌더링 대기

    print(f"\n=== 캡처된 API 요청 ({len(api_calls)}개) ===")
    for call in api_calls:
        print(f"\n[{call['status']}] {call['url']}")
        print(f"  {call['body_preview']}")

    # 전체 API 응답 저장
    api_path = DEBUG_DIR / "api_calls.json"
    api_path.write_text(json.dumps(api_calls, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\nAPI 응답 저장: {api_path}")

    # 스크린샷 (5초 후)
    ss_path = DEBUG_DIR / "bimobject_loaded.png"
    page.screenshot(path=str(ss_path), full_page=True)
    print(f"스크린샷: {ss_path}")

    # 렌더링된 제품 카드 확인
    print("\n=== 렌더링된 DOM ===")
    for sel in ["app-product-card", "[class*='product-card']", ".uk-grid > *", "app-search-results li", "app-search-results > div > div > *"]:
        els = page.query_selector_all(sel)
        print(f"  {sel}: {len(els)}개")

    browser.close()

print("완료")
