# ================================================================
# config.py — 설정 파일 (API 키, SMTP, 검색 키워드)
# 실제 값으로 교체 후 사용하세요.
# ================================================================

# ── Google API 키 ───────────────────────────────────────────────
GOOGLE_MAPS_API_KEY    = "AIzaSyCqv0O0mKu0FDhH03qUedvrz4u2_62L4gM"
GOOGLE_SEARCH_API_KEY  = "AIzaSyCqv0O0mKu0FDhH03qUedvrz4u2_62L4gM"
GOOGLE_DRIVE_API_KEY   = "AIzaSyCJaFwoBYl4dAtZV2O9a0yYUTCkYKC1HcU"
GOOGLE_SHEETS_API_KEY  = "AIzaSyCJaFwoBYl4dAtZV2O9a0yYUTCkYKC1HcU"
# Custom Search Engine ID — Google CSE 설정 후 아래에 입력
# https://programmablesearchengine.google.com 에서 생성
GOOGLE_CSE_ID          = "c48ebd1f977284dc2"

# ── 네이버 검색 API (무료 25,000건/일) ──────────────────────────
# https://developers.naver.com/apps 에서 애플리케이션 등록 후 발급
NAVER_CLIENT_ID     = "YOUR_NAVER_CLIENT_ID"
NAVER_CLIENT_SECRET = "YOUR_NAVER_CLIENT_SECRET"

# ── 이메일 발송 SMTP 설정 ────────────────────────────────────────
# 네이버 메일 사용 시:
#   SMTP_SERVER   = "smtp.naver.com"
#   SMTP_PORT     = 587
#   SENDER_EMAIL  = "your_id@naver.com"
#   SENDER_PASSWORD = "네이버 로그인 비밀번호"
#   ※ 네이버 메일 설정 → IMAP/SMTP 사용 허용 필요
#
# Gmail 사용 시:
#   SMTP_SERVER   = "smtp.gmail.com"
#   SENDER_EMAIL  = "your_email@gmail.com"
#   SENDER_PASSWORD = "Google 앱 비밀번호 (16자리)"

SMTP_SERVER     = "smtp.naver.com"
SMTP_PORT       = 587
SENDER_EMAIL    = "jycompany90@naver.com"
SENDER_PASSWORD = "K82N7NLBJ1FQ"
SENDER_NAME     = "LUA BIM LABS"

# ── 검색 키워드 (Google Maps 검색에 사용) ───────────────────────
SEARCH_KEYWORDS = [
    # MEP 직접 타겟 (핵심)
    "기계설비 설계 사무소",
    "기계설비 전문건설",
    "소방설비 설계 사무소",
    "전기 설비 설계",
    "배관 설계 전문",
    "HVAC 설계 전문",
    "플랜트 배관 설계",
    # BIM 설계·시공 타겟
    "건축사사무소 BIM",
    "건설사 BIM 담당",
    "종합건설 설계팀",
    # 발주처 타겟 (MEP 협력사 필요)
    "건축 설계 사무소",
    "종합건설회사",
]

# ── 검색 지역 ───────────────────────────────────────────────────
SEARCH_LOCATIONS = [
    "서울특별시",
    "경기도 성남시",
    "경기도 수원시",
    "경기도 화성시",
    "인천광역시",
    "부산광역시",
    "대구광역시",
    "광주광역시",
    "대전광역시",
    "울산광역시",
    "세종특별자치시",
]

# ── 데이터베이스 경로 ────────────────────────────────────────────
import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH  = os.path.join(BASE_DIR, "data", "companies.db")

# ── 이메일 발송 딜레이 (초) — 스팸 방지 ─────────────────────────
EMAIL_SEND_DELAY = 5

# ── 크롤링 딜레이 (초) — API Rate Limit 방지 ────────────────────
CRAWL_DELAY = 0.5
PAGE_TOKEN_DELAY = 2
