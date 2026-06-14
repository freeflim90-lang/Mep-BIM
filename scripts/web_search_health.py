#!/usr/bin/env python3
"""웹검색 보강 백본 health 체크.

자가치유(약한 답변 → 웹검색 보강) 품질은 살아있는 검색 제공자 수에 직결된다.
키가 설정돼 있어도 쿼터 초과(Tavily 432)·API 미활성화(Google 403)·봇 차단
(DuckDuckGo 202)으로 조용히 죽어 보강이 Naver 단일 의존이 되는 일이 잦다.

  python scripts/web_search_health.py

각 제공자의 실제 응답(키 유무 + 라이브 여부)을 한 번에 보여준다.
"""
from __future__ import annotations

import asyncio
import os
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import httpx  # noqa: E402

PROBE = "BIM Revit 간섭검토"


def _load_env() -> None:
    env = PROJECT_ROOT / ".env"
    if not env.exists():
        return
    for line in env.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if "=" in line and not line.startswith("#"):
            k, _, v = line.partition("=")
            os.environ.setdefault(k.strip(), v.strip())


async def _check(client: httpx.AsyncClient) -> list[tuple[str, str, str]]:
    rows: list[tuple[str, str, str]] = []

    # Naver
    nid, nsec = os.environ.get("NAVER_CLIENT_ID", ""), os.environ.get("NAVER_CLIENT_SECRET", "")
    if not (nid and nsec):
        rows.append(("Naver", "키없음", "-"))
    else:
        try:
            r = await client.get("https://openapi.naver.com/v1/search/webkr.json",
                                 params={"query": PROBE, "display": 1},
                                 headers={"X-Naver-Client-Id": nid, "X-Naver-Client-Secret": nsec}, timeout=10)
            n = len(r.json().get("items", [])) if r.status_code == 200 else 0
            rows.append(("Naver", "LIVE" if r.status_code == 200 and n else f"HTTP {r.status_code}", f"{n} results"))
        except Exception as e:
            rows.append(("Naver", "ERROR", str(e)[:60]))

    # Tavily
    tk = os.environ.get("TAVILY_API_KEY", "")
    if not tk:
        rows.append(("Tavily", "키없음", "-"))
    else:
        try:
            r = await client.post("https://api.tavily.com/search",
                                  json={"api_key": tk, "query": PROBE, "max_results": 1}, timeout=12)
            rows.append(("Tavily", "LIVE" if r.status_code == 200 else f"HTTP {r.status_code}", str(r.text)[:70]))
        except Exception as e:
            rows.append(("Tavily", "ERROR", str(e)[:60]))

    # Google CSE
    gk, cx = os.environ.get("GOOGLE_API_KEY", ""), os.environ.get("GOOGLE_CSE_ID", "")
    if not (gk and cx):
        rows.append(("Google CSE", "키없음", "-"))
    else:
        try:
            r = await client.get("https://www.googleapis.com/customsearch/v1",
                                 params={"key": gk, "cx": cx, "q": PROBE, "num": 1}, timeout=12)
            rows.append(("Google CSE", "LIVE" if r.status_code == 200 else f"HTTP {r.status_code}", str(r.text)[:70]))
        except Exception as e:
            rows.append(("Google CSE", "ERROR", str(e)[:60]))

    # DuckDuckGo (lite 엔드포인트 — 실제 web_search.py 와 동일)
    try:
        r = await client.post("https://lite.duckduckgo.com/lite/", data={"q": PROBE},
                              headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"},
                              timeout=10, follow_redirects=True)
        live = r.status_code == 200 and "result-link" in r.text
        rows.append(("DuckDuckGo", "LIVE" if live else f"HTTP {r.status_code} 차단/구조변경", "-"))
    except Exception as e:
        rows.append(("DuckDuckGo", "ERROR", str(e)[:60]))

    return rows


async def main() -> int:
    _load_env()
    async with httpx.AsyncClient() as client:
        rows = await _check(client)
    live = sum(1 for _, status, _ in rows if status == "LIVE")
    print(f"웹검색 보강 백본: LIVE {live}/{len(rows)}")
    for name, status, detail in rows:
        mark = "✅" if status == "LIVE" else "❌"
        print(f"  {mark} {name:12} {status:24} {detail}")

    # 답변 전달 직전 DeepSeek 검수 설정 — 이름이 비슷한 두 플래그 혼동을 잡는다.
    answer_review = os.environ.get("DEEPSEEK_FINAL_ANSWER_REVIEW_ENABLED", "").lower() in {"1", "true", "yes", "on"}
    reasoning_review = os.environ.get("DEEPSEEK_FINAL_REVIEW_ENABLED", "true").lower() in {"1", "true", "yes", "on"}
    print("\nDeepSeek 검수 설정:")
    print(f"  {'✅' if answer_review else '❌'} 고객 답변 검수  (DEEPSEEK_FINAL_ANSWER_REVIEW_ENABLED)")
    print(f"  {'✅' if reasoning_review else '❌'} 추론 피드백 검수 (DEEPSEEK_FINAL_REVIEW_ENABLED)")
    if reasoning_review and not answer_review:
        print("  WARN: 추론 검수만 켜짐 — 고객 답변 DeepSeek 검수는 꺼진 상태(플래그명 혼동 가능).")
    if live == 0:
        print("FAIL: 살아있는 검색 제공자 없음 — 자가치유 웹보강 불가")
        return 1
    if live == 1:
        print("WARN: 단일 제공자 의존 — 장애 시 보강 중단 위험")
    return 0


if __name__ == "__main__":
    raise SystemExit(asyncio.run(main()))
