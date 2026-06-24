"""
SECTION 4 ── 지식 베이스 검색 · 점수화 · 답변 생성
  - knowledge_search_files, query_terms, score_knowledge_text
  - extract_relevant_excerpt, search_local_knowledge
  - infer_knowledge_agent_from_query, build_combined_answer
  - assess_knowledge_answer_quality, auto_supplement_knowledge_gap
  - append_auto_knowledge_gap_log, build_more_research_answer
  - count_gap_occurrences, get_persistent_gaps
  ※ 운영 제외 파일: _EXCLUDED_KNOWLEDGE_STEMS
"""
from __future__ import annotations

import bisect
import datetime
import json
import os
import re
from collections import Counter
from pathlib import Path

from backend.core.paths import (
    AGENT_KB_DIR as _AGENT_KB_DIR,
    CATALOG_DIR as _CATALOG_DIR,
    CURATION_DIR as _CURATION_DIR,
    DOCS_DIR as _DOCS_DIR,
    OBSIDIAN_VAULTS_DIR as _OBSIDIAN_VAULTS_DIR,
    PROJECT_ROOT as _PROJECT_ROOT,
    QA_KB_DIR as _QA_KB_DIR,
)
from backend import agent_registry as _registry
from backend.knowledge_store import ORGANIZATION as _ORGANIZATION
from backend.knowledge_store import safe_agent_stem as _safe_agent_stem
from backend.web_search import _search_web_for_knowledge

_AGENT_TO_TEAM = {
    agent: team for team, agents in _ORGANIZATION.items() for agent in agents
}

# ---------------------------------------------------------------------------
# 운영 파일 제외 목록 (지식 검색 대상에서 제외)
# ---------------------------------------------------------------------------
_EXCLUDED_KNOWLEDGE_STEMS = {
    "지식업데이트md", "지식큐레이터md",
}

# 로컬 답변을 confident 하게 서빙할 최소 매치 점수. 측정 결과 off-topic/thin 노이즈
# 매치는 18~27, 정당한 답변은 36+ 로 갈리므로 그 사이(32)를 임계로 둔다. 이보다 낮으면
# 약매칭으로 보고 웹보강(needs_more_research)·웹실패 시 graceful '찾지 못함'으로 처리한다.
_WEAK_LOCAL_SCORE = 32

def _st():
    """server_total 지연 임포트 헬퍼 — 순환 참조 방지."""
    import backend.server_total as _mod
    return _mod


# ---------------------------------------------------------------------------
# 지식 카탈로그 (scripts/build_knowledge_catalog.py 가 매일 생성)
#   - 키워드 역색인으로 후보 파일을 줄여 전체 read_text 풀스캔을 회피한다.
#   - 카탈로그가 없거나 손상되면 기존 풀스캔으로 폴백한다.
# ---------------------------------------------------------------------------
_FILE_MAP_PATH = _CATALOG_DIR / "FILE_MAP.json"
_catalog_state: dict = {"mtime": None, "data": None, "tokens": []}


def _load_catalog() -> dict | None:
    try:
        mtime = _FILE_MAP_PATH.stat().st_mtime
    except OSError:
        return None
    if _catalog_state["mtime"] != mtime:
        try:
            data = json.loads(_FILE_MAP_PATH.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            return None
        _catalog_state["mtime"] = mtime
        _catalog_state["data"] = data
        _catalog_state["tokens"] = sorted(data.get("keyword_to_files", {}))
    return _catalog_state["data"]


def _catalog_candidates(catalog: dict, terms: list[str]) -> tuple[set[str], set[str]]:
    """(후보 rel 경로, 카탈로그가 아는 전체 rel 경로) 반환.

    매칭은 정확 일치 + 접두 일치(한국어 조사/어미 대응). 후보가 비면 호출부가
    풀스캔으로 폴백한다.
    """
    keyword_map = catalog.get("keyword_to_files") or {}
    tokens = _catalog_state["tokens"]
    files = catalog.get("files") or []
    indices: set[int] = set()
    for term in terms:
        for hit in keyword_map.get(term, ()):
            indices.add(hit)
        pos = bisect.bisect_left(tokens, term)
        while pos < len(tokens) and tokens[pos].startswith(term):
            indices.update(keyword_map[tokens[pos]])
            pos += 1
    candidates = {files[i]["path"] for i in indices if i < len(files)}
    known = {meta["path"] for meta in files}
    return candidates, known


def _catalog_team_lookup(catalog: dict) -> dict[str, str]:
    return {meta["path"]: meta.get("team", "") for meta in catalog.get("files") or []}


def _catalog_domain_lookup(catalog: dict) -> dict[str, str]:
    return {meta["path"]: meta.get("domain", "") for meta in catalog.get("files") or []}


def _catalog_agent_domain(catalog: dict, agent: str) -> str:
    """추론된 에이전트의 KB 파일 도메인 — 쿼리의 도메인 축 추정에 사용."""
    rel = (catalog.get("agent_to_file") or {}).get(agent, "")
    if not rel:
        return ""
    for meta in catalog.get("files") or []:
        if meta["path"] == rel:
            return meta.get("domain", "")
    return ""


def knowledge_search_files() -> list[Path]:
    roots = [
        _AGENT_KB_DIR,
        _QA_KB_DIR,
        _DOCS_DIR,
        _OBSIDIAN_VAULTS_DIR / "model_quality_auditor",
    ]
    excluded_parts = {
        "knowledge_updates",
        "knowledge_intake",
        "Team_Telegram_QA",
        "Revit_Assistant_QA",
        "__pycache__",
        # 내부 운영/메타 로그 — 도메인 Q&A 의 답이 아니다. 저신호 질의를 흔한 토큰으로
        # 가로채는 노이즈원이라 검색셋에서 제외한다(REASONING_TRAINING_DIGEST,
        # INTERNAL_SELF_GROWTH_PULSE 류 ~60개 파일).
        "reasoning_training",
        "internal_growth",
        # AI 협업 프로세스 테스트/로그(AITEST_*, TEST_ROUND_*, 에스컬레이션 추적 등).
        # BIM 간섭해결 지식이 아니라 조직 운영 산출물이며 도메인 질의를 하이재킹한다.
        # (실제 BIM 간섭 지식은 간섭검토.md 가 담당)
        "conflict_resolution",
    }
    files: list[Path] = []
    for root in roots:
        if root.exists():
            files.extend(
                path for path in root.rglob("*.md")
                if path.is_file()
                and not any(part in excluded_parts for part in path.parts)
                and path.stem not in _EXCLUDED_KNOWLEDGE_STEMS
            )
    return files


def query_terms(query: str) -> list[str]:
    raw_terms = re.findall(r"[A-Za-z0-9_#+.\-가-힣]{2,}", query.lower())
    # 부정/제외: 'X 말고/빼고/제외하고 Y' 에서 제외 대상 X 를 검색어에서 뺀다. 그래야
    # '스프링클러 말고 다른 소화설비'가 스프링클러 콘텐츠를 답으로 내지 않는다.
    _EXCLUDE_MARKERS = {"말고", "빼고", "제외하고", "외에", "말고요"}
    if any(m in raw_terms for m in _EXCLUDE_MARKERS):
        pruned = []
        for i, t in enumerate(raw_terms):
            nxt = raw_terms[i + 1] if i + 1 < len(raw_terms) else ""
            if nxt in _EXCLUDE_MARKERS:
                continue  # 제외 마커 바로 앞 용어는 제거
            pruned.append(t)
        raw_terms = pruned
    stopwords = {
        "으로", "에서", "대한", "관련", "정리", "알려줘", "해주세요", "기준", "질문", "요청",
        "지식질문", "말고", "또", "뭐가", "있을까", "있는지", "종류", "유체",
        "하는", "하게", "확인해야", "기본", "답변을",
        "얼마야", "얼마예요", "얼마나", "얼마임", "알려줘", "뭐야", "뭐임", "무엇", "어떻게",
        "어떤", "있어", "있나요", "인가요", "인지", "할까", "해야", "돼요", "됩니까",
        # 거의 모든 KB 에 흔한 검수/일반 동사 — 저신호인데 검토형 에이전트(법무조항검토·
        # 간섭검토)를 magnet 으로 끌어당겨 도메인 질의를 가로챈다(예: '보 처짐 검토').
        "검토", "점검", "확인", "처리", "방법", "작성",
    }
    terms = []
    for term in raw_terms:
        if term in stopwords:
            continue
        normalized = term
        for suffix in ("이야", "이에요", "이다", "에서", "에는", "으로", "의", "가", "이", "을", "를", "은", "는", "야", "이랑", "도", "과", "와"):
            if normalized.endswith(suffix) and len(normalized) > len(suffix) + 1:
                normalized = normalized[: -len(suffix)]
                break
        if normalized and normalized not in stopwords:
            terms.append(normalized)
    # 아래 도메인 확장은 raw_terms 를 검사하는데, 조사 제거 후의 정규형('분전반의'→'분전반')도
    # 확장 트리거가 되도록 정규화된 terms 를 합쳐 둔다(이후 raw_terms 는 확장에서만 쓰임).
    raw_terms = list(raw_terms) + terms
    if any(term in raw_terms for term in ["cws", "cwr", "cw"]):
        terms.extend(["냉각수", "condenser", "water"])
    if any(term in raw_terms for term in ["chws", "chwr", "chw"]):
        terms.extend(["냉수", "chilled", "water"])
    if any(term in raw_terms for term in ["hws", "hwr", "hw"]):
        terms.extend(["온수", "난방", "hot", "water"])
    if any("hwr" in term or "급탕환수" in term for term in raw_terms):
        terms.extend(["급탕환수", "domestic hot water return", "순환", "온도", "레지오넬라"])
    # '통기'는 접두로만 인정한다. 부분문자열이면 '유통기획관'('유통기'+'획관')이
    # '통기'로 오매칭돼 위생 배수 확장이 주입된다(cycle4 부분문자열 클래스).
    if any(term.startswith("통기") or term.startswith("트랩") or term == "트랩" for term in raw_terms):
        terms.extend(["통기", "통기관", "트랩", "봉수", "오배수", "vent", "trap"])
    # HVAC 장비 약어(FCU/AHU)·한글명(팬코일/공조기)을 공조 계통 용어로 확장한다.
    # 콘텐츠는 공조배관/공조덕트 KB 에 있으나(팬코일/공조기/결로) 라우팅 키워드가 없어
    # 기본값으로 빠져 점수가 낮았다. 접두/단독 매칭으로 무관어 오매칭은 피한다.
    if any(t in ("fcu", "ahu", "공조기") or t.startswith("팬코일") for t in raw_terms):
        terms.extend(["공조", "팬코일", "공조기", "냉수", "온수", "응축수", "결로", "드레인", "외기", "급기"])
    # 댐퍼(방화/풍량/볼륨) — 공조덕트 KB 에 풍부(댐퍼 48·방화댐퍼 19). 라우팅 키워드가 없어
    # 'bare 댐퍼'가 default 로 빠졌다. 단 제진/내진 댐퍼는 구조(seismic)이므로 제외한다.
    if any(t.startswith("댐퍼") or "방화댐퍼" in t or "풍량댐퍼" in t for t in raw_terms) and not any(
        kw in query.lower() for kw in ["제진", "내진", "지진", "seismic"]
    ):
        terms.extend(["댐퍼", "공조덕트", "풍량", "방화댐퍼"])
    # 제연/배연/급기가압(smoke control) — 공조덕트 KB 에 풍부(제연 47회)하나 'bare 제연'이
    # 키워드가 아니라('제연덕트'만) 짧은 질의('제연설비 기준')가 default 로 빠졌다.
    if any(t.startswith("제연") or t.startswith("배연") or t.startswith("급기가압") for t in raw_terms):
        terms.extend(["제연", "공조덕트", "댐퍼", "급기", "배기", "풍량"])
    # 접지 — 전기 KB 에 풍부(43회). discipline 키워드로 substring 매칭하면 '직접지원'('직접지'
    # +'원')이 '접지'로 오매칭되므로(cycle4 클래스) startswith 확장으로만 처리한다.
    if any(t.startswith("접지") for t in raw_terms):
        terms.extend(["접지", "전기", "등전위", "본딩"])
    # 냉동기(chiller) — 공조배관 KB 에 풍부(21회). 라우팅 키워드가 없어 default 로 빠졌다.
    if any(t in ("chiller",) or t.startswith("냉동기") for t in raw_terms):
        terms.extend(["냉동기", "공조", "냉수", "냉각수", "chiller"])
    # 전기 배전 장비 약어(MCCB/ACB/ELCB/UPS) → 전기 차단기/분전반(전기 KB 차단기 16·UPS 6).
    if any(t in ("mccb", "acb", "elcb", "ups", "무정전") for t in raw_terms):
        terms.extend(["전기", "차단기", "분전반", "수전", "무정전"])
    if any("냉매" in term for term in raw_terms):
        terms.extend(["냉매", "refrigerant", "전기 트레이", "이격", "단열", "누설"])
    if any("팽창탱크" in term or "팽창" in term for term in raw_terms):
        terms.extend(["팽창탱크", "펌프", "흡입", "환수", "압력", "air vent"])
    if any(term in raw_terms for term in ["mdf", "idf", "cctv", "광케이블", "통신실", "약전"]):
        terms.extend(["mdf", "idf", "cctv", "광케이블", "통신", "약전", "emi", "이격"])
    if any(term in raw_terms for term in ["분전반", "수배전반", "큐비클"]):
        terms.extend(["분전반", "수배전반", "전면", "작업 공간"])
        # 누수/배관은 물·누수 맥락일 때만 — '분전반 작업공간' 질의가 '냉수배관 이격'
        # 섹션으로 끌려가지 않도록(작업공간 질문엔 배관 섹션이 답이 아니다).
        if any(term in raw_terms for term in ["누수", "침수", "배관", "물", "방수", "냉수"]):
            terms.extend(["누수", "배관"])
    if any(term in raw_terms for term in ["방화셔터", "제연팬", "감지기", "수신기", "방재"]):
        terms.extend(["방화셔터", "제연팬", "감지기", "수신기", "방재", "연동", "소방전기"])
    # '헤드'는 단독/접미(스프링클러헤드·살수헤드)로만 인정한다. 부분문자열이면
    # '헤드헌팅'(채용)·'헤드라인'(마케팅)·'헤드셋'이 소방 스프링클러로 오라우팅된다.
    if any(
        any(kw in term for kw in ["스프링클러", "스프링쿨러", "살수", "소화배관", "소방배관"])
        or term == "헤드" or term.endswith("헤드")
        for term in raw_terms
    ):
        # '스프링쿨러'는 '스프링클러'의 흔한 오타 → 정규형을 추가해 KB(스프링클러) 매칭
        terms.extend(["스프링클러", "헤드", "살수", "장애", "소방기계", "소화배관", "소방배관", "fire", "sprinkler"])
    if any(term in raw_terms for term in ["vav", "정압", "bms", "bas", "ddc"]):
        terms.extend(["vav", "정압", "센서", "팬", "인버터", "vfd", "최소풍량", "bms", "point list"])
    if any(term in raw_terms for term in ["navisworks", "나비스웍스", "클래시", "clash"]):
        terms.extend(["navisworks", "clash detective", "selection set", "search set", "rule", "공차", "bcf", "rfi", "간섭검토"])
    if "공조배관" in raw_terms:
        terms.extend(["냉수", "온수", "냉각수", "냉매", "증기", "응축수"])
    if any(term in raw_terms for term in ["위생배관", "위생"]):
        terms.extend(["급탕환수", "오배수", "통기", "우수", "sanitary", "vent", "storm"])
    # '트레이'는 접미 복합어(케이블트레이/통신트레이/전기트레이)나 단독어로만 인정한다.
    # 단순 부분문자열 매칭은 '오케스트레이터' 같은 무관 단어를 케이블트레이로 오인해
    # 전기 공종으로 오라우팅한다.
    if any(term == "트레이" or term.endswith("트레이") or "케이블" in term for term in raw_terms):
        terms.extend(["트레이", "케이블", "강전", "약전", "이격", "곡률", "충전율"])
    if any(term.startswith("revit") or "addin" in term or "add-in" in term for term in raw_terms):
        terms.extend(["revit", "addin", "add-in"])
        # assistant/knowledge-gateway/obsidian 은 LUA 제품 연동 용어다. 일반 Revit API
        # 질문(트랜잭션/패밀리 등)에까지 붙이면 'Revit Assistant 연동' 섹션이 본래
        # 주제를 가린다. 연동/어시스턴트 맥락일 때만 추가.
        if any(k in raw_terms for k in ["assistant", "어시스턴트", "luachat", "gateway", "게이트웨이", "obsidian", "옵시디언", "연동"]):
            terms.extend(["assistant", "knowledge-gateway", "obsidian"])
    if any(term in terms for term in ["다이나모", "dynamo"]):
        terms.extend(["dynamo", "다이나모", "categories", "all elements of category", "python",
                       "filteredelementcollector", "selection", "setelementids"])
    # 패밀리 '배치/로드' 의도일 때만 placement 용어 확장. bare '패밀리'(파라미터/공유 등)는
    # placement 가 아니므로 제외 — 안 그러면 '패밀리 파라미터 공유'가 배치 섹션으로 끌린다.
    if any(term in terms for term in ["폴더", "하위", "배치", "로드", "loadfamily", "rfa"]):
        terms.extend(["folder", "family", "loadfamily", "newfamilyinstance", "directory", "rfa",
                       "패밀리", "로드", "배치"])
    # 영문 BIM 용어 → 한글 동의어. 글로벌 제품(Autodesk Store) 영문 질의가 한글 KB 에
    # 매칭되도록 한다(기존 cws→냉각수 확장과 같은 패턴). 명확한 도메인 명사만 보수적으로.
    _EN_KO = {
        "fire": ["소방", "방화", "화재"], "sprinkler": ["스프링클러", "소방기계"],
        "rebar": ["철근", "배근"], "reinforcement": ["철근", "배근"],
        "duct": ["덕트"], "compartment": ["구획", "방화구획"], "penetration": ["관통"],
        "drainage": ["오배수", "배수"], "vent": ["통기"], "insulation": ["단열", "보온"],
        "panelboard": ["분전반"], "switchboard": ["수배전반", "분전반"],
        "structural": ["구조"], "architectural": ["건축"], "plumbing": ["위생"],
        "clearance": ["이격", "작업공간"], "clash": ["간섭", "간섭검토"],
        "cable": ["케이블", "트레이"], "tray": ["트레이", "케이블"],
        "hvac": ["공조", "공조배관", "공조덕트"], "telecom": ["통신", "약전"],
        # 소방 영문 명사(콘텐츠 존재·startswith·단일 도메인이라 오라우팅 없음). 전기 영문어
        # (grounding/conduit/transformer)는 '전기' 확장이 공조배관 '전기트레이'에 hijack
        # 되거나 부족해 backlog 로 둔다(영문 엔지니어링 = 웹 폴백, cycle38/99 결정).
        "hydrant": ["소화전", "옥내소화전"],
    }
    # 한글→영문(KB 헤딩/본문이 영문 기술용어를 쓰는 경우 — '트랜잭션' 질의가
    # 'Transaction 처리' 섹션을 찾도록). 접두매칭으로 무관 오매칭 방지.
    _KO_EN = {
        "트랜잭션": ["transaction"], "패밀리": ["family"], "파라미터": ["parameter"],
        "클래시": ["clash"], "다이나모": ["dynamo"], "스케줄": ["schedule"],
    }
    # 한글 변형/오타 → KB 정규형. 실사용자가 쓰는 흔한 변형을 KB 실제 표기로 매핑해
    # 매칭시킨다(모두 KB 콘텐츠 풍부·모호성 0인 것만). 예: 닥트→덕트, 디퓨져→디퓨저.
    _KO_VARIANTS = {
        "닥트": ["덕트"], "디퓨져": ["디퓨저"], "후렉시블": ["플렉시블"],
        "파라메터": ["파라미터"], "매개변수": ["파라미터", "parameter"],
        "발브": ["밸브"], "벨브": ["밸브"], "훼밀리": ["패밀리", "family"],
        "레빗": ["revit"], "분전판": ["분전반"], "커텐월": ["커튼월"], "방화구회": ["방화구획"],
        # 한글 음역 약어 → 영문 약어(KB 표기). 한국 고객이 'LOD' 대신 '엘오디',
        # 'IFC' 대신 '아이에프씨'로 흔히 타이핑하는데 KB는 영문 약어라 미스코어→웹검색.
        # 모두 distinctive(타 한국어 substring 아님)·콘텐츠 풍부한 것만.
        "엘오디": ["lod"], "아이에프씨": ["ifc"], "비아이엠": ["bim"],
    }
    for variant, canon in _KO_VARIANTS.items():
        if any(t.startswith(variant) for t in raw_terms):
            terms.extend(canon)
    for ko, ens in _KO_EN.items():
        if any(t.startswith(ko) for t in raw_terms):
            terms.extend(ens)
    for en, kos in _EN_KO.items():
        # 접두 매칭(복수형 ducts/pipes 허용)하되 부분문자열은 금지한다.
        # 'duct' in 'product', 'vent' in 'event' 같은 무관 오매칭을 막는다(cycle4 클래스).
        if any(t.startswith(en) for t in raw_terms):
            terms.extend(kos)
    return list(dict.fromkeys(terms))[:20]


def score_knowledge_text(text: str, terms: list[str]) -> int:
    lower = text.lower()
    score = 0
    for term in terms:
        hits = lower.count(term)
        if hits:
            score += min(hits, 6)
    return score


def _clean_truncate(text: str, limit: int) -> str:
    """max_chars 하드컷이 문장/단어 중간을 자르지 않게 가장 가까운 경계에서 자른다.

    줄바꿈 > 문장종결(.·다·요·음) 순으로 경계를 찾고, 너무 많이 깎이면(<60%)
    그냥 자르고 말줄임표를 붙인다. 고객 답변이 '관경(' 처럼 끊기는 걸 막는다."""
    text = text.strip()
    if len(text) <= limit:
        return text
    window = text[:limit]
    boundary = max(
        window.rfind("\n"),
        window.rfind(". "), window.rfind(".\n"),
        window.rfind("다. "), window.rfind("요. "), window.rfind("음. "),
        window.rfind("다.\n"), window.rfind("요.\n"),
    )
    if boundary < int(limit * 0.6):
        # 종결 부호가 없으면 한국어 종결어미 단독으로라도 경계를 잡는다.
        for ender in ("다", "요", "음", "권장", "확인", "필요"):
            boundary = max(boundary, window.rfind(ender + "\n"), window.rfind(ender + " "))
    if boundary >= int(limit * 0.6):
        return window[: boundary + 1].strip()
    return window.strip() + "…"


def _section_body_chars(section: str) -> int:
    """섹션의 실질 본문 길이(헤딩·Source/Tags 메타·---·빈줄 제외). 배너 헤딩
    (예: '## X BIM 마스터급 경험 지식' + Source + ---, 본문은 다음 ## 섹션) 감지용."""
    body = []
    for line in section.split("\n")[1:]:  # 첫 줄(헤딩) 제외
        s = line.strip()
        if not s or s == "---" or s.startswith("```"):
            continue
        sl = s.lower()
        if sl.startswith(("- source", "- tags", "source:", "tags:", "- 관련", "- links")):
            continue
        body.append(s)
    return len(" ".join(body))


def extract_relevant_excerpt(content: str, terms: list[str], max_chars: int = 2400, query: str = "") -> str:
    sections = [section.strip() for section in re.split(r"(?=^##\s+)", content, flags=re.MULTILINE) if section.strip()]
    paragraphs = sections or [paragraph.strip() for paragraph in re.split(r"\n\s*\n", content) if paragraph.strip()]
    line_noise = (
        "[tavily]", "[ddg]", "[naver]", "[google]", "youtube.com", "instagram.com",
        "telegram-auto-search", "telegram-auto-quality", "웹 검색 자동 수집", "자동 수집 결과:",
        "검토 기준:", "감지 사유:", "처리 기준:",
        "auto-quality", "knowledge-gap", "self-healing", "needs-review",
        "source: telegram-", "source: system-", "tags: auto-", "tags: auto",
        "1차 답변 품질검사", "답변 품질 기준 미달", "자동 보강을 시작",
        "- source:", "- tags:", "- links:", "출처: http", "출처: https",
        "자동 수집:", "auto-collect", "needs-review",
        # auto-enrich KST04 가드레일 라인(거버넌스 마커) — 고객 답변 노출 금지.
        # 'kst04 자동수집' 전체 문구로만 매칭해 KST01~KST04 방법론 본문은 보존한다.
        "kst04 자동수집",
        # 지식업데이트 KB의 needs-review 검색 실패 샘플 — 노이즈 샘플 섹션 한정 마커.
        "노이즈 샘플", "운영 판정:", "수집 후보 결과:", "검색 실패 사례",
        # 웹 수집 후보의 provider-evidence 불릿/출처 — needs-review 노이즈(지식업데이트 KB 한정).
        "tavily evidence", "ddg evidence", "naver evidence", "google evidence", "source-url:",
        "• [", "질문: ",
    )

    def clean_paragraph(paragraph: str) -> str:
        lines = paragraph.splitlines()
        kept = [l for l in lines if not any(n in l.lower() for n in line_noise)]
        return "\n".join(kept).strip()

    # 검증 전 자동수집(KST04 auto-enrich) 섹션 식별 — 클리닝 전 원문에서 판정해야
    # 가드레일/Source 라인이 stripped 되기 전에 잡는다. 이 섹션은 curated 검증 섹션
    # 아래로 강등하고(정독 결과 confident-오답의 주원인), 그래도 노출될 땐 면책을 붙인다.
    def _is_autoenrich(paragraph: str) -> bool:
        # 출처/거버넌스 마커로만 판정한다. bare 'auto-enrich'는 본문에서 기능을
        # 설명하는 정상 큐레이션 섹션('auto-enrich guardrail 결과를...')까지 오탐하므로
        # 실제 자동수집 Source 라인 형식('auto-enrich via ...')과 KST04 마커로 한정.
        pl = paragraph.lower()
        return "kst04 자동수집" in pl or "auto-enrich via" in pl

    _pairs = [(clean_paragraph(p), _is_autoenrich(p)) for p in paragraphs]
    _pairs = [(c, f) for c, f in _pairs if c]
    if _pairs:
        paragraphs = [c for c, _ in _pairs]
        autoenrich_set = {c for c, f in _pairs if f}
    else:
        autoenrich_set = set()
    if not paragraphs:
        return content[:max_chars]
    query_lower = query.lower()
    wants_legal = any(keyword in query_lower for keyword in ["법", "법규", "고시", "ks", "기준서", "근거문서", "인허가"])
    wants_type = any(keyword in query_lower for keyword in ["종류", "유체", "계통", "분류", "말고", "약어"])
    # 'bare 패밀리'는 배치 의도가 아니다(패밀리 파라미터/공유 등). 실제 배치·로드 신호로만.
    wants_family_placement = any(keyword in query_lower for keyword in ["폴더", "하위", "배치", "로드", "loadfamily", "rfa"])

    def paragraph_score(paragraph: str) -> int:
        lower = paragraph.lower()
        score = score_knowledge_text(paragraph, terms)
        # 섹션 제목이 질의어와 겹치면 그 섹션이 질문의 세부 주제일 가능성이 높다.
        # 길고 키워드가 조밀한 다른 섹션이 확장 토큰으로 점수를 부풀려 정답 섹션을
        # 가리는 것을 막는다(예: '분전반 전면 작업공간' 질문이 케이블트레이 섹션에 밀림).
        heading = lower.splitlines()[0] if lower else ""
        if heading.startswith("#"):
            matched_in_head = [term for term in terms if len(term) >= 2 and term in heading]
            score += min(len(matched_in_head), 3) * 20
            # 길이 보너스: 제목에 든 더 긴(=구체적) 질의어를 약간 더 가산한다. 흔한 공통어
            # (revit/addin)보다 distinctive 용어(transaction)가 든 섹션을 끌어올린다.
            score += min(sum(len(t) for t in matched_in_head), 20)
        if wants_type and any(keyword in lower for keyword in ["기본 분류", "역할·유체", "유체 약어", "종류", "말고 다른"]):
            score += 18
        # '빠른 답변' 큐레이션 섹션 가산 — 단, 세부주제가 어긋난 빠른답변이 정답
        # 섹션을 가리지 않도록 제목 일치(위 heading 부스트)가 우선하는 타이브레이커 수준.
        if "빠른 답변" in lower:
            score += 15
        if wants_family_placement:
            if any(keyword in lower for keyword in ["폴더 하위", "패밀리 로드", "패밀리", "loadfamily", "newfamilyinstance", ".rfa"]):
                score += 50
            if any(keyword in lower for keyword in ["카테고리 객체", "일괄 선택", "all elements of category", "setelementids"]):
                score -= 30
        # LUA 제품(Revit Assistant/게이트웨이) 섹션 가산은 연동·제품 맥락 질의에만.
        # 일반 Revit API 질문(트랜잭션/패밀리/파라미터)까지 끌어올리면 본래 주제를 가린다.
        if (
            any(keyword in query_lower for keyword in ["assistant", "어시스턴트", "luachat", "게이트웨이", "gateway", "연동", "설치", "라이선스"])
            and any(keyword in query_lower for keyword in ["revit", "addin", "add-in", "애드인"])
            and any(keyword in lower for keyword in ["revit assistant", "지식 게이트웨이", "knowledge-gateway", "설비 bim 근거", "lua bim labs"])
        ):
            score += 25
        if "설비 질문" in query_lower and any(keyword in lower for keyword in ["revit assistant", "지식 베이스", "설비 bim", "obsidian"]):
            score += 18
        if any(keyword in lower for keyword in ["faq", "답변 포인트", "물 때:"]):
            score += 8
        if "## " in paragraph[:12] or paragraph.startswith("# "):
            score += 3
        # 검증 전 자동수집(auto-enrich) 섹션 강등: 질의가 명시적으로 '최신/동향/트렌드/
        # 요즘/최근'을 묻지 않는 한 curated 검증 섹션이 항상 우선하도록 큰 페널티를 준다.
        if paragraph in autoenrich_set and not any(
            k in query_lower for k in ["최신", "동향", "트렌드", "요즘", "최근", "근황"]
        ):
            score -= 60
        if not wants_legal and any(keyword in lower for keyword in ["국내 법령", "국내 고시", "ks 규격", "국내 표준", "국제 기준", "법률 제", "시행규칙"]):
            score -= 22
        # 공항·대형시설 '연면적 데이터베이스'는 흔한 토큰 '면적'(⊂연면적)으로 무관 면적 질의
        # (방화구획/실/주차장/개구부 면적)의 선두 섹션을 가로채는 자석이다. 질의가 연면적/규모/
        # 대형시설/공항을 명시할 때만 정상 점수, 아니면 페널티(c29/c30 magnet 페널티 패턴).
        if "연면적 실무 데이터베이스" in lower or (
            "연면적" in lower and any(b in lower for b in ["인천국제공항", "스타필드", "제2터미널", "탑승동"])
        ):
            if not any(k in query_lower for k in ["연면적", "규모", "대형", "공항", "터미널", "스타필드"]):
                score -= 45
        return score

    ranked = sorted(
        ((paragraph_score(paragraph), index, paragraph) for index, paragraph in enumerate(paragraphs)),
        key=lambda item: (item[0], -item[1]),
        reverse=True,
    )
    selected_limit = 1 if wants_family_placement else 2
    positive = [(score, idx, para) for score, idx, para in ranked if score > 0]
    if not positive:
        selected = [paragraphs[0]]
    else:
        selected = [positive[0][2]]
        # 배너 헤딩(본문이 메타/--- 뿐, 실제 콘텐츠는 다음 ## 섹션)이 heading-match 로
        # 뽑히면 thin excerpt 가 된다. 선택 섹션 본문이 near-empty 면 다음 문서순 섹션을 병합.
        top_idx = positive[0][1]
        if _section_body_chars(positive[0][2]) < 40 and top_idx + 1 < len(paragraphs):
            selected.append(paragraphs[top_idx + 1])
        if selected_limit > 1 and len(positive) > 1:
            # 2번째 섹션은 1번째가 다루지 못한 질의어를 커버하는 상위 후보를 우선한다.
            # 다중 항목 질문('A와 B')에서 한 측면만 답하는 것을 막는다. 단일주제 질의는
            # 미커버 용어가 없어 기존(차점) 동작과 동일하다.
            first_lower = positive[0][2].lower()
            uncovered = [t for t in terms if t not in first_lower]
            # 참조 '데이터베이스'(예: 공항·대형시설 연면적 DB)는 흔한 토큰('면적')으로
            # 무관 질의(방화구획 면적 등)의 2번째 섹션에 끼어드는 자석이다. 질의가 그 DB의
            # 도메인(연면적/규모/대형시설)을 명시할 때만 2번째 섹션 후보로 허용한다.
            _db_topic = any(t in ("연면적", "규모", "대형", "공항", "시설규모") for t in terms) \
                or any(k in (query or "").lower() for k in ("연면적", "규모", "대형", "공항"))

            def _ok_second(para: str) -> bool:
                if _db_topic:
                    return True
                pl = para.lower()
                # 연면적 DB 본문/하위표(연면적·특정시설명 밀집)는 무관 '면적' 질의에서 제외
                return "데이터베이스" not in para[:100].lower() and "연면적" not in pl

            candidates = [para for _, _, para in positive[1:5] if _ok_second(para)]
            second = next(
                (para for para in candidates
                 if uncovered and any(t in para.lower() for t in uncovered)),
                candidates[0] if candidates else None,
            )
            if second is not None:
                selected.append(second)
    excerpt = "\n\n".join(selected)
    # auto-enrich 섹션이 답변에 포함되면(강등 후에도 유일 후보 등) 면책을 선두에 붙여
    # 미검증 정보가 면책 없이 confident 답변으로 노출되지 않게 한다.
    if any(p in autoenrich_set for p in selected):
        excerpt = (
            "⚠️ 아래는 검증 전 자동수집(auto-enrich) 참고 정보입니다. "
            "공식 출처·담당자 확인 전에는 고객 확정 답변·견적·납품 기준으로 사용하지 마세요.\n\n"
            + excerpt
        )
    return _clean_truncate(excerpt, max_chars)


def search_local_knowledge(query: str, limit: int = 4) -> list[dict]:
    terms = query_terms(query)
    if not terms:
        return []
    inferred_agent = infer_knowledge_agent_from_query(query)
    inferred_team = _AGENT_TO_TEAM.get(inferred_agent, "")

    catalog = _load_catalog()
    candidate_rel: set[str] = set()
    known_rel: set[str] = set()
    team_by_rel: dict[str, str] = {}
    domain_by_rel: dict[str, str] = {}
    inferred_domain = ""
    if catalog:
        candidate_rel, known_rel = _catalog_candidates(catalog, terms)
        team_by_rel = _catalog_team_lookup(catalog)
        domain_by_rel = _catalog_domain_lookup(catalog)
        inferred_domain = _catalog_agent_domain(catalog, inferred_agent)

    # 카탈로그(매일 빌드)보다 새로 갱신된 파일은 스킵하지 않는다. 자가치유 보강이
    # 추가한 콘텐츠가 다음 일일빌드 전이라도 검색되도록 스테일 엔트리를 자가보정한다.
    catalog_mtime = _catalog_state.get("mtime")
    matches = []
    for path in knowledge_search_files():
        try:
            rel = path.relative_to(_PROJECT_ROOT).as_posix()
        except ValueError:
            rel = path.as_posix()
        # 카탈로그가 아는 파일인데 키워드 후보가 아니면 본문 스캔 생략
        # (안전판: 파일명이 추론 에이전트/검색어와 닿아 있거나, 카탈로그보다 새 파일이면 항상 스캔)
        if (
            candidate_rel
            and rel in known_rel
            and rel not in candidate_rel
            and inferred_agent not in path.stem
            and not any(term in path.stem.lower() for term in terms)
            and (catalog_mtime is None or path.stat().st_mtime <= catalog_mtime)
        ):
            continue
        try:
            content = path.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        score = score_knowledge_text(content, terms)
        if path.is_relative_to(_AGENT_KB_DIR) or path.is_relative_to(_QA_KB_DIR):
            score += 8
        # 파일 stem 은 특수문자가 제거돼 저장되므로(safe_agent_stem) 추론 에이전트도
        # 같은 규칙으로 정규화해 비교한다. 그래야 '고객지원 CS' 등도 자기 KB 를 찾는다.
        inferred_stem = _safe_agent_stem(inferred_agent)
        if path.stem == inferred_stem:
            score += 80 if inferred_agent in {"간섭검토", "설비시공조율"} else 50
        elif inferred_stem and inferred_stem in path.stem:
            score += 10
        if any(term in path.stem.lower() for term in terms):
            score += 8
        if inferred_team and team_by_rel.get(rel) == inferred_team:
            score += 6
        if inferred_domain and inferred_domain != "기타" and domain_by_rel.get(rel) == inferred_domain:
            score += 4
        if "curation" in rel.lower() or "daily_knowledge" in rel.lower():
            score -= 30
        if path.stem in {"지식업데이트", "지식업데이트_QA", "지식큐레이터", "지식큐레이터_QA"} and not any(
            term in query.lower()
            for term in ("지식", "큐레이션", "업데이트", "답변 품질", "kpi", "평가 축", "제품화")
        ):
            score -= 50
        # 내부 신호/성장펄스/전략리뷰 운영 로그는 도메인 Q&A 의 답이 아니다.
        # 흔한 토큰(예: '시간')으로 도메인 질문을 가로채는 것을 막되, 질의가 실제
        # 트렌드/신호/전략 의도면 면제한다(그땐 정상적으로 최상위가 되어야 함).
        stem_lower = path.stem.lower()
        is_internal_log = any(
            marker in stem_lower
            for marker in ("신호모니터링", "self_growth_pulse", "전략승격리뷰", "성장펄스")
        )
        if is_internal_log and not any(
            kw in query.lower()
            for kw in ("신호", "모니터링", "트렌드", "펄스", "ax", "전략", "성장", "시장", "동향")
        ):
            score -= 40
        # BIMobject 패밀리 인덱스(316KB 카탈로그)는 영문 카테고리·패밀리명이 방대해
        # 도메인 질의(특히 영문)를 magnet 으로 빨아들인다. 패밀리/라이브러리 검색 의도가
        # 아니면 페널티해 도메인 답을 가리지 않게 한다(패밀리 검색 질의엔 그대로 최상위).
        if path.stem == "BIMobject_패밀리_인덱스" and not any(
            kw in query.lower()
            for kw in ("bimobject", "패밀리", "family", "라이브러리", "library", "카탈로그", "다운로드")
        ):
            score -= 40
        if score <= 0:
            continue
        # excerpt 는 비싸다(노이즈 제거·문단 랭킹·정규식). 점수>0 인 모든 후보(~90개)에
        # 계산하면 낭비라, 정렬 후 상위 limit 개에만 계산한다(콘텐츠는 잠시 보관).
        matches.append({"score": score, "path": path, "_content": content})
    top = sorted(matches, key=lambda item: item["score"], reverse=True)[:limit]
    for match in top:
        match["excerpt"] = extract_relevant_excerpt(match.pop("_content"), terms, query=query)
    return top


def prioritize_agent_matches(matches: list[dict], agent: str) -> list[dict]:
    if not matches:
        return matches

    agent_stem = _safe_agent_stem(agent)

    def rank(match: dict) -> tuple[int, int]:
        path = match.get("path")
        stem = path.stem if isinstance(path, Path) else ""
        agent_hit = 1 if stem == agent_stem else 0
        return (agent_hit, int(match.get("score", 0)))

    return sorted(matches, key=rank, reverse=True)


def _inference_rule_matches(rule: dict, lower_text: str) -> bool:
    """규칙 매처: all=모든 부분문자열, any=하나 이상, any_groups=각 그룹마다 하나 이상 (모두 AND)."""
    if "all" in rule and not all(k in lower_text for k in rule["all"]):
        return False
    if "any" in rule and not any(k in lower_text for k in rule["any"]):
        return False
    if "any_groups" in rule:
        for group in rule["any_groups"]:
            if not any(k in lower_text for k in group):
                return False
    return True


def infer_knowledge_agent_from_query(query: str) -> str:
    """질의 → 담당 지식 에이전트. 규칙은 config/organization.json(SSOT)의
    inference_rules 순서(=우선순위)대로 평가한다. 새 라우팅은 코드가 아니라 config 편집."""
    st = _st()
    # 흔한 표기 변형 정규화(라우팅은 raw substring 매칭이라 변형이 키워드를 비껴간다).
    # '컨텐츠'→'콘텐츠', '후렉시블'→'플렉시블'(flexible)은 흔한 오기 → 통일해 라우팅 견고화.
    # '분전판'→'분전반'(반/판 혼동), '커텐월'→'커튼월'(curtain)도 흔한 변형 → KB 표기로 통일.
    lower_text = (
        query.lower()
        .replace("컨텐츠", "콘텐츠").replace("후렉시블", "플렉시블")
        .replace("분전판", "분전반").replace("커텐월", "커튼월").replace("방화구회", "방화구획")
    )

    for rule in _registry.inference_rules():
        target = rule["target"]
        if target == "@discipline_keywords":
            # 공종 키워드 순회 (DISCIPLINE_KEYWORDS 순서대로 첫 매칭)
            for agent, keywords in st.DISCIPLINE_KEYWORDS.items():
                if any(keyword.lower() in lower_text for keyword in keywords):
                    return agent
            continue
        if target == "@knowledge_agent_name":
            # 에이전트명 직접 포함 여부
            for agent in st.KNOWLEDGE_AGENTS:
                name = agent.lower()
                if name.isascii():
                    # 짧은 ASCII 명(COO/CEO/CFO 등)은 단어경계로만 매칭한다. 부분일치를
                    # 허용하면 'coo'∈'coordinator' 처럼 영문 단어 속에 박혀 오라우팅된다
                    # (예: 'BIM Coordinator 6년차 교육'이 교육컨설팅 대신 COO 로 샘).
                    # 밑줄(_)은 경계로 보지 않아 'revit_addin' 같은 합성명도 온전히 매칭.
                    if re.search(rf"(?<![a-z0-9]){re.escape(name)}(?![a-z0-9])", lower_text):
                        return agent
                elif name in lower_text:
                    return agent
            continue
        if _inference_rule_matches(rule, lower_text):
            return target

    # 규칙이 모두 빗나갔을 때만(=공종/명시 규칙 우선) 이름-친화도 폴백.
    # 운영 기본값(지식업데이트)으로 떨어지면 자기 KB 가산점(+50)이 사라져
    # 올바른 로컬 답변도 점수가 임계 밑으로 내려가 불필요한 웹검색이 돈다.
    # 질의 용어가 에이전트명(특수문자 제거)에 2개 이상 포함되면 그 에이전트로 본다.
    fallback = _name_affinity_agent(query)
    if fallback:
        return fallback

    return _registry.inference_default()


_OPERATIONAL_INFERENCE_AGENTS = {"지식업데이트", "지식큐레이터"}


def _name_affinity_agent(query: str) -> str:
    """질의 용어와 에이전트명(safe stem)의 부분일치로 담당 에이전트를 추정.

    규칙 기반 추론이 모두 실패한 경우의 마지막 폴백. 공종/명시 규칙이 먼저
    평가되므로 핵심 도메인 라우팅을 가로채지 않는다(가산적·후순위)."""
    st = _st()
    terms = [t for t in query_terms(query) if len(t) >= 2]
    if not terms:
        return ""
    best_agent = ""
    best_score = 0
    for agent in st.KNOWLEDGE_AGENTS:
        if agent in _OPERATIONAL_INFERENCE_AGENTS:
            continue
        stem = _safe_agent_stem(agent).lower()
        if len(stem) < 2:
            continue
        matched = [t for t in terms if t in stem or stem in t]
        if not matched:
            continue
        # 매칭 용어 수 + 매칭 길이 합(더 구체적인 이름 우선)
        score = len(matched) * 100 + sum(len(t) for t in matched)
        # 단일 약매칭(이름 부분만 1개)은 채택하지 않음 — 오라우팅 방지.
        if len(matched) < 2 and not any(t == stem for t in matched):
            continue
        if score > best_score:
            best_score = score
            best_agent = agent
    return best_agent


def resolve_save_agent(query: str, matches: list[dict] | None = None) -> str:
    """지식 갭 자동수집 결과를 저장할 담당 에이전트를 정한다.

    추론 라우팅이 운영 기본값(지식업데이트)으로 떨어지는 도메인 질의가 많은데,
    이때 무작정 '건축'으로 저장하면 구조/법무/제품패키징 등의 웹 보강 내용이
    엉뚱한 에이전트 KB 를 오염시킨다. 추론 실패 시 검색 top 파일의 에이전트로
    역매핑해 올바른 KB 에 적재한다."""
    st = _st()
    operational = {"지식업데이트", "지식큐레이터"}
    inferred = infer_knowledge_agent_from_query(query)
    if inferred in st.KNOWLEDGE_AGENTS and inferred not in operational:
        return inferred
    # 검색 top → 에이전트 역매핑(stem 정규화 기준)
    if matches is None:
        matches = search_local_knowledge(query, limit=1)
    stem_to_agent = {_safe_agent_stem(a): a for a in st.KNOWLEDGE_AGENTS}
    for match in matches or []:
        path = match.get("path")
        stem = path.stem if isinstance(path, Path) else ""
        # _QA 파일도 본체 에이전트로 환원
        base_stem = stem[:-3] if stem.endswith("_QA") else stem
        agent = stem_to_agent.get(base_stem)
        if agent and agent not in operational:
            return agent
    return "건축"


def build_knowledge_answer(query: str, matches: list[dict]) -> str:
    if not matches:
        return ""
    st = _st()
    return st.sanitize_outbound_text(st.clean_markdown_for_display(matches[0]["excerpt"])[:3600])


_LUA_INTRO = (
    "저는 Lua입니다. LUA BIM LABS의 MEP BIM 전문 AI 어시스턴트로, "
    "Revit·Navisworks·설비(MEP) BIM 실무와 지식 베이스 기반 질의응답을 돕습니다. "
    "무엇을 도와드릴까요?"
)
# 인사/감사 같은 사회적 발화는 '찾지 못함'이 아니라 친근한 결정적 응답을 준다(고객 접점 UX).
_GREETING_REPLY = (
    "안녕하세요! 저는 LUA BIM LABS의 BIM 어시스턴트 Lua입니다. "
    "Revit·Navisworks·설비(MEP) BIM 실무나 지식이 궁금하시면 편하게 물어봐 주세요."
)
_THANKS_REPLY = "도움이 되었다니 다행입니다. 더 궁금한 점이 있으면 언제든 질문해 주세요."
# 공백/물음표 제거 후 정확히 일치할 때만(실제 도메인 질의 hijack 방지). 짧은 단독 사회적 발화.
_GREETING_EXACT = frozenset({
    "안녕", "안녕하세요", "안녕하십니까", "안뇽", "하이", "헬로", "hi", "hello",
    "반가워요", "반갑습니다", "반가워", "좋은아침", "좋은하루", "수고하세요", "수고하십니다",
})
_THANKS_EXACT = frozenset({
    "고마워", "고마워요", "고맙습니다", "고마웠어요", "감사", "감사해", "감사해요",
    "감사합니다", "감사드립니다", "감사드려요", "땡큐", "thanks", "thankyou", "thx",
    "도움이됐어요", "도움됐어요", "잘봤습니다", "잘봤어요",
})
# 복합 감사 발화("고마워요 도움이 됐어요"·"정말 감사합니다") — exact 셋이 놓치는 케이스.
# 명확한 감사 substring 만(짧은 발화 한정) 매칭해 도메인 질의 hijack 을 막는다.
# bare "감사"는 'BIM 감사 기준'(audit) 충돌이라 제외하고 종결형(감사합니다/해/드)만 본다.
_THANKS_CONTAINS = (
    "고마워", "고맙", "감사합니다", "감사해", "감사드", "감사히", "땡큐", "thank",
    "도움이됐", "도움됐", "도움이되었", "도움많이", "큰도움", "잘봤",
)
# 공백 제거 후 정확히 일치할 때만 정체성으로 보는 짧은 단독 표현
_IDENTITY_EXACT = {
    "누구세요", "누구야", "누구신가요", "누구인가요", "누구니",
    "자기소개", "자기소개해", "자기소개해줘", "소개해줘",
    "너누구야", "넌누구야", "너누구니", "네소개", "당신은누구",
    # 주어 없는 단독 이름 질의(챗봇 문맥상 봇 이름) — 전체 일치일 때만(도메인 질의 'X 이름이 뭐야'는 미해당)
    "이름이뭐예요", "이름이뭐야", "이름뭐야", "이름뭐예요", "이름이뭐니",
    "이름알려줘", "이름이무엇인가요", "이름이무엇인가", "성함이어떻게되세요",
}
# 봇 자신을 가리키는 self-reference (이게 있어야 '누구/이름/기능' 질의를 봇 대상으로 본다 → 도메인/제품 질의 오발 방지)
_IDENTITY_SELFREF = (
    "너", "당신", "넌", "네 이름", "너 이름", "당신 이름", "너의", "당신의",
    "봇", "bot", "lua", "루아", "어시스턴트", "assistant", "자기소개",
)
# 봇 능력(capability) 질의 — 주어 없이 단독일 때만(전체 일치). 제품 기능 질의는 미해당.
_CAPABILITY_EXACT = {
    "뭐할수있어", "뭐할수있나요", "무엇을할수있나요", "무엇을할수있어", "뭘할수있어",
    "뭘도와줄수있어", "무엇을도와줄수있어", "뭐도와줄수있어", "어떻게도와줄수있어",
    "뭘도와줄수있나요", "어떤걸물어보면돼", "어떤걸물어봐야돼", "뭐물어보면돼",
    # 주어 없는 단독 역량/기능 질의(챗봇 문맥상 봇 능력) — 제품 기능 질의는 주어가 있어 미해당.
    "도와줄수있어", "도와줄수있나요", "도와줄수있니", "도움을줄수있어",
    "무슨기능이있나요", "무슨기능이있어", "어떤기능이있나요", "어떤기능이있어",
    "어떤기능을제공하나요", "어떤기능을제공해", "기능이뭐가있어", "기능이뭐가있나요",
    "기능뭐있어", "어떤걸도와줄수있어", "어떤도움을줄수있어",
}
# self-reference 와 함께 능력 의도를 나타내는 표현
_CAPABILITY_HINTS = ("할 수 있", "할 줄", "뭐 해", "뭐 도와", "도와줄", "무엇을 도와", "어떤 기능", "무슨 기능", "기능이 있")


# 대화 후속질의 판별용 — 주제(subject)가 아닌 일반 요청어/속성어/지시어.
# 이것만 남으면 '주어 없는 후속질의'로 보고 직전 대화 주제를 상속한다.
# 속성명사(어떤 대상의 측정/스펙 속성). 단독이면 직전 주제에 대한 후속질의이지만, carried
# 재시도 안전게이트에서는 이 속성어가 carried 발췌에 실제 있으면 관련 후속으로 인정한다
# ('간격은?'·'용량은?' 처럼 토픽이 전부 속성어라 extract_topic_terms 가 비는 경우 대비).
_CONTEXT_ATTRIBUTE_TERMS = frozenset({
    "간격", "순서", "용량", "크기", "치수", "두께", "높이", "길이", "폭", "직경",
    "구경", "개수", "수량", "종류", "방법", "기준", "사양", "스펙", "재질", "수치",
})

_CONTEXT_GENERIC_TERMS = frozenset({
    # 요청 동사/표현
    "알려줘", "알려", "찾아줘", "찾아서", "찾아", "보여줘", "보여", "정리", "정리해",
    "설명", "설명해", "말해줘", "말해", "줘", "주세요", "해줘", "나에게", "내게", "좀",
    # 추가 요청·엘라보레이션 동사/표현(직전 주제에 대한 후속 = 문맥 상속 대상)
    "알려주세", "설명해줘", "설명해주세", "설명좀", "들어줘", "들어주세", "보여주세",
    "가르쳐줘", "가르쳐주세", "예시", "예", "사례", "쉽게", "간단히", "간략히",
    "자세하게", "구체적으로", "풀어서",
    # 일반 명사(주제가 아닌 메타)
    "프로젝트", "관련", "자료", "정보", "내용", "개요", "자세히", "상세", "현황", "사항", "제품",
    # 지시어/조응(대명사·장소대명사) — 주제가 아니므로 후속질의로 본다
    "그", "이", "저", "해당", "위", "방금", "아까", "그거", "이거", "저거", "그것", "이것",
    "동일", "같은", "거기", "여기", "저기", "그곳", "이곳", "저곳",
    "그건", "이건", "저건", "그게", "이게", "그걸", "이걸", "더",
    # 흔한 속성 변형
    "준공일", "준공년도", "준공연도", "담당", "담당자",
    # 흔한 속성(주제 없이 단독이면 후속질의) — 건설/BIM 공통 메타속성
    "시공사", "연면적", "면적", "규모", "위치", "준공", "발주처", "발주", "설계사",
    "공사", "기간", "비용", "가격", "등등", "등", "무엇", "뭐", "어떻게", "얼마",
    "누구", "누가", "언제", "어디", "어디야", "왜",
    # 속성명사(어떤 대상의 속성 — 단독이면 직전 주제에 대한 후속질의). SSOT: 위 _CONTEXT_ATTRIBUTE_TERMS.
    *_CONTEXT_ATTRIBUTE_TERMS,
})


# 조사(긴 것 우선으로 제거) — query_terms 는 도메인 확장을 하므로 문맥판별엔 자체 토크나이저 사용
_CONTEXT_JOSA = (
    # 의문/서술 종결(긴 것 우선)
    "인가요", "일까요", "나요", "어요", "아요", "예요", "에요", "이야", "일까", "인지",
    # 조사
    "으로서", "에서의", "으로", "로서", "에서", "에게", "까지", "부터", "이나",
    "이랑", "랑", "을", "를", "이", "가", "은", "는", "의", "도", "에",
    "와", "과", "로", "만", "께", "나", "야", "요", "죠",
)
# 흔한 동사/보조어미/의문어(주제 아님)
_CONTEXT_VERB_AUX = frozenset({
    "알고", "싶어", "싶다", "싶어요", "궁금", "궁금해", "궁금합니다", "해줘", "해주세요",
    "하는", "인지", "일까", "될까", "되나", "인가", "인가요", "어떤", "무슨", "해봐",
    "말이야", "말야", "되는지", "있어", "있나", "있나요", "알려주세요",
})


def _strip_context_josa(token: str) -> str:
    changed = True
    while changed and len(token) >= 3:
        changed = False
        for j in _CONTEXT_JOSA:
            if len(token) > len(j) + 1 and token.endswith(j):
                token = token[: -len(j)]
                changed = True
                break
    return token


def extract_topic_terms(query: str) -> list[str]:
    """질의에서 '주제(subject)'로 볼 distinctive 토큰만 추출한다.
    조사/동사어미/일반 요청·속성·지시어를 제거하고 남은 게 없으면 '주어 없는 후속질의'
    (직전 대화 주제 상속 대상)로 판단한다. query_terms 의 도메인 확장을 피하려 자체 토크나이즈."""
    topic: list[str] = []
    for raw in re.findall(r"[0-9A-Za-z가-힣]+", query.lower()):
        t = _strip_context_josa(raw)
        if not t or t in _CONTEXT_GENERIC_TERMS or t in _CONTEXT_VERB_AUX:
            continue
        if len(t) < 2 and not t.isalnum():
            continue
        topic.append(t)
    return topic


def extract_attribute_terms(query: str) -> list[str]:
    """질의에서 속성명사(간격/용량/두께 등 _CONTEXT_ATTRIBUTE_TERMS)만 추출한다.
    '간격은?'처럼 토픽이 전부 속성어라 extract_topic_terms 가 비는 순수 속성 후속질의의
    관련성 판정(carried 재시도 안전게이트)에 쓴다."""
    out: list[str] = []
    for raw in re.findall(r"[0-9A-Za-z가-힣]+", query.lower()):
        t = _strip_context_josa(raw)
        if t in _CONTEXT_ATTRIBUTE_TERMS:
            out.append(t)
    return out


def identity_answer(query: str) -> str | None:
    """봇 정체성/이름/능력 질의면 결정적으로 'Lua' 소개(_LUA_INTRO)를 반환한다(아니면 None).

    qwen 합성 페르소나는 ollama 다운 시 미적용 → raw 폴백 경로에서도 이런 질의가
    엉뚱한 KB 발췌(IFC 연동 실패 등)를 반환하던 것을 차단. self-reference 가 있을 때만
    '누구/이름/기능'을 봇 대상으로 해석해 '이 부재 이름이 뭐야'·'BIM Command Center 어떤 기능'
    같은 도메인/제품 질의 오발을 막는다."""
    if not query:
        return None
    q = query.strip().lower()
    q_nospace = q.rstrip("?!.~ ").replace(" ", "")
    # 인사/감사 등 사회적 발화 — '찾지 못함' 대신 친근한 응답(exact 매칭이라 도메인 질의 무영향).
    if q_nospace in _GREETING_EXACT:
        return _GREETING_REPLY
    if q_nospace in _THANKS_EXACT:
        return _THANKS_REPLY
    # 복합 감사 발화: 짧고(도메인 문장 배제) 명확한 감사 표현을 포함하면 친근 응답.
    if len(q_nospace) <= 24 and any(marker in q_nospace for marker in _THANKS_CONTAINS):
        return _THANKS_REPLY
    if q_nospace in _IDENTITY_EXACT or q_nospace in _CAPABILITY_EXACT:
        return _LUA_INTRO
    has_self = any(token in q for token in _IDENTITY_SELFREF)
    if has_self and ("누구" in q or "이름" in q):
        return _LUA_INTRO
    if has_self and any(hint in q for hint in _CAPABILITY_HINTS):
        return _LUA_INTRO
    return None


def assess_knowledge_answer_quality(query: str, agent: str, matches: list[dict], answer: str = "") -> dict:
    st = _st()
    reasons: list[str] = []
    top = matches[0] if matches else None
    top_score = int(top.get("score", 0)) if top else 0
    top_path = top.get("path") if top else None
    top_stem = top_path.stem if isinstance(top_path, Path) else ""
    query_lower = query.lower()
    answer_lower = (answer or "").lower()

    if not matches:
        reasons.append("no-local-match")
    if top_score and top_score < _WEAK_LOCAL_SCORE:
        reasons.append(f"low-score:{top_score}")
    if agent and agent in st.KNOWLEDGE_AGENTS and top_stem and top_stem != _safe_agent_stem(agent):
        if agent in {"Dynamo", "Revit_Addin", "Navisworks_Addin"}:
            reasons.append(f"agent-mismatch:{top_stem}")
        elif top_stem in {"지식업데이트", "지식큐레이터"}:
            reasons.append(f"operational-doc-ranked:{top_stem}")
    if top_stem in {"지식업데이트", "지식큐레이터"} and not any(term in query_lower for term in ["지식", "큐레이션", "업데이트"]):
        reasons.append(f"operational-doc-ranked:{top_stem}")
    # 인프라_DevOps(Obsidian) 는 정식 지식 에이전트다. 다만 인프라/Obsidian/DevOps
    # 와 무관한 질의에서 top 이면 도메인 누수로 보고 보강한다(주제 적합 시 로컬 즉답).
    if top_stem == "인프라_DevOpsObsidian" and not any(
        term in query_lower for term in ["obsidian", "옵시디언", "devops", "ci/cd", "ci ", "파이프라인", "인프라", "배포", "백업", "동기화", "볼트", "vault"]
    ):
        reasons.append(f"operational-doc-ranked:{top_stem}")
    if any(noise in answer_lower for noise in ["현재 보유 지식에서 충분히", "| 문서 | 유형 | 권고 |", "daily_knowledge_curation"]):
        reasons.append("answer-noise")
    if any(term in query_lower for term in ["다이나모", "dynamo"]) and "dynamo" not in top_stem.lower():
        reasons.append(f"dynamo-not-ranked:{top_stem or '-'}")

    # 시설 규모(면적/연면적/세대수/층수...) 팩트 질의에서, 매칭 답변이 질의가 지목한
    # 고유 시설명을 전혀 담지 않으면 '엉뚱한 시설 수치를 confident 로 서빙'하는 것이다.
    # 예: '청라 스타필드 면적' → 표에 없어 인천공항 연면적 표를 그대로 반환(면책 문구가
    # 있어도 사용자는 질문한 시설의 답을 못 얻고 다른 시설 수치를 먼저 봄). 이런 경우
    # 웹검색을 허용한다. '공항/터미널/센터' 같은 카테고리어는 식별자가 아니므로 제외해
    # '김포 공항 면적'이 인천'공항' 부분일치로 오통과하지 않게 한다.
    if answer_lower and any(m in query_lower for m in _MAGNITUDE_FACT_MARKERS):
        entity_terms = [
            t for t in extract_topic_terms(query)
            if t not in _MAGNITUDE_FACT_MARKERS
            and t not in _FACILITY_CATEGORY_WORDS
            and not t.isdigit() and len(t) >= 2
        ]
        # 실제 커버는 '시설명 + 수치(㎡)' 인접으로 본다. 단순 등장은 면책 산문
        # ("표에 없는 예: 무역센터 KITA …")일 수 있어 커버로 인정하지 않는다.
        if entity_terms and not any(
            _entity_has_magnitude_nearby(answer_lower, t) for t in entity_terms
        ):
            reasons.append("named-entity-not-covered")

    return {
        "ok": not reasons,
        "reasons": reasons,
        "top_score": top_score,
        "top_path": _relative_to_project(top_path) if isinstance(top_path, Path) else "",
    }


def _relative_to_project(path: Path) -> str:
    """PROJECT_ROOT 기준 상대경로. 밖에 있으면(테스트 tmp_path 등) 원본 문자열 반환.
    (유료 Revit 경로가 readiness 평가를 공유하면서 PROJECT_ROOT 밖 경로도 들어올 수 있다.)"""
    try:
        return str(path.relative_to(_PROJECT_ROOT))
    except ValueError:
        return str(path)


_MAGNITUDE_VALUE_RE = re.compile(r"[0-9][0-9,\.]*\s*(?:㎡|m2|m²|만㎡|만\s*㎡|만|세대|층|m\b)")


def _entity_has_magnitude_nearby(answer_lower: str, entity: str, window: int = 60) -> bool:
    """답변에서 시설명(entity) 등장 위치 인근(window 자)에 규모 수치(㎡/만/세대/층)가
    있으면 '실제 데이터 행으로 커버됨'으로 본다. 면책 산문의 단순 언급과 구분한다."""
    el = entity.lower()
    start = 0
    while True:
        idx = answer_lower.find(el, start)
        if idx < 0:
            return False
        seg = answer_lower[idx: idx + len(el) + window]
        if _MAGNITUDE_VALUE_RE.search(seg):
            return True
        start = idx + len(el)


# 시설 규모/물량 팩트 질의 마커 — 이 단어가 있으면 '특정 시설을 지목한 수치 질의'로 본다.
_MAGNITUDE_FACT_MARKERS = (
    "면적", "연면적", "규모", "세대수", "세대 수", "층수", "층 수", "높이",
    "건폐율", "용적률", "주차대수", "객실수", "병상수",
)
# 시설 카테고리어(식별자 아님) — 고유 시설명 매칭에서 제외해 부분 카테고리 일치로
# 엉뚱한 시설 답이 confident 통과하는 것을 막는다.
_FACILITY_CATEGORY_WORDS = frozenset({
    "공항", "터미널", "빌딩", "센터", "타워", "스타디움", "경기장", "병원", "학교",
    "청사", "역사", "프로젝트", "project", "building", "tower", "center", "면적", "연면적",
})


def assess_team_telegram_answer_readiness(
    query: str,
    agent: str,
    matches: list[dict],
    answer: str = "",
    *,
    local_score_threshold: int = 40,
) -> dict:
    """팀 Telegram 1차 답변을 로컬 지식만으로 보낼 수 있는지 판단한다.

    기존에는 top score 기준만으로 웹 검색 생략 여부를 결정했다. 이 함수는
    score와 함께 운영문서 랭킹, 에이전트 불일치, 답변 노이즈를 같이 보아
    연결된 지식이 실제 질문 답변 품질로 이어지는지 판단한다.
    """
    assessment = assess_knowledge_answer_quality(query, agent, matches, answer)
    top_score = int(assessment.get("top_score", 0) or 0)
    reasons = list(assessment.get("reasons", []))
    if top_score < local_score_threshold:
        reasons.append(f"below-local-threshold:{top_score}<{local_score_threshold}")
    should_search = bool(reasons)
    return {
        **assessment,
        "ok": not should_search,
        "should_search": should_search,
        "reasons": list(dict.fromkeys(reasons)),
        "local_score_threshold": local_score_threshold,
    }


def append_auto_knowledge_gap_log(*, query: str, agent: str, assessment: dict, search_result: str = "") -> None:
    st = _st()
    auto_gap_log = _CURATION_DIR / "auto_knowledge_gap_log.md"
    auto_gap_log.parent.mkdir(parents=True, exist_ok=True)
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry = (
        f"\n\n## 자동 지식 품질 보강 ({now})\n"
        f"- Agent: {agent}\n"
        f"- Query: {st.sanitize_outbound_text(query)}\n"
        f"- Reasons: {', '.join(assessment.get('reasons', [])) or '-'}\n"
        f"- Top: {assessment.get('top_path', '-') or '-'} / score {assessment.get('top_score', '-')}\n"
        f"- Tags: auto-quality,knowledge-gap,self-healing\n\n"
        "### 자동 수집 결과\n"
        f"{st.sanitize_outbound_text(search_result.strip()) if search_result else '자동 수집 결과 없음. 담당 지식베이스 보강 필요.'}\n"
    )
    with open(auto_gap_log, "a", encoding="utf-8") as log_file:
        log_file.write(entry)


def count_gap_occurrences(query: str) -> int:
    """갭 로그에서 동일 질문의 누적 등장 횟수를 반환."""
    auto_gap_log = _CURATION_DIR / "auto_knowledge_gap_log.md"
    if not auto_gap_log.exists():
        return 0
    try:
        text = auto_gap_log.read_text(encoding="utf-8")
    except Exception:
        return 0
    q_norm = query.strip().lower().replace(" ", "")
    count = 0
    for line in text.splitlines():
        if line.startswith("- Query:"):
            logged = line[len("- Query:"):].strip().lower().replace(" ", "")
            if q_norm == logged or (len(q_norm) > 8 and (q_norm in logged or logged in q_norm)):
                count += 1
    return count


def get_persistent_gaps(min_count: int = 3) -> list[dict]:
    """min_count 이상 반복된 미해결 갭 질문 목록 반환."""
    auto_gap_log = _CURATION_DIR / "auto_knowledge_gap_log.md"
    if not auto_gap_log.exists():
        return []
    try:
        text = auto_gap_log.read_text(encoding="utf-8")
    except Exception:
        return []

    agent_map: dict[str, str] = {}
    query_counts: Counter = Counter()
    current_agent = ""
    for line in text.splitlines():
        if line.startswith("- Agent:"):
            current_agent = line[len("- Agent:"):].strip()
        elif line.startswith("- Query:"):
            q = line[len("- Query:"):].strip()
            q_key = q.lower().replace(" ", "")
            query_counts[q_key] += 1
            if q_key not in agent_map:
                agent_map[q_key] = current_agent

    return [
        {"query": k, "count": v, "agent": agent_map.get(k, "unknown")}
        for k, v in query_counts.most_common()
        if v >= min_count
    ]


async def auto_supplement_knowledge_gap(*, update, query: str, agent: str, assessment: dict) -> str:
    st = _st()

    # 이미 2회 이상 검색 시도된 동일 질문은 재검색 생략 → persistent gap 마킹
    prior_count = count_gap_occurrences(query)
    if prior_count >= 2:
        append_auto_knowledge_gap_log(
            query=query, agent=agent, assessment=assessment,
            search_result=(
                f"[PERSISTENT-GAP] 동일 질문 {prior_count}회 검색 후에도 KB에 적합한 답변 없음. "
                "수동 검토 또는 도메인 전문가 입력 필요."
            ),
        )
        return ""

    st.ensure_agent_state("지식큐레이터")
    st.agent_states["지식큐레이터"]["status"] = "Active"
    st.agent_states["지식큐레이터"]["message"] = f"답변 품질 기준 미달 자동 보강 중: {query[:80]}"
    await st.send_state_to_dashboard()

    append_auto_knowledge_gap_log(query=query, agent=agent, assessment=assessment)

    search_prompt = f"{query}\n\n목표: Telegram 1차 답변 품질 보강. 실무 FAQ, 절차, 예시, 주의사항 중심."
    search_result = await _search_web_for_knowledge(agent, search_prompt)
    if search_result:
        _OPERATIONAL_AGENTS = {"지식업데이트", "지식큐레이터"}
        if agent in st.KNOWLEDGE_AGENTS and agent not in _OPERATIONAL_AGENTS:
            save_agent = agent
        else:
            # 추론 실패 시 검색 top 파일의 에이전트로 역매핑(엉뚱한 KB 오염 방지)
            save_agent = resolve_save_agent(query)
        candidate_update = st.KnowledgeUpdateRequest(
            agent=save_agent,
            title=f"자동 수집: {query[:60]}",
            source="telegram-auto-quality-search" if update else "system-auto-quality-search",
            tags="auto-collect,needs-review",
            content=(
                f"질문: {query}\n\n"
                f"{search_result}\n\n"
                "검토 기준: 공식 문서 여부, 최신성, 프로젝트 적용 가능성 확인 후 FAQ로 승격."
            ),
        )
        candidate_result = st.append_knowledge_update(candidate_update)
        await st.submit_knowledge_approval_candidate(candidate_update, candidate_result, assessment)

    append_auto_knowledge_gap_log(query=query, agent=agent, assessment=assessment, search_result=search_result)
    await st.refresh_obsidian_after_knowledge_update()
    st.agent_states["지식큐레이터"]["status"] = "Idle"
    await st.send_state_to_dashboard()
    return search_result


def build_combined_answer(query: str, search_result: str, local_matches: list[dict]) -> str:
    """웹 검색 결과와 로컬 지식을 합쳐 요약 답변을 만든다."""
    terms = {t.lower() for t in query_terms(query)}
    tavily_ai_answer = ""
    web_answer = ""
    web_url = ""
    best_score = -1

    for block in (search_result or "").split("\n\n"):
        lines = [l.strip() for l in block.strip().splitlines() if l.strip()]
        if not lines:
            continue
        if any("Tavily AI 요약" in l for l in lines):
            content_lines = [l for l in lines if not l.startswith("•") and "Tavily AI 요약" not in l and not l.startswith("출처:")]
            candidate = " ".join(content_lines).strip()
            if candidate:
                tavily_ai_answer = candidate
            continue
        url = next((l.replace("출처:", "").strip() for l in lines if l.startswith("출처:")), "")
        content_lines = [l for l in lines if not l.startswith("•") and not l.startswith("출처:")]
        content = " ".join(content_lines).strip()
        if not content:
            continue
        content_lower = content.lower()
        content_no_space = content_lower.replace(" ", "")
        score = sum(1 for t in terms if t in content_lower or t.replace(" ", "") in content_no_space)
        has_area_unit = any(u in content for u in ("㎡", "만㎡", "천㎡", "평", "바닥면적", "연면적", "전체면적"))
        if has_area_unit:
            score += 3
        first_term = list(terms)[0] if terms else ""
        if first_term and first_term in content_lower[:80]:
            score += 2
        for t in terms:
            if re.search(r'제[2-9]터미널|T[2-9]터미널', content) and t not in content_lower[:60]:
                score -= 2
        if score > best_score:
            best_score = score
            web_answer = content
            web_url = url

    def _is_korean(text: str) -> bool:
        return sum(1 for c in text if '가' <= c <= '힣') > len(text) * 0.1

    if tavily_ai_answer and _is_korean(tavily_ai_answer):
        final_web = tavily_ai_answer
    elif web_answer:
        final_web = web_answer
    else:
        final_web = tavily_ai_answer

    local_excerpt = ""
    if local_matches:
        candidate = local_matches[0]["excerpt"].strip()
        candidate = "\n".join(l for l in candidate.splitlines() if l.strip())
        local_score = sum(1 for t in terms if t in candidate.lower())
        # 매치 점수가 품질 임계(_WEAK_LOCAL_SCORE) 미만이면 off-topic/thin 약매칭이다. 웹 실패 시
        # 이걸 답으로 내보내면 '양자컴퓨터' 질의에 'AI 토큰 최적화' 같은 엉뚱한 답이 나간다.
        match_score = int(local_matches[0].get("score", 0))
        # 시설 규모 팩트 질의인데 발췌가 질의 시설을 (수치와 함께) 커버하지 않으면 폴백
        # 금지 — 웹 다운 시 '성수 K-project 면적'에 인천공항 발췌(고득점)를 다시 내보내는
        # 것을 막는다(readiness named-entity-not-covered 가드와 동일 기준).
        entity_uncovered = False
        if any(m in query.lower() for m in _MAGNITUDE_FACT_MARKERS):
            ents = [
                t for t in extract_topic_terms(query)
                if t not in _MAGNITUDE_FACT_MARKERS and t not in _FACILITY_CATEGORY_WORDS
                and not t.isdigit() and len(t) >= 2
            ]
            if ents and not any(_entity_has_magnitude_nearby(candidate.lower(), t) for t in ents):
                entity_uncovered = True
        if local_score >= 1 and len(candidate) > 20 and match_score >= _WEAK_LOCAL_SCORE and not entity_uncovered:
            local_excerpt = candidate[:600]

    st = _st()
    # 웹/로컬 본문의 마크다운(##/```/**)을 고객 노출 전 정리한다(build_knowledge_answer 와 동일 규칙).
    # qwen 합성이 ollama 다운으로 미적용될 때 이 결과가 그대로 고객 답변이 되므로 노이즈를 막는다.
    if not final_web and local_excerpt:
        return st.sanitize_outbound_text(st.clean_markdown_for_display(local_excerpt[:3600]))
    if not final_web and not local_excerpt:
        return st.sanitize_outbound_text(f"'{query}'에 대한 답변을 찾지 못했습니다.")

    body = final_web[:800]
    if local_excerpt and local_excerpt not in final_web and len(local_excerpt) > 30:
        local_terms_hit = sum(1 for t in terms if t in local_excerpt.lower())
        if local_terms_hit >= 2:
            body += f"\n\n📚 저장된 지식:\n{local_excerpt[:400]}"
    if web_url and not tavily_ai_answer:
        body += f"\n\n출처: {web_url}"
    return st.sanitize_outbound_text(st.clean_markdown_for_display(body[:3600]))


def build_more_research_answer(query: str, agent: str, search_result: str, matches: list[dict]) -> str:
    st = _st()
    if not search_result:
        return st.sanitize_outbound_text(
            f"'{query}'에 대한 답변을 찾지 못했습니다. 지식 공백으로 기록했습니다."
        )
    query_terms_lower = {t.lower() for t in query_terms(query)}
    best_content = ""
    best_url = ""
    best_score = -1
    for block in search_result.split("\n\n"):
        lines = [l.strip() for l in block.strip().splitlines() if l.strip()]
        if not lines:
            continue
        url = ""
        content_lines = []
        for line in lines:
            if line.startswith("출처:"):
                url = line.replace("출처:", "").strip()
            elif not line.startswith("•"):
                content_lines.append(line)
        content = " ".join(content_lines).strip()
        if not content:
            continue
        score = sum(1 for t in query_terms_lower if t in content.lower())
        if score > best_score:
            best_score = score
            best_content = content
            best_url = url
    if not best_content:
        first_block = search_result.split("\n\n")[0]
        lines = [l.strip() for l in first_block.splitlines() if l.strip() and not l.startswith("•") and not l.startswith("출처:")]
        best_content = " ".join(lines)
    answer = best_content[:800]
    if best_url:
        answer += f"\n\n출처: {best_url}"
    # 웹 결과의 마크다운(##/```/**)을 고객 노출 전 정리(다른 답변 빌더와 동일 규칙).
    return st.sanitize_outbound_text(st.clean_markdown_for_display(answer[:3600]))
