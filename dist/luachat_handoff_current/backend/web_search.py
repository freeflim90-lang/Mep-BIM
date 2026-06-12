"""
SECTION 7 (부분) ── 웹 검색 파이프라인
  - Naver / Tavily / Google CSE / DuckDuckGo 병렬 검색
  - _build_search_query  : 에이전트 컨텍스트 기반 검색어 생성
  - _search_web_for_knowledge : 병렬 검색 → 결과 병합
  - _save_search_result_to_knowledge : 검색 결과 지식 파일 저장
"""
from __future__ import annotations

import asyncio
import datetime
import os
import re

import httpx

from backend.knowledge_store import KNOWLEDGE_DIR, knowledge_file_path

# ---------------------------------------------------------------------------
# 에이전트별 영문 검색 컨텍스트 (DuckDuckGo 쿼리 품질 향상용)
# ---------------------------------------------------------------------------
_AGENT_SEARCH_CONTEXT: dict[str, str] = {
    "CEO": "BIM software product strategy Autodesk App Store add-in",
    "조율차장": "BIM project management coordination MEP add-in development",
    "건축": "architecture BIM Revit clearance fire compartment floor plan add-in",
    "구조": "structural BIM Revit beam column slab penetration opening reinforcement",
    "토목": "civil BIM site utility invert level drainage connection",
    "위생": "plumbing BIM Revit drainage slope vent pipe sanitary",
    "공조배관": "HVAC piping BIM Revit insulation valve clash detection MEP",
    "공조덕트": "HVAC duct BIM Revit airflow pressure drop damper clearance",
    "소방기계": "fire suppression BIM Revit sprinkler head coverage pipe routing",
    "소방전기": "fire alarm BIM Revit detector wiring panel coordination",
    "전기": "electrical BIM Revit cable tray panel clearance EMI separation",
    "통신": "low voltage telecom BIM Revit cable tray network CCTV separation",
    "Revit_Addin": "Revit API IExternalCommand addin manifest C# .NET development",
    "Navisworks_Addin": "Navisworks API plugin .NET clash detection automation export",
    "요구사항분석": "BIM add-in requirements analysis user story scope Revit Navisworks",
    "빌드검증": "Revit add-in build validation smoke test manifest deployment",
    "배포문서": "Revit add-in deployment documentation installer user guide",
    "제품패키징": "Revit add-in MSI installer packaging Autodesk App Store",
    "스토어심사": "Autodesk App Store review guidelines submission product",
    "라이선스결제": "Autodesk App Store license payment subscription entitlement",
    "고객지원 CS": "BIM add-in customer support operations privacy policy refund technical escalation",
    "QA_테스터": "Revit add-in QA testing regression crash performance",
    "테크니컬_라이터": "BIM add-in technical documentation release notes user guide",
    "지식큐레이터": "knowledge curation taxonomy Obsidian graph documentation governance BIM knowledge management",
    "지식업데이트": "",
    "라이선스_보안관": "BIM add-in license security privacy data protection",
    "프로그램개발": "Revit Navisworks add-in C# .NET development architecture",
}

_KNOWLEDGE_MIN_CHARS = 300  # 이 미만이면 지식 부족으로 판단


def _build_search_query(agent_name: str, user_prompt: str) -> str:
    """에이전트 도메인 컨텍스트를 고려한 검색 쿼리를 생성합니다."""
    core_prompt = user_prompt.split("\n\n")[0].strip()
    context = _AGENT_SEARCH_CONTEXT.get(agent_name, "")
    en_words = [w for w in re.findall(r'[A-Za-z0-9\-\.]+', core_prompt) if len(w) > 2]
    ko_words = [w for w in re.findall(r'[가-힣A-Za-z0-9_#+.\-]{2,}', core_prompt) if len(w) > 1]
    stopwords = {"으로", "에서", "대한", "관련", "정리", "알려줘", "해주세요", "기준", "질문", "요청",
                 "더", "찾아줘", "부족", "목표", "Telegram", "FAQ"}
    terms = []
    for word in en_words + ko_words:
        token = word.strip()
        if token and token.lower() not in stopwords and token not in terms:
            terms.append(token)
    extra = " ".join(terms[:8])
    bim_terms = {"revit", "bim", "addin", "navisworks", "dynamo", "clash", "클래시",
                 "모델링", "배관", "덕트", "케이블트레이", "소방", "전기", "위생"}
    has_bim = any(t in core_prompt.lower() for t in bim_terms)
    if context and has_bim:
        return f"{context} {extra}".strip()
    return extra.strip() or core_prompt[:120]


async def _search_tavily(query: str, client: httpx.AsyncClient) -> list[dict]:
    """Tavily Search API로 검색합니다. include_answer=true로 AI 요약 답변도 수집합니다."""
    api_key = os.environ.get("TAVILY_API_KEY", "")
    if not api_key:
        return []
    try:
        resp = await client.post(
            "https://api.tavily.com/search",
            json={"api_key": api_key, "query": query, "search_depth": "advanced",
                  "include_answer": True, "max_results": 5},
            timeout=15,
        )
        data = resp.json()
        results = data.get("results", [])
        tavily_answer = (data.get("answer") or "").strip()
        if tavily_answer:
            results.insert(0, {"title": "Tavily AI 요약", "content": tavily_answer,
                                "url": "", "_is_tavily_answer": True})
        return results
    except Exception as exc:
        print(f"⚠️ [Tavily 오류] {exc}")
        return []


async def _search_duckduckgo(query: str, client: httpx.AsyncClient) -> list[dict]:
    """DuckDuckGo HTML 검색으로 스니펫을 수집합니다."""
    try:
        resp = await client.get(
            "https://html.duckduckgo.com/html/",
            params={"q": query},
            headers={"User-Agent": "Mozilla/5.0 (compatible; LUABIMBot/1.0)"},
            timeout=12,
            follow_redirects=True,
        )
        titles = re.findall(r'class="result__a"[^>]*>(.*?)</a>', resp.text, re.DOTALL)
        snippets = re.findall(r'class="result__snippet"[^>]*>(.*?)</a>', resp.text, re.DOTALL)
        results = []
        for title, snippet in zip(titles[:5], snippets[:5]):
            clean_title = re.sub(r'<[^>]+>', '', title).strip()
            clean_snippet = re.sub(r'<[^>]+>', '', snippet).strip()
            if clean_snippet:
                results.append({"title": clean_title, "content": clean_snippet, "source": "duckduckgo"})
        return results
    except Exception as exc:
        print(f"⚠️ [DuckDuckGo 오류] {exc}")
        return []


async def _search_google_cse(query: str, client: httpx.AsyncClient) -> list[dict]:
    """Google Custom Search API로 검색합니다."""
    api_key = os.environ.get("GOOGLE_API_KEY", "")
    cse_id = os.environ.get("GOOGLE_CSE_ID", "")
    if not api_key or not cse_id:
        return []
    try:
        resp = await client.get(
            "https://www.googleapis.com/customsearch/v1",
            params={"key": api_key, "cx": cse_id, "q": query, "num": 5, "hl": "ko"},
            timeout=12,
        )
        data = resp.json()
        results = []
        for item in data.get("items", []):
            results.append({
                "title": item.get("title", ""),
                "content": item.get("snippet", ""),
                "url": item.get("link", ""),
            })
        return results
    except Exception as exc:
        print(f"⚠️ [Google CSE 오류] {exc}")
        return []


async def _search_naver(query: str, client: httpx.AsyncClient) -> list[dict]:
    """Naver 검색 API로 검색합니다 (웹문서 + 뉴스)."""
    client_id = os.environ.get("NAVER_CLIENT_ID", "")
    client_secret = os.environ.get("NAVER_CLIENT_SECRET", "")
    if not client_id or not client_secret:
        return []
    headers = {"X-Naver-Client-Id": client_id, "X-Naver-Client-Secret": client_secret}
    results: list[dict] = []
    try:
        for search_type in ("webkr", "news"):
            resp = await client.get(
                f"https://openapi.naver.com/v1/search/{search_type}.json",
                params={"query": query, "display": 4, "sort": "sim"},
                headers=headers,
                timeout=12,
            )
            if resp.status_code != 200:
                continue
            for item in resp.json().get("items", []):
                title = re.sub(r"<[^>]+>", "", item.get("title", "")).strip()
                desc = re.sub(r"<[^>]+>", "", item.get("description", "")).strip()
                link = item.get("link", "") or item.get("originallink", "")
                if desc:
                    results.append({"title": title, "content": desc, "url": link})
    except Exception as exc:
        print(f"⚠️ [Naver 오류] {exc}")
    return results


async def _search_web_for_knowledge(agent_name: str, user_prompt: str) -> str:
    """Naver + Tavily + Google CSE + DuckDuckGo를 병렬로 검색하여 결과를 병합합니다."""
    query = _build_search_query(agent_name, user_prompt)
    print(f"🔍 [병렬 검색] {agent_name} | 쿼리: {query}")

    async with httpx.AsyncClient() as client:
        naver_task = asyncio.create_task(_search_naver(query, client))
        tavily_task = asyncio.create_task(_search_tavily(query, client))
        google_task = asyncio.create_task(_search_google_cse(query, client))
        ddg_task = asyncio.create_task(_search_duckduckgo(query, client))
        naver_results, tavily_results, google_results, ddg_results = await asyncio.gather(
            naver_task, tavily_task, google_task, ddg_task
        )

    tavily_ai_block = ""
    tavily_snippets = []
    for item in tavily_results:
        if item.get("_is_tavily_answer"):
            content = (item.get("content") or "").strip()[:500]
            if content:
                tavily_ai_block = f"• [Tavily] Tavily AI 요약\n  {content}\n  출처: "
        else:
            tavily_snippets.append(item)

    seen_snippets: set[str] = set()
    merged: list[str] = []

    for item in naver_results:
        title = item.get("title", "").strip()
        content = item.get("content", "").strip()[:300]
        url = item.get("url", "")
        key = content[:80]
        if content and key not in seen_snippets:
            seen_snippets.add(key)
            merged.append(f"• [Naver] {title}\n  {content}\n  출처: {url}")

    for item in google_results:
        title = item.get("title", "").strip()
        content = item.get("content", "").strip()[:300]
        url = item.get("url", "")
        key = content[:80]
        if content and key not in seen_snippets:
            seen_snippets.add(key)
            merged.append(f"• [Google] {title}\n  {content}\n  출처: {url}")

    for item in tavily_snippets:
        title = item.get("title", "").strip()
        content = (item.get("content") or item.get("snippet") or "").strip()[:300]
        url = item.get("url", "")
        key = content[:80]
        if content and key not in seen_snippets:
            seen_snippets.add(key)
            merged.append(f"• [Tavily] {title}\n  {content}\n  출처: {url}")

    for item in ddg_results:
        content = item.get("content", "").strip()
        key = content[:80]
        if content and key not in seen_snippets:
            seen_snippets.add(key)
            merged.append(f"• [DDG] {item.get('title','')}\n  {content}")

    result_blocks = ([tavily_ai_block] if tavily_ai_block else []) + merged[:7]
    print(f"✅ [검색 완료] Naver {len(naver_results)}건 + Google {len(google_results)}건 + Tavily {len(tavily_snippets)}건 + DDG {len(ddg_results)}건 → 병합 {len(result_blocks)}건")
    return "\n\n".join(result_blocks) if result_blocks else ""


def _save_search_result_to_knowledge(agent_name: str, query: str, content: str) -> None:
    """검색 결과를 해당 에이전트의 지식 파일에 자동 저장합니다."""
    if not content:
        return
    path = knowledge_file_path(agent_name)

    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    if not os.path.exists(path):
        os.makedirs(KNOWLEDGE_DIR, exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            f.write(f"# {agent_name} 지식 베이스\n")
    entry = (
        f"\n\n## 웹 검색 자동 수집 ({now})\n"
        f"- Source: DuckDuckGo search\n"
        f"- Query: {query}\n"
        f"- Tags: auto,search\n\n"
        f"{content}\n"
    )
    with open(path, "a", encoding="utf-8") as f:
        f.write(entry)
    print(f"💾 [지식 자동 저장] {agent_name} → {path}")
