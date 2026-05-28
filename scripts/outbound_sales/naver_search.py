# ================================================================
# naver_search.py — 네이버 검색 API 연동
#
# 사용 API (무료 25,000건/일):
#   - 지역 검색: 구글맵이 못 잡는 국내 소규모 업체 보완
#   - 웹 검색:   업체 이메일 폴백 탐색
#
# API 키 발급: https://developers.naver.com/apps
#   → 애플리케이션 등록 → 검색 API 선택
# ================================================================
import re
import requests
from config import NAVER_CLIENT_ID, NAVER_CLIENT_SECRET

NAVER_LOCAL_URL = "https://openapi.naver.com/v1/search/local.json"
NAVER_WEB_URL   = "https://openapi.naver.com/v1/search/webkr.json"

EMAIL_PATTERN = re.compile(r"[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}")

EXCLUDE_DOMAINS = {
    "example.com", "test.com", "noreply.com",
    "wixpress.com", "sentry.io", "naver.com",
    "kakao.com", "daum.net",
    "png", "jpg", "jpeg", "gif",
}

_HEADERS = {
    "X-Naver-Client-Id":     NAVER_CLIENT_ID,
    "X-Naver-Client-Secret": NAVER_CLIENT_SECRET,
}

_AVAILABLE = bool(
    NAVER_CLIENT_ID and NAVER_CLIENT_ID != "YOUR_NAVER_CLIENT_ID"
)


def _strip_tags(text: str) -> str:
    """네이버 API 응답의 HTML 태그 제거"""
    return re.sub(r"<[^>]+>", "", text).strip()


# ── 지역 검색 ───────────────────────────────────────────────────

def search_local(keyword: str, display: int = 5) -> list[dict]:
    """
    네이버 지역 검색으로 업체 목록 반환.
    구글맵 Places API 결과를 보완하는 용도.

    반환 형태:
        [{"name", "address", "telephone", "link", "category"}, ...]
    """
    if not _AVAILABLE:
        return []

    params = {
        "query":   keyword,
        "display": min(display, 5),   # 최대 5건 (무료 플랜)
        "sort":    "comment",
    }
    try:
        resp = requests.get(NAVER_LOCAL_URL, headers=_HEADERS, params=params, timeout=8)
        data = resp.json()

        if "errorCode" in data:
            print(f"  [NAVER LOCAL 오류] {data.get('errorMessage')}")
            return []

        results = []
        for item in data.get("items", []):
            results.append({
                "name":      _strip_tags(item.get("title", "")),
                "address":   item.get("roadAddress") or item.get("address", ""),
                "telephone": item.get("telephone", ""),
                "website":   item.get("link", ""),
                "category":  item.get("category", ""),
            })
        return results

    except Exception as e:
        print(f"  [NAVER LOCAL 예외] {e}")
        return []


def search_local_all(keywords: list[str], locations: list[str]) -> list[dict]:
    """
    키워드 × 지역 조합으로 네이버 지역 검색 전체 실행.
    place_id가 없으므로 '상호명+주소' 기반 중복 제거.
    """
    import time
    seen    = {}
    total   = len(keywords) * len(locations)
    done    = 0

    for location in locations:
        for keyword in keywords:
            done += 1
            query = f"{keyword} {location}"
            print(f"  [NAVER {done}/{total}] 🔍 {query}")

            items = search_local(query, display=5)
            for item in items:
                key = f"{item['name']}|{item['address']}"
                if key not in seen:
                    seen[key] = item
                    print(f"    ✅ {item['name']} | {item['telephone'] or '전화없음'}")

            time.sleep(0.3)

    return list(seen.values())


# ── 웹 검색 (이메일 폴백) ────────────────────────────────────────

def search_email_via_naver(company_name: str) -> list[str]:
    """
    네이버 웹 검색으로 업체 이메일 탐색.
    웹사이트 스캔으로 이메일을 못 찾은 경우 폴백으로 사용.
    """
    if not _AVAILABLE:
        return []

    query = f'"{company_name}" 이메일'
    params = {"query": query, "display": 5}

    try:
        resp = requests.get(NAVER_WEB_URL, headers=_HEADERS, params=params, timeout=8)
        data = resp.json()

        if "errorCode" in data:
            return []

        found = set()
        for item in data.get("items", []):
            text = _strip_tags(item.get("title", "")) + " " + _strip_tags(item.get("description", ""))
            for email in EMAIL_PATTERN.findall(text):
                domain = email.split("@")[-1].lower()
                if not any(ex in domain for ex in EXCLUDE_DOMAINS):
                    found.add(email.lower())
        return sorted(found)

    except Exception:
        return []


def is_available() -> bool:
    return _AVAILABLE
