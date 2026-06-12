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

import datetime
import os
import re
from collections import Counter
from pathlib import Path

from backend.core.paths import DATA_DIR as _DATA_DIR, PROJECT_ROOT as _PROJECT_ROOT
from backend.web_search import _search_web_for_knowledge

# ---------------------------------------------------------------------------
# 운영 파일 제외 목록 (지식 검색 대상에서 제외)
# ---------------------------------------------------------------------------
_EXCLUDED_KNOWLEDGE_STEMS = {"지식업데이트", "지식큐레이터", "지식업데이트md", "지식큐레이터md"}

def _st():
    """server_total 지연 임포트 헬퍼 — 순환 참조 방지."""
    import backend.server_total as _mod
    return _mod


def knowledge_search_files() -> list[Path]:
    roots = [
        _DATA_DIR / "knowledge_base",
        _PROJECT_ROOT / "docs",
        _PROJECT_ROOT / "obsidian_vaults" / "model_quality_auditor",
    ]
    excluded_parts = {
        "knowledge_updates",
        "knowledge_intake",
        "Team_Telegram_QA",
        "Revit_Assistant_QA",
        "__pycache__",
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
    stopwords = {
        "으로", "에서", "대한", "관련", "정리", "알려줘", "해주세요", "기준", "질문", "요청",
        "지식질문", "말고", "또", "뭐가", "있을까", "있는지", "종류", "유체",
        "하는", "하게", "확인해야", "기본", "답변을",
        "얼마야", "얼마예요", "얼마나", "얼마임", "알려줘", "뭐야", "뭐임", "무엇", "어떻게",
        "어떤", "있어", "있나요", "인가요", "인지", "할까", "해야", "돼요", "됩니까",
    }
    terms = []
    for term in raw_terms:
        if term in stopwords:
            continue
        normalized = term
        for suffix in ("이야", "이에요", "이다", "에서", "에는", "으로", "가", "이", "을", "를", "은", "는", "야", "이랑", "도"):
            if normalized.endswith(suffix) and len(normalized) > len(suffix) + 1:
                normalized = normalized[: -len(suffix)]
                break
        if normalized and normalized not in stopwords:
            terms.append(normalized)
    if any(term in raw_terms for term in ["cws", "cwr", "cw"]):
        terms.extend(["냉각수", "condenser", "water"])
    if any(term in raw_terms for term in ["chws", "chwr", "chw"]):
        terms.extend(["냉수", "chilled", "water"])
    if any(term in raw_terms for term in ["hws", "hwr", "hw"]):
        terms.extend(["온수", "난방", "hot", "water"])
    if "공조배관" in raw_terms:
        terms.extend(["냉수", "온수", "냉각수", "냉매", "증기", "응축수"])
    if any(term in raw_terms for term in ["위생배관", "위생"]):
        terms.extend(["급탕환수", "오배수", "통기", "우수", "sanitary", "vent", "storm"])
    if any("트레이" in term or "케이블" in term for term in raw_terms):
        terms.extend(["트레이", "케이블", "강전", "약전", "이격", "곡률", "충전율"])
    if any("revit" in term or "addin" in term or "add-in" in term for term in raw_terms):
        terms.extend(["revit", "addin", "add-in", "assistant", "knowledge-gateway", "obsidian"])
    if any(term in terms for term in ["다이나모", "dynamo"]):
        terms.extend(["dynamo", "다이나모", "categories", "all elements of category", "python",
                       "filteredelementcollector", "selection", "setelementids"])
    if any(term in terms for term in ["폴더", "하위", "패밀리", "배치"]):
        terms.extend(["folder", "family", "loadfamily", "newfamilyinstance", "directory", "rfa",
                       "패밀리", "로드", "배치"])
    return list(dict.fromkeys(terms))[:20]


def score_knowledge_text(text: str, terms: list[str]) -> int:
    lower = text.lower()
    score = 0
    for term in terms:
        hits = lower.count(term)
        if hits:
            score += min(hits, 6)
    return score


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
        "- source:", "- tags:", "출처: http", "출처: https",
        "자동 수집:", "auto-collect", "needs-review",
        "• [", "질문: ",
    )

    def clean_paragraph(paragraph: str) -> str:
        lines = paragraph.splitlines()
        kept = [l for l in lines if not any(n in l.lower() for n in line_noise)]
        return "\n".join(kept).strip()

    curated_paragraphs = [clean_paragraph(p) for p in paragraphs]
    curated_paragraphs = [p for p in curated_paragraphs if p]
    paragraphs = curated_paragraphs or paragraphs
    if not paragraphs:
        return content[:max_chars]
    query_lower = query.lower()
    wants_legal = any(keyword in query_lower for keyword in ["법", "법규", "고시", "ks", "기준서", "근거문서", "인허가"])
    wants_type = any(keyword in query_lower for keyword in ["종류", "유체", "계통", "분류", "말고", "약어"])
    wants_family_placement = any(keyword in query_lower for keyword in ["폴더", "하위", "패밀리", "배치", "loadfamily", "rfa"])

    def paragraph_score(paragraph: str) -> int:
        lower = paragraph.lower()
        score = score_knowledge_text(paragraph, terms)
        if wants_type and any(keyword in lower for keyword in ["기본 분류", "역할·유체", "유체 약어", "종류", "말고 다른"]):
            score += 18
        if "빠른 답변" in lower:
            score += 40
        if wants_family_placement:
            if any(keyword in lower for keyword in ["폴더 하위", "패밀리 로드", "패밀리", "loadfamily", "newfamilyinstance", ".rfa"]):
                score += 50
            if any(keyword in lower for keyword in ["카테고리 객체", "일괄 선택", "all elements of category", "setelementids"]):
                score -= 30
        if any(keyword in query_lower for keyword in ["revit", "addin", "add-in", "애드인"]) and any(keyword in lower for keyword in ["revit assistant", "지식 게이트웨이", "knowledge-gateway", "설비 bim 근거", "lua bim labs"]):
            score += 25
        if "설비 질문" in query_lower and any(keyword in lower for keyword in ["revit assistant", "지식 베이스", "설비 bim", "obsidian"]):
            score += 18
        if any(keyword in lower for keyword in ["faq", "답변 포인트", "물 때:"]):
            score += 8
        if "## " in paragraph[:12] or paragraph.startswith("# "):
            score += 3
        if not wants_legal and any(keyword in lower for keyword in ["국내 법령", "국내 고시", "ks 규격", "국내 표준", "국제 기준", "법률 제", "시행규칙"]):
            score -= 22
        return score

    ranked = sorted(
        ((paragraph_score(paragraph), index, paragraph) for index, paragraph in enumerate(paragraphs)),
        key=lambda item: (item[0], -item[1]),
        reverse=True,
    )
    selected_limit = 1 if wants_family_placement else 2
    selected = [paragraph for score, _, paragraph in ranked[:selected_limit] if score > 0] or [paragraphs[0]]
    excerpt = "\n\n".join(selected)
    return excerpt[:max_chars].strip()


def search_local_knowledge(query: str, limit: int = 4) -> list[dict]:
    terms = query_terms(query)
    if not terms:
        return []
    inferred_agent = infer_knowledge_agent_from_query(query)
    matches = []
    for path in knowledge_search_files():
        try:
            content = path.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        score = score_knowledge_text(content, terms)
        try:
            rel = path.relative_to(_PROJECT_ROOT).as_posix()
        except ValueError:
            rel = path.as_posix()
        if rel.startswith("data/knowledge_base/"):
            score += 8
        if path.stem == inferred_agent:
            score += 20
        elif inferred_agent in path.stem:
            score += 10
        if any(term in path.stem.lower() for term in terms):
            score += 8
        if "curation" in rel.lower() or "daily_knowledge" in rel.lower():
            score -= 30
        if score <= 0:
            continue
        matches.append({
            "score": score,
            "path": path,
            "excerpt": extract_relevant_excerpt(content, terms, query=query),
        })
    return sorted(matches, key=lambda item: item["score"], reverse=True)[:limit]


def prioritize_agent_matches(matches: list[dict], agent: str) -> list[dict]:
    if not matches:
        return matches

    def rank(match: dict) -> tuple[int, int]:
        path = match.get("path")
        stem = path.stem if isinstance(path, Path) else ""
        agent_hit = 1 if stem == agent else 0
        return (agent_hit, int(match.get("score", 0)))

    return sorted(matches, key=rank, reverse=True)


def infer_knowledge_agent_from_query(query: str) -> str:
    st = _st()
    lower_text = query.lower()
    if any(keyword in lower_text for keyword in ["revit", "add-in", "addin", "애드인"]):
        return "Revit_Addin"
    if any(keyword in lower_text for keyword in ["다이나모", "dynamo"]):
        return "Dynamo"
    if any(keyword in lower_text for keyword in ["navisworks", "나비스웍스"]):
        return "Navisworks_Addin"
    if any(keyword in lower_text for keyword in ["도면", "계통도", "장비일람표", "부하계산서", "범례"]):
        if any(keyword in lower_text for keyword in ["cws", "cwr", "냉각수", "냉수", "온수", "냉매", "공조배관"]):
            return "공조배관"
        return "설비도면해석"
    if any(keyword in lower_text for keyword in ["cws", "cwr", "chws", "chwr", "hws", "hwr", "냉각수", "냉수", "냉매"]):
        return "공조배관"
    for agent, keywords in st.DISCIPLINE_KEYWORDS.items():
        if any(keyword.lower() in lower_text for keyword in keywords):
            return agent
    for agent in st.KNOWLEDGE_AGENTS:
        if agent.lower() in lower_text:
            return agent
    if any(keyword in lower_text for keyword in ["교육", "커리큘럼", "온보딩", "연차"]):
        return "교육컨설팅"
    if any(keyword in lower_text for keyword in ["개발", "코드", "qwen", "api", "addin", "revit", "navisworks"]):
        return "프로그램개발"
    return "지식업데이트"


def build_knowledge_answer(query: str, matches: list[dict]) -> str:
    if not matches:
        return ""
    return _st().sanitize_outbound_text(matches[0]["excerpt"][:3600])


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
    if top_score and top_score < 18:
        reasons.append(f"low-score:{top_score}")
    if agent and agent in st.KNOWLEDGE_AGENTS and top_stem and top_stem != agent:
        if agent in {"Dynamo", "Revit_Addin", "Navisworks_Addin"}:
            reasons.append(f"agent-mismatch:{top_stem}")
        elif top_stem in {"지식업데이트", "지식큐레이터", "인프라_DevOpsObsidian"}:
            reasons.append(f"operational-doc-ranked:{top_stem}")
    if top_stem in {"지식업데이트", "지식큐레이터"} and not any(term in query_lower for term in ["지식", "큐레이션", "업데이트"]):
        reasons.append(f"operational-doc-ranked:{top_stem}")
    if any(noise in answer_lower for noise in ["현재 보유 지식에서 충분히", "| 문서 | 유형 | 권고 |", "daily_knowledge_curation"]):
        reasons.append("answer-noise")
    if any(term in query_lower for term in ["다이나모", "dynamo"]) and "dynamo" not in top_stem.lower():
        reasons.append(f"dynamo-not-ranked:{top_stem or '-'}")

    return {
        "ok": not reasons,
        "reasons": reasons,
        "top_score": top_score,
        "top_path": str(top_path.relative_to(_PROJECT_ROOT)) if isinstance(top_path, Path) else "",
    }


def append_auto_knowledge_gap_log(*, query: str, agent: str, assessment: dict, search_result: str = "") -> None:
    st = _st()
    auto_gap_log = _DATA_DIR / "knowledge_quality" / "auto_knowledge_gap_log.md"
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
    auto_gap_log = _DATA_DIR / "knowledge_quality" / "auto_knowledge_gap_log.md"
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
    auto_gap_log = _DATA_DIR / "knowledge_quality" / "auto_knowledge_gap_log.md"
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
        save_agent = agent if agent in st.KNOWLEDGE_AGENTS and agent not in _OPERATIONAL_AGENTS else infer_knowledge_agent_from_query(query)
        if save_agent in _OPERATIONAL_AGENTS:
            save_agent = "건축"
        st.append_knowledge_update(st.KnowledgeUpdateRequest(
            agent=save_agent,
            title=f"자동 수집: {query[:60]}",
            source="telegram-auto-quality-search" if update else "system-auto-quality-search",
            tags="auto-collect,needs-review",
            content=(
                f"질문: {query}\n\n"
                f"{search_result}\n\n"
                "검토 기준: 공식 문서 여부, 최신성, 프로젝트 적용 가능성 확인 후 FAQ로 승격."
            ),
        ))

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
        if local_score >= 1 and len(candidate) > 20:
            local_excerpt = candidate[:600]

    st = _st()
    if not final_web and local_excerpt:
        return st.sanitize_outbound_text(local_excerpt[:3600])
    if not final_web and not local_excerpt:
        return st.sanitize_outbound_text(f"'{query}'에 대한 답변을 찾지 못했습니다.")

    body = final_web[:800]
    if local_excerpt and local_excerpt not in final_web and len(local_excerpt) > 30:
        local_terms_hit = sum(1 for t in terms if t in local_excerpt.lower())
        if local_terms_hit >= 2:
            body += f"\n\n📚 저장된 지식:\n{local_excerpt[:400]}"
    if web_url and not tavily_ai_answer:
        body += f"\n\n출처: {web_url}"
    return st.sanitize_outbound_text(body[:3600])


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
    return st.sanitize_outbound_text(answer[:3600])
