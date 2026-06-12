#!/usr/bin/env python3
"""BIMobject 패밀리 크롤러 — 소분류 단위 전량 수집

전략:
  - 315개 전체 카테고리 트리를 파악
  - 대분류(16개) 하위 소분류(leaf) 단위로 개별 수집
  - 각 소분류 < 9,000개면 전량, >= 9,000개면 API 캡까지
  - 제품 ID 기준 중복 제거
  - Obsidian: 대분류 폴더 → 소분류 노트 계층형 저장

실행:
    python3 scripts/crawl_bimobject.py                  # 전체 수집
    python3 scripts/crawl_bimobject.py --category hvac  # 특정 대분류만
    python3 scripts/crawl_bimobject.py --dry-run        # 수집 계획만 출력
"""

from __future__ import annotations

import sys
import argparse
import json
import logging
import time
from datetime import datetime
from pathlib import Path

import urllib.request
import urllib.parse
import urllib.error

# ────────────────────────── 경로 ──────────────────────────────────
PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))
from backend.core.paths import AGENT_KB_DIR, BIMOBJECT_DIR  # noqa: E402

DATA_DIR     = BIMOBJECT_DIR
VAULT_DIR    = PROJECT_ROOT / "obsidian_vaults" / "lua_bim_lab_global_map" / "NAS_Knowledge" / "BIMobject"
KB_DIR       = AGENT_KB_DIR

DATA_DIR.mkdir(parents=True, exist_ok=True)
VAULT_DIR.mkdir(parents=True, exist_ok=True)

API_BASE       = "https://www.bimobject.com/proxy/search-api-2/v1"
PRODUCT_BASE   = "https://www.bimobject.com/ko"
REVIT_UUID     = "85ea1736-77c4-4c22-88e9-fb83788fc64a"
API_CAP        = 9_000   # Elasticsearch 기본 캡 판단 기준

HEADERS = {
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "ko-KR,ko;q=0.9",
    "Referer": "https://www.bimobject.com/ko/search",
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
    ),
    "Origin": "https://www.bimobject.com",
}

# ──────────────── 수집 대상 대분류 16개 (API 실제 코드) ────────────
TARGET_PARENTS = [
    "hvac",
    "plumbing",
    "sanitary",
    "fire-products",
    "electrical",
    "lighting",
    "construction",
    "doors",
    "windows",
    "walls",
    "flooring",
    "building-materials",
    "furniture",
    "landscaping",
    "electronics",
    "engineering",
]

# 한국어 이름 + 아이콘
CAT_KO: dict[str, tuple[str, str]] = {
    "hvac":               ("공조(HVAC)",      "🌡️"),
    "plumbing":           ("배관",            "🔧"),
    "sanitary":           ("위생",            "🚿"),
    "fire-products":      ("소방",            "🔥"),
    "electrical":         ("전기",            "⚡"),
    "lighting":           ("조명",            "💡"),
    "construction":       ("건축_구조",        "🏗️"),
    "doors":              ("문",              "🚪"),
    "windows":            ("창호",            "🪟"),
    "walls":              ("벽체",            "🧱"),
    "flooring":           ("바닥재",          "📐"),
    "building-materials": ("건축자재",        "🪵"),
    "furniture":          ("가구",            "🛋️"),
    "landscaping":        ("외부_조경",        "🌳"),
    "electronics":        ("전자_통신_보안",   "📡"),
    "engineering":        ("엔지니어링_인프라", "🛣️"),
    # 소분류 한국어 (API name 폴백으로도 동작)
    "sanitary-taps-mixers":      ("수도꼭지",     "🚰"),
    "sanitary-accessories1":     ("욕실소품",     "🧴"),
    "showers":                   ("샤워실",       "🚿"),
    "wash-basins":               ("세면기",       "🪣"),
    "toilets":                   ("대변기",       "🚽"),
    "urinals":                   ("소변기",       "🚽"),
    "sanitary-bath-spas":        ("욕조_스파",    "🛁"),
    "sanitary-bidets":           ("비데",         "🚿"),
    "air-conditioning":          ("공기조화",     "❄️"),
    "ductwork":                  ("덕트설비",     "💨"),
    "hvac-mech":                 ("기계환기",     "🌀"),
    "boilers":                   ("보일러",       "🔥"),
    "chillers":                  ("냉각기",       "❄️"),
    "heat-pumps":                ("열펌프",       "♨️"),
    "drainage":                  ("배수",         "🔽"),
    "valves":                    ("밸브",         "🔩"),
    "plumbing-pumps":            ("펌프",         "⚙️"),
    "pipes":                     ("파이프",       "🔧"),
    "fire-protection":           ("화재예방",     "🔥"),
    "sprinkler-systems":         ("스프링클러",   "💦"),
    "smoke-ventilation":         ("연기환기",     "💨"),
    "distribution":              ("배전",         "⚡"),
    "ceiling-mounted":           ("천장등",       "💡"),
    "wall-mounted-lighting":     ("벽부등",       "💡"),
    "outside-lighting":          ("외부조명",     "🔦"),
    "door-sets":                 ("문세트",       "🚪"),
    "sliding-doors":             ("미닫이문",     "🚪"),
    "fire-doors-shutters":       ("방화문",       "🔥"),
    "roof-windows":              ("지붕창",       "🪟"),
    "curtain-walls":             ("커튼월",       "🏙️"),
    "roof":                      ("지붕",         "🏠"),
    "ceilings":                  ("천장",         "📐"),
    "stairs":                    ("계단",         "🪜"),
    "lifts":                     ("엘리베이터",   "🛗"),
    "railing":                   ("난간",         "🪜"),
    "tiles":                     ("타일",         "🔲"),
    "insulation":                ("단열재",       "🧱"),
    "wood-flooring":             ("목재바닥",     "🪵"),
    "shelving-storage":          ("선반보관",     "📦"),
    "chairs-stools-benches":     ("의자스툴",     "🪑"),
    "tables":                    ("테이블",       "🪑"),
    "outdoor-furniture":         ("야외가구",     "🌳"),
    "networking":                ("네트워킹",     "📡"),
    "security-cameras-accessories": ("보안카메라", "📹"),
    "road":                      ("도로",         "🛣️"),
}

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S",
)
log = logging.getLogger(__name__)


# ──────────────────────────── API 유틸 ────────────────────────────
def _get(url: str, retries: int = 3) -> dict | None:
    for attempt in range(retries):
        try:
            req = urllib.request.Request(url, headers=HEADERS)
            with urllib.request.urlopen(req, timeout=20) as resp:
                return json.loads(resp.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            log.warning(f"HTTP {e.code}: {url[:80]} (시도 {attempt+1})")
            if e.code in (403, 429):
                time.sleep(5 * (attempt + 1))
        except Exception as e:
            log.warning(f"오류: {e} (시도 {attempt+1})")
            time.sleep(2)
    return None


# ──────────────────── 카테고리 트리 수집 ─────────────────────────
def fetch_category_tree() -> dict[str, dict]:
    """전체 카테고리 315개를 트리로 수집
    반환: code → {name, ko_name, icon, uid, n_products, parent, children}
    """
    url = f"{API_BASE}/products/filters/categories?_locale=ko&page=1&pageSize=200&sort=downloads"
    data = _get(url)
    if not data:
        log.error("카테고리 API 실패")
        return {}

    tree: dict[str, dict] = {}

    def _walk(cats: list, parent: str = "") -> None:
        for c in cats:
            code = c.get("code", "")
            if not code:
                continue
            children_raw = c.get("children", [])
            ko_name, icon = CAT_KO.get(code, (c.get("name", code), "📦"))
            tree[code] = {
                "code":       code,
                "name":       c.get("name", ""),
                "ko_name":    ko_name,
                "icon":       icon,
                "uid":        c.get("uniqueIdentifier", ""),
                "n_products": c.get("numberOfProducts", 0),
                "parent":     parent,
                "children":   [ch["code"] for ch in children_raw if ch.get("code")],
            }
            _walk(children_raw, code)

    _walk(data.get("data", []))
    log.info(f"카테고리 트리: {len(tree)}개")
    return tree


def _safe_filename(name: str) -> str:
    """파일명에 사용할 수 없는 문자 제거"""
    for ch in r'/\:*?"<>|':
        name = name.replace(ch, "_")
    return name.strip("_ ")


# ──────────────────── 단일 카테고리 제품 수집 ────────────────────
def fetch_all_products(cat: dict) -> list[dict]:
    """소분류 하나의 Revit 패밀리 전량 수집"""
    uid  = cat["uid"]
    code = cat["code"]
    if not uid:
        return []

    products: list[dict] = []
    page = 1
    total_pages = 1

    while page <= total_pages:
        params = urllib.parse.urlencode({
            "_locale": "ko",
            "category.uniqueidentifiers": uid,
            "filetype.uniqueidentifiers": REVIT_UUID,
            "page": page,
            "pageSize": 42,
            "sort": "downloads",
        })
        data = _get(f"{API_BASE}/products?{params}")
        if not data:
            break

        meta        = data.get("meta", {})
        total_pages = meta.get("totalPages", 1)
        items       = data.get("data", [])

        for item in items:
            brand          = item.get("brand", {}) or {}
            brand_name     = brand.get("name", "")
            brand_link     = brand.get("permalink", "")
            permalink      = item.get("permalink", "")
            product_url    = (
                f"{PRODUCT_BASE}/{brand_link}/{permalink}"
                if brand_link and permalink else ""
            )
            products.append({
                "id":       item.get("id", ""),
                "name":     item.get("name", ""),
                "brand":    brand_name,
                "url":      product_url,
                "rating":   item.get("rating"),
                "cat_code": code,
            })

        log.info(
            f"    {code} p{page}/{total_pages}: "
            f"+{len(items)}개 (누적 {len(products):,})"
        )
        page += 1
        time.sleep(0.4)

    return products


# ──────────────────── 메인 크롤러 ─────────────────────────────────
class BIMObjectCrawler:
    """대분류 → 소분류 단위 수집, 제품 ID 중복 제거"""

    def __init__(self) -> None:
        self.tree:    dict[str, dict]          = {}
        # parent_code → {sub_code → [products]}
        self.results: dict[str, dict[str, list[dict]]] = {}
        self._seen:   set[str]                 = set()

    # ── 소분류 하나 수집 (중복 제거 포함) ──
    def _collect_sub(self, sub_code: str) -> list[dict]:
        cat = self.tree.get(sub_code)
        if not cat:
            return []
        raw      = fetch_all_products(cat)
        unique   = []
        for p in raw:
            pid = p.get("id", "")
            if pid and pid not in self._seen:
                self._seen.add(pid)
                unique.append(p)
        return unique

    # ── 대분류 하나 수집: 소분류 있으면 드릴다운 ──
    def _collect_parent(self, parent_code: str) -> dict[str, list[dict]]:
        cat      = self.tree.get(parent_code, {})
        n        = cat.get("n_products", 0)
        children = cat.get("children", [])
        ko_name  = cat.get("ko_name", parent_code)

        log.info(f"{'─'*55}")
        log.info(f"[{ko_name}] 총 {n:,}개 | 소분류 {len(children)}개")

        sub_results: dict[str, list[dict]] = {}

        if children:
            # 소분류별 개별 수집
            for sub_code in children:
                sub = self.tree.get(sub_code, {})
                sub_n  = sub.get("n_products", 0)
                sub_ko = sub.get("ko_name", sub_code)
                grandchildren = sub.get("children", [])

                log.info(f"  └ [{sub_ko}] {sub_n:,}개")

                if sub_n > API_CAP and grandchildren:
                    # 손자 분류까지 드릴다운
                    log.info(f"      → 손자분류 {len(grandchildren)}개로 분할")
                    merged: list[dict] = []
                    for gc_code in grandchildren:
                        gc     = self.tree.get(gc_code, {})
                        gc_ko  = gc.get("ko_name", gc_code)
                        gc_n   = gc.get("n_products", 0)
                        log.info(f"      └─ [{gc_ko}] {gc_n:,}개")
                        merged.extend(self._collect_sub(gc_code))
                        time.sleep(0.3)
                    sub_results[sub_code] = merged
                else:
                    sub_results[sub_code] = self._collect_sub(sub_code)

                log.info(
                    f"    완료: {sub_ko} → {len(sub_results[sub_code]):,}개"
                )
                time.sleep(0.5)
        else:
            # 소분류 없는 대분류: 직접 수집
            sub_results[parent_code] = self._collect_sub(parent_code)

        total = sum(len(v) for v in sub_results.values())
        log.info(f"[{ko_name}] 소계: {total:,}개")
        return sub_results

    def run(self, target_parents: list[str] | None = None) -> None:
        log.info("카테고리 트리 수집 중...")
        self.tree = fetch_category_tree()

        targets = target_parents or TARGET_PARENTS
        for code in targets:
            if code not in self.tree:
                log.warning(f"카테고리 없음: {code}")
                continue
            self.results[code] = self._collect_parent(code)
            time.sleep(1)

    def flat_products(self) -> list[dict]:
        """전체 제품 단일 리스트"""
        out = []
        for subs in self.results.values():
            for prods in subs.values():
                out.extend(prods)
        return out


# ──────────────────── JSON 저장 ───────────────────────────────────
def save_json(crawler: BIMObjectCrawler) -> Path:
    flat  = crawler.flat_products()
    stamp = datetime.now().strftime("%Y%m%d_%H%M")
    payload = {
        "updated_at":    datetime.now().isoformat(),
        "source":        "https://www.bimobject.com/ko",
        "total_products": len(flat),
        "categories": {
            parent: {sub: prods for sub, prods in subs.items()}
            for parent, subs in crawler.results.items()
        },
    }
    ts_path     = DATA_DIR / f"bimobject_{stamp}.json"
    latest_path = DATA_DIR / "bimobject_latest.json"
    ts_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    latest_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    log.info(f"JSON 저장: {ts_path} ({len(flat):,}개)")
    return ts_path


# ──────────────────── Obsidian 노트 생성 ──────────────────────────
def _cat_ko_name(tree: dict, code: str) -> tuple[str, str]:
    """트리 또는 CAT_KO에서 한국어 이름과 아이콘 반환"""
    if code in tree:
        return tree[code].get("ko_name", code), tree[code].get("icon", "📦")
    if code in CAT_KO:
        return CAT_KO[code]
    return code, "📦"


def generate_obsidian(crawler: BIMObjectCrawler) -> None:
    updated = datetime.now().strftime("%Y-%m-%d %H:%M")
    tree    = crawler.tree

    for parent_code, subs in crawler.results.items():
        p_ko, p_icon = _cat_ko_name(tree, parent_code)
        p_total = sum(len(v) for v in subs.values())

        # 대분류별 폴더
        folder = VAULT_DIR / _safe_filename(p_ko)
        folder.mkdir(parents=True, exist_ok=True)

        # 소분류별 노트
        for sub_code, products in subs.items():
            s_ko, s_icon = _cat_ko_name(tree, sub_code)

            lines = [
                "---",
                f"tags: [BIMobject, 패밀리, {p_ko}, {s_ko}]",
                f"updated: {updated}",
                f"source: https://www.bimobject.com/ko/search?categories={sub_code}&software=revit",
                "---",
                "",
                f"# {s_icon} {s_ko} 패밀리",
                f"_상위: {p_icon} {p_ko}_",
                "",
                f"> **{len(products):,}개** Revit 패밀리 | 업데이트: {updated}",
                f"> 🔗 [BIMobject에서 검색](https://www.bimobject.com/ko/search?categories={sub_code}&software=revit&sort=downloads)",
                "",
                "## 패밀리 목록",
                "",
            ]

            if products:
                lines += ["| # | 제품명 | 제조사 | 링크 |", "|---|--------|--------|------|"]
                for i, p in enumerate(products, 1):
                    nm  = p.get("name", "").replace("|", "\\|")
                    br  = p.get("brand", "").replace("|", "\\|")
                    url = p.get("url", "")
                    lnk = f"[↗]({url})" if url else "-"
                    lines.append(f"| {i} | {nm} | {br} | {lnk} |")
            else:
                lines.append("_수집된 패밀리 없음_")

            lines += [
                "",
                "## 관련",
                f"- [[MOC - BIMobject {p_ko}]]",
                "- [[MOC - BIMobject 패밀리 가이드]]",
            ]

            note = folder / f"{_safe_filename(s_ko)} 패밀리.md"
            note.write_text("\n".join(lines), encoding="utf-8")

        # 대분류 MOC
        moc_lines = [
            "---",
            f"tags: [MOC, BIMobject, {p_ko}]",
            f"updated: {updated}",
            "---",
            "",
            f"# {p_icon} MOC — BIMobject {p_ko}",
            "",
            f"> 소계: **{p_total:,}개** | 소분류 **{len(subs)}개** | 업데이트: {updated}",
            "",
            "## 소분류 노트",
            "",
        ]
        for sub_code, products in subs.items():
            scat   = tree.get(sub_code, {})
            s_ko   = scat.get("ko_name", sub_code)
            s_icon = scat.get("icon", "📦")
            moc_lines.append(f"- {s_icon} [[{s_ko} 패밀리]] — {len(products):,}개")

        moc_lines += [
            "",
            "## 관련",
            "- [[MOC - BIMobject 패밀리 가이드]]",
        ]
        moc_note = folder / f"MOC - BIMobject {_safe_filename(p_ko)}.md"
        moc_note.write_text("\n".join(moc_lines), encoding="utf-8")
        log.info(f"  Obsidian 폴더: {p_ko}/ ({len(subs)}개 소분류 노트)")

    # 전체 최상위 MOC
    _generate_top_moc(crawler, updated)
    # KB 인덱스
    _generate_kb(crawler, updated)


def _generate_top_moc(crawler: BIMObjectCrawler, updated: str) -> None:
    flat  = crawler.flat_products()
    tree  = crawler.tree
    lines = [
        "---",
        "tags: [MOC, BIMobject, 패밀리라이브러리]",
        f"updated: {updated}",
        "---",
        "",
        "# 📚 MOC — BIMobject 패밀리 가이드",
        "",
        f"> 총 **{len(flat):,}개** Revit 패밀리 | 업데이트: {updated}",
        "",
        "## 대분류 → 소분류 인덱스",
        "",
    ]
    for parent_code, subs in crawler.results.items():
        pcat   = tree.get(parent_code, {})
        p_ko   = pcat.get("ko_name", parent_code)
        p_icon = pcat.get("icon", "📦")
        total  = sum(len(v) for v in subs.values())
        lines.append(f"### {p_icon} [[MOC - BIMobject {p_ko}|{p_ko}]] — {total:,}개")
        for sub_code, products in subs.items():
            scat   = tree.get(sub_code, {})
            s_ko   = scat.get("ko_name", sub_code)
            s_icon = scat.get("icon", "📦")
            lines.append(f"- {s_icon} [[{s_ko} 패밀리]] — {len(products):,}개")
        lines.append("")

    moc = VAULT_DIR / "MOC - BIMobject 패밀리 가이드.md"
    moc.write_text("\n".join(lines), encoding="utf-8")
    log.info(f"최상위 MOC: {moc.name}")


def _generate_kb(crawler: BIMObjectCrawler, updated: str) -> None:
    flat  = crawler.flat_products()
    tree  = crawler.tree
    lines = [
        "# BIMobject 패밀리 라이브러리 인덱스",
        "",
        f"> 자동 업데이트: {updated} | 총 {len(flat):,}개 (소분류 드릴다운, 중복 제거)",
        "",
    ]
    for parent_code, subs in crawler.results.items():
        pcat   = tree.get(parent_code, {})
        p_ko   = pcat.get("ko_name", parent_code)
        p_icon = pcat.get("icon", "📦")
        total  = sum(len(v) for v in subs.values())
        lines += [f"## {p_icon} {p_ko} ({total:,}개)", ""]
        for sub_code, products in subs.items():
            scat  = tree.get(sub_code, {})
            s_ko  = scat.get("ko_name", sub_code)
            lines.append(f"### {s_ko} ({len(products):,}개)")
            for p in products[:15]:
                nm  = p.get("name", "")
                br  = p.get("brand", "")
                url = p.get("url", "")
                br_str  = f" _{br}_" if br else ""
                lnk_str = f" ([↗]({url}))" if url else ""
                lines.append(f"- **{nm}**{br_str}{lnk_str}")
            if len(products) > 15:
                lines.append(f"- _... 외 {len(products)-15:,}개_")
            lines.append("")

    path = KB_DIR / "BIMobject_패밀리_인덱스.md"
    path.write_text("\n".join(lines), encoding="utf-8")
    log.info(f"KB 인덱스: {path.name}")


# ──────────────────── 수집 계획 출력 (dry-run) ────────────────────
def dry_run(tree: dict[str, dict]) -> None:
    log.info("=== 수집 계획 (dry-run) ===")
    grand_total = 0
    for parent_code in TARGET_PARENTS:
        pcat     = tree.get(parent_code, {})
        p_ko     = pcat.get("ko_name", parent_code)
        n        = pcat.get("n_products", 0)
        children = pcat.get("children", [])
        log.info(f"\n{p_ko} ({n:,}개) → 소분류 {len(children)}개")
        for sub_code in children:
            sub   = tree.get(sub_code, {})
            sub_n = sub.get("n_products", 0)
            sub_ko= sub.get("ko_name", sub_code)
            flag  = " ⚠️캡초과" if sub_n >= API_CAP else ""
            log.info(f"  └ {sub_ko}: {sub_n:,}개{flag}")
            grand_total += sub_n
    log.info(f"\n총 예상 수집: ~{grand_total:,}개")


# ──────────────────── 메인 ────────────────────────────────────────
def main() -> None:
    parser = argparse.ArgumentParser(description="BIMobject 소분류 드릴다운 크롤러")
    parser.add_argument("--category", nargs="+", help="대분류 코드 (예: sanitary hvac)")
    parser.add_argument("--dry-run",  action="store_true", help="수집 계획만 출력")
    parser.add_argument("--json-only",action="store_true", help="JSON만 저장")
    args = parser.parse_args()

    log.info("=" * 60)
    log.info("BIMobject 크롤러 — 소분류 단위 전량 수집")
    log.info(f"  캡 기준: {API_CAP:,}개 초과 시 소분류 드릴다운")
    log.info("=" * 60)

    tree = fetch_category_tree()

    if args.dry_run:
        dry_run(tree)
        return

    crawler = BIMObjectCrawler()
    crawler.tree = tree
    targets = args.category or TARGET_PARENTS
    for code in targets:
        if code not in tree:
            log.warning(f"카테고리 없음: {code}")
            continue
        crawler.results[code] = crawler._collect_parent(code)
        time.sleep(1)

    ts_path = save_json(crawler)

    if not args.json_only:
        generate_obsidian(crawler)

    flat = crawler.flat_products()
    log.info("=" * 60)
    log.info(f"완료: 총 {len(flat):,}개 Revit 패밀리 (중복 제거)")
    log.info(f"JSON:    {ts_path}")
    log.info(f"Obsidian: {VAULT_DIR}")
    log.info("=" * 60)


if __name__ == "__main__":
    main()
