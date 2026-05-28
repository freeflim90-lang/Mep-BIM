"""
LUA BIM LAND — 백엔드 API 통합 테스트
사전 조건: uvicorn backend.server_total:app --reload 실행 중

실행:
    python scripts/test_bim_land_api.py
"""

import json
import sys
import datetime
import urllib.request
import urllib.error

BASE_URL = "http://127.0.0.1:8000"

PASS = "✅"
FAIL = "❌"


def post(path: str, payload: dict) -> dict:
    data = json.dumps(payload).encode()
    req = urllib.request.Request(
        f"{BASE_URL}{path}",
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=10) as resp:
        return json.loads(resp.read())


def get(path: str) -> dict | list:
    with urllib.request.urlopen(f"{BASE_URL}{path}", timeout=10) as resp:
        return json.loads(resp.read())


def check(label: str, condition: bool, detail: str = "") -> bool:
    icon = PASS if condition else FAIL
    print(f"  {icon} {label}" + (f"  ({detail})" if detail else ""))
    return condition


# ── 테스트 케이스 ──────────────────────────────────────────────────────────────

def test_normal_grade():
    print("\n[1] Normal 등급 동기화 (송도 오피스, D_BIM ≈ 0.17)")
    r = post("/api/bim-land/sync", {
        "project_code":      "PRJ-INCHEON-001",
        "project_name":      "인천 송도 D타워 오피스",
        "user_email":        "engineer@luabim.com",
        "total_elements":    500,
        "gross_floor_area_ft2": 32291.0,   # 3000 m²
        "latitude":          37.3926,
        "longitude":         126.6430,
    })
    ok = (
        check("status == ok",           r.get("status") == "ok")
        & check("등급 == Normal",        r.get("territory_grade") == "Normal",  str(r.get("territory_grade")))
        & check("XP > 0",               r.get("xp_earned", 0) > 0,             str(r.get("xp_earned")))
        & check("shadow_strike == False", not r.get("shadow_strike"),           str(r.get("shadow_strike")))
    )
    return ok


def test_rare_grade():
    print("\n[2] Rare 등급 동기화 (강남 아파트, D_BIM ≈ 0.83)")
    r = post("/api/bim-land/sync", {
        "project_code":   "PRJ-GANGNAM-002",
        "project_name":   "강남구 역삼 주상복합 A동",
        "user_email":     "bim01@luabim.com",
        "total_elements": 5000,
        "gross_floor_area_ft2": 64583.0,   # 6000 m²
        "latitude":       37.5013,
        "longitude":      127.0398,
    })
    ok = (
        check("status == ok",  r.get("status") == "ok")
        & check("등급 == Rare", r.get("territory_grade") == "Rare", str(r.get("territory_grade")))
    )
    return ok


def test_legendary_grade():
    print("\n[3] Legendary 등급 동기화 (반도체 플랜트, D_BIM ≈ 5.0)")
    r = post("/api/bim-land/sync", {
        "project_code":   "PRJ-HWASEONG-003",
        "project_name":   "화성 반도체 FAB 플랜트 MEP",
        "user_email":     "mep.lead@luabim.com",
        "total_elements": 150000,
        "gross_floor_area_ft2": 322917.0,  # 30000 m²
        "latitude":       37.1997,
        "longitude":      126.8318,
    })
    ok = (
        check("status == ok",          r.get("status") == "ok")
        & check("등급 == Legendary",    r.get("territory_grade") == "Legendary", str(r.get("territory_grade")))
        & check("grade_mult == 3.0",   r.get("grade_multiplier") == 3.0,        str(r.get("grade_multiplier")))
        & check("XP > 50000",          r.get("xp_earned", 0) > 50000,           str(r.get("xp_earned")))
    )
    return ok


def test_shadow_strike():
    print("\n[4] Shadow Strike 발동 (이직 시나리오)")
    # 1차: luabim.com 소속으로 동기화
    post("/api/bim-land/sync", {
        "project_code":   "PRJ-BUSAN-004",
        "project_name":   "부산 해운대 랜드마크 타워",
        "user_email":     "veteran@luabim.com",
        "total_elements": 8000,
        "gross_floor_area_ft2": 107639.0,  # 10000 m²
        "latitude": 35.1595, "longitude": 129.1603,
    })
    # 2차: competitor.com 소속으로 동기화 (이직)
    r = post("/api/bim-land/sync", {
        "project_code":   "PRJ-BUSAN-004",
        "project_name":   "부산 해운대 랜드마크 타워 리모델링",
        "user_email":     "veteran@competitor.com",
        "total_elements": 4000,
        "gross_floor_area_ft2": 107639.0,
        "latitude": 35.1595, "longitude": 129.1603,
    })
    ok = (
        check("status == ok",            r.get("status") == "ok")
        & check("shadow_strike == True", r.get("shadow_strike") is True, str(r.get("shadow_strike")))
        & check("ss_mult >= 1.3",        r.get("shadow_strike_multiplier", 1.0) >= 1.3,
                str(r.get("shadow_strike_multiplier")))
    )
    return ok


def test_no_floor_area():
    print("\n[5] 연면적 0 — 요소 수 기반 XP 추정")
    r = post("/api/bim-land/sync", {
        "project_code":   "PRJ-DAEJEON-005",
        "project_name":   "대전 정부청사 증축",
        "user_email":     "arch@luabim.com",
        "total_elements": 3000,
        "gross_floor_area_ft2": 0,
        "latitude": 36.4800, "longitude": 127.2890,
    })
    ok = (
        check("status == ok", r.get("status") == "ok")
        & check("XP > 0",     r.get("xp_earned", 0) > 0, str(r.get("xp_earned")))
    )
    return ok


def test_territories_endpoint():
    print("\n[6] GET /api/bim-land/territories")
    data = get("/api/bim-land/territories")
    ok = (
        check("dict 반환",          isinstance(data, dict))
        & check("PRJ-INCHEON-001 존재", "PRJ-INCHEON-001" in data)
    )
    return ok


def test_leaderboard_endpoint():
    print("\n[7] GET /api/bim-land/leaderboard")
    data = get("/api/bim-land/leaderboard")
    ok = (
        check("list 반환",      isinstance(data, list))
        & check("항목 1개 이상", len(data) >= 1)
        & check("rank 키 존재", all("rank" in item for item in data))
    )
    return ok


# ── 실행 ───────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("=" * 55)
    print("  LUA BIM LAND  백엔드 API 테스트")
    print(f"  대상: {BASE_URL}")
    print(f"  시각: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 55)

    tests = [
        test_normal_grade,
        test_rare_grade,
        test_legendary_grade,
        test_shadow_strike,
        test_no_floor_area,
        test_territories_endpoint,
        test_leaderboard_endpoint,
    ]

    results = []
    for t in tests:
        try:
            results.append(t())
        except urllib.error.URLError:
            print(f"  {FAIL} 서버 연결 실패 — uvicorn 실행 확인")
            results.append(False)
        except Exception as e:
            print(f"  {FAIL} 예외: {e}")
            results.append(False)

    passed = sum(results)
    total  = len(results)
    print(f"\n{'='*55}")
    print(f"  결과: {passed}/{total} 통과  {'🎉' if passed == total else '⚠️'}")
    print("=" * 55)
    sys.exit(0 if passed == total else 1)
