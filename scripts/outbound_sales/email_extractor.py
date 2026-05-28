# ================================================================
# email_extractor.py — 업체 웹사이트 + Google Custom Search로 이메일 추출
# ================================================================
import re
import requests
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup
# CSE 대신 DuckDuckGo 무료 검색 사용
try:
    from duckduckgo_search import DDGS
    _DDG_AVAILABLE = True
except ImportError:
    _DDG_AVAILABLE = False

# 이메일 정규식 (일반적인 패턴)
EMAIL_PATTERN = re.compile(
    r"[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}"
)

# 제외할 이메일 도메인 (SNS, 이미지 파일 등 노이즈)
EXCLUDE_DOMAINS = {
    "example.com", "test.com", "noreply.com",
    "wixpress.com", "sentry.io", "sentry-next.io",
    "png", "jpg", "jpeg", "gif", "svg",
}

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    )
}
TIMEOUT = 8


def _clean_emails(raw: set[str]) -> list[str]:
    """노이즈 이메일 필터링 후 정렬"""
    cleaned = []
    for email in raw:
        domain = email.split("@")[-1].lower()
        if any(ex in domain for ex in EXCLUDE_DOMAINS):
            continue
        if len(email) > 80:
            continue
        cleaned.append(email.lower())
    return sorted(set(cleaned))


def _extract_from_html(html: str) -> set[str]:
    """HTML 텍스트 전체에서 이메일 추출 (mailto: + 텍스트 모두)"""
    return set(EMAIL_PATTERN.findall(html))


def _get_contact_page_url(base_url: str, soup: BeautifulSoup) -> str | None:
    """홈페이지에서 '연락처', '문의', 'Contact' 링크 탐색"""
    contact_keywords = ["contact", "문의", "연락", "about", "회사소개", "오시는길"]
    for a in soup.find_all("a", href=True):
        text = (a.get_text() + a["href"]).lower()
        if any(kw in text for kw in contact_keywords):
            href = urljoin(base_url, a["href"])
            # 외부 링크 제외
            if urlparse(href).netloc == urlparse(base_url).netloc:
                return href
    return None


def extract_emails_from_website(url: str) -> list[str]:
    """
    웹사이트 URL에서 이메일 추출.
    1) 홈페이지 스캔
    2) 연락처 페이지가 있으면 추가 스캔
    """
    if not url:
        return []

    if not url.startswith("http"):
        url = "https://" + url

    found = set()

    try:
        # 1) 홈페이지
        resp = requests.get(url, headers=HEADERS, timeout=TIMEOUT)
        resp.encoding = resp.apparent_encoding
        found |= _extract_from_html(resp.text)

        soup = BeautifulSoup(resp.text, "html.parser")

        # 2) mailto: 링크 별도 수집
        for a in soup.find_all("a", href=True):
            if a["href"].startswith("mailto:"):
                email = a["href"].replace("mailto:", "").split("?")[0].strip()
                if email:
                    found.add(email)

        # 3) 연락처 페이지 추가 탐색
        contact_url = _get_contact_page_url(url, soup)
        if contact_url and contact_url != url:
            try:
                cresp = requests.get(contact_url, headers=HEADERS, timeout=TIMEOUT)
                cresp.encoding = cresp.apparent_encoding
                found |= _extract_from_html(cresp.text)
                csoup = BeautifulSoup(cresp.text, "html.parser")
                for a in csoup.find_all("a", href=True):
                    if a["href"].startswith("mailto:"):
                        email = a["href"].replace("mailto:", "").split("?")[0].strip()
                        if email:
                            found.add(email)
            except Exception:
                pass

    except requests.exceptions.SSLError:
        # HTTPS 실패 시 HTTP 재시도
        try:
            http_url = url.replace("https://", "http://")
            resp = requests.get(http_url, headers=HEADERS, timeout=TIMEOUT)
            resp.encoding = resp.apparent_encoding
            found |= _extract_from_html(resp.text)
        except Exception:
            pass
    except Exception:
        pass

    return _clean_emails(found)


def search_email_via_ddg(company_name: str) -> list[str]:
    """
    DuckDuckGo 무료 검색으로 업체 이메일 보조 탐색.
    API 키 불필요, 완전 무료.
    웹사이트 스캔으로 못 찾은 경우 폴백으로 사용.
    """
    if not _DDG_AVAILABLE:
        return []

    query = f'"{company_name}" 이메일 OR email'
    try:
        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=5))
        found = set()
        for r in results:
            text = r.get("title", "") + " " + r.get("body", "")
            found |= set(EMAIL_PATTERN.findall(text))
        return _clean_emails(found)
    except Exception:
        return []


def pick_best_email(emails: list[str]) -> str:
    """
    여러 이메일 중 가장 적합한 대표 이메일 선택.
    우선순위: info@ > contact@ > admin@ > 나머지
    """
    priority = ["info", "contact", "admin", "bim", "design", "office"]
    for prefix in priority:
        for email in emails:
            if email.startswith(prefix + "@"):
                return email
    return emails[0] if emails else ""
