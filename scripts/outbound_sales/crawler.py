# ================================================================
# crawler.py — Google Maps Places API 기반 업체 크롤링
# ================================================================
import re
import requests
import time
from config import (
    GOOGLE_MAPS_API_KEY,
    SEARCH_KEYWORDS,
    SEARCH_LOCATIONS,
    CRAWL_DELAY,
    PAGE_TOKEN_DELAY,
)

TEXT_SEARCH_URL = "https://maps.googleapis.com/maps/api/place/textsearch/json"
DETAILS_URL     = "https://maps.googleapis.com/maps/api/place/details/json"
FIELDS          = "place_id,name,formatted_address,formatted_phone_number,website,types"


def _text_search(query: str) -> list[dict]:
    """한 키워드로 Places Text Search 실행 (페이지네이션 포함)"""
    results = []
    params = {
        "query":    query,
        "key":      GOOGLE_MAPS_API_KEY,
        "language": "ko",
        "region":   "kr",
    }

    while True:
        resp = requests.get(TEXT_SEARCH_URL, params=params, timeout=10)
        data = resp.json()
        status = data.get("status")

        if status == "ZERO_RESULTS":
            break
        if status != "OK":
            print(f"  [WARN] Places API 오류: {status} ({query})")
            break

        results.extend(data.get("results", []))

        next_token = data.get("next_page_token")
        if not next_token:
            break

        time.sleep(PAGE_TOKEN_DELAY)
        params = {"pagetoken": next_token, "key": GOOGLE_MAPS_API_KEY}

    return results


def _get_details(place_id: str) -> dict:
    """Place ID로 상세 정보(웹사이트·전화) 조회"""
    params = {
        "place_id": place_id,
        "fields":   FIELDS,
        "key":      GOOGLE_MAPS_API_KEY,
        "language": "ko",
    }
    resp = requests.get(DETAILS_URL, params=params, timeout=10)
    return resp.json().get("result", {})


def crawl_naver(keywords: list[str] = None, locations: list[str] = None) -> list[dict]:
    """
    네이버 지역 검색으로 업체 수집 (구글맵 보완용).
    place_id 없으므로 'naver_상호명+주소' 형태로 고유 ID 생성.
    """
    from naver_search import search_local_all, is_available
    if not is_available():
        print("[NAVER] API 키 미설정 — 건너뜀")
        return []

    keywords  = keywords  or SEARCH_KEYWORDS
    locations = locations or SEARCH_LOCATIONS

    print("[NAVER] 지역 검색 시작")
    items = search_local_all(keywords, locations)

    companies = []
    for item in items:
        fake_pid = "naver_" + re.sub(r"\s+", "_", item["name"]) + "_" + item["address"][:10]
        companies.append({
            "place_id": fake_pid,
            "name":     item["name"],
            "address":  item["address"],
            "phone":    item["telephone"],
            "website":  item["website"],
            "email":    "",
            "category": item["category"] or "네이버지역검색",
        })
    print(f"[NAVER] 수집 완료: {len(companies)}개")
    return companies


def crawl(keywords: list[str] = None, locations: list[str] = None) -> list[dict]:
    """
    키워드 × 지역 조합으로 전체 크롤링.
    중복 place_id 제거 후 리스트 반환.
    """
    keywords  = keywords  or SEARCH_KEYWORDS
    locations = locations or SEARCH_LOCATIONS

    seen      = {}   # place_id → company dict (중복 방지)
    total_req = len(keywords) * len(locations)
    done      = 0

    for location in locations:
        for keyword in keywords:
            done += 1
            query = f"{keyword} {location}"
            print(f"[{done}/{total_req}] 🔍 {query}")

            try:
                places = _text_search(query)
            except Exception as e:
                print(f"  [ERROR] 검색 실패: {e}")
                continue

            for place in places:
                pid = place.get("place_id")
                if not pid or pid in seen:
                    continue

                time.sleep(CRAWL_DELAY)
                try:
                    details = _get_details(pid)
                except Exception as e:
                    print(f"  [ERROR] 상세 조회 실패: {e}")
                    details = {}

                company = {
                    "place_id": pid,
                    "name":     details.get("name")               or place.get("name", ""),
                    "address":  details.get("formatted_address")  or place.get("formatted_address", ""),
                    "phone":    details.get("formatted_phone_number", ""),
                    "website":  details.get("website", ""),
                    "email":    "",
                    "category": keyword,
                }
                seen[pid] = company
                print(f"  ✅ {company['name']} | {company['website'] or '웹사이트 없음'}")

    print(f"\n[CRAWL] 수집 완료: {len(seen)}개 업체")
    return list(seen.values())
