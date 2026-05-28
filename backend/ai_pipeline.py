"""
SECTION 8 ── AI 스트리밍 · DeepSeek 예산 · 기업 파이프라인
  [AI 스트리밍 헬퍼]
  - _extract_agent_name, _parse_sections, _score_and_pick, _compose_knowledge_response
  - stream_claude (Claude API 스트리밍, Tavily 툴 포함)
  - infer_target_agent (라우팅 대상 에이전트 추론)
  [DeepSeek 예산 관리]
  - current_budget_month, load/save_deepseek_budget_registry
  - deepseek_month_usage, deepseek_budget_remaining, can_use_deepseek_budget
  - record_deepseek_budget_use
  [AI 실행 정책]
  - should_use_paid_ai, ai_execution_policy_summary
  [기업 파이프라인 핵심]
  - process_corporate_pipeline (CEO → PM → 실무팀 지휘 체계)
"""
from __future__ import annotations

import asyncio
import datetime
import json
import os
import re

from backend.core.paths import DATA_DIR as _DATA_DIR
from backend.web_search import (
    _build_search_query,
    _save_search_result_to_knowledge,
    _search_web_for_knowledge,
    _KNOWLEDGE_MIN_CHARS,
)
from backend.text_utils import append_korean_response_instruction, enforce_korean_answer

# ---------------------------------------------------------------------------
# DeepSeek 예산 경로 상수 (server_total과 동일 계산)
# ---------------------------------------------------------------------------
_DEEPSEEK_BUDGET_FILE = _DATA_DIR / "ai_usage" / "deepseek_monthly_budget.json"
_DEEPSEEK_MONTHLY_BUDGET_USD = float(os.environ.get("DEEPSEEK_MONTHLY_BUDGET_USD", "50"))
_DEEPSEEK_ESTIMATED_CALL_COST_USD = float(os.environ.get("DEEPSEEK_ESTIMATED_CALL_COST_USD", "0.35"))

# ---------------------------------------------------------------------------
# AI 실행 정책 상수
# ---------------------------------------------------------------------------
LOCAL_ONLY_WORKFLOW_IDS = {
    "support_general", "license_billing", "privacy_security", "knowledge_update",
    "resume_analysis_dashboard", "excel_qwen_automation", "expense_receipt_intake",
    "local_qwen_development", "employee_onboarding_training", "docs_release", "build_qa",
}

DEEPSEEK_CANDIDATE_WORKFLOW_IDS = {
    "pricing_revenue", "store_release", "requirements_scope",
    "daily_idea_report", "idea_to_product_development_queue", "packaging_install",
}

LOCAL_ONLY_AGENTS = {
    "고객지원 CS", "CS_기술지원관", "라이선스결제", "라이선스_보안관", "법무조항검토",
    "지식업데이트", "지식큐레이터", "경영지원", "경비정산_AI", "HR_인재분석관",
    "엑셀자동화", "Qwen_Coder_8B", "인프라_DevOps (Obsidian)", "교육컨설팅",
    "러닝콘텐츠디자이너", "QA_테스터", "빌드검증", "배포문서",
}

DEEPSEEK_CANDIDATE_AGENTS = {
    "CEO", "COO", "CFO", "조율차장", "전략기획",
    "아이디어발굴", "스토어심사", "견적심사원", "브랜드마케팅", "요구사항분석",
}

PAID_AI_BLOCK_KEYWORDS = [
    "개인정보", "주민", "급여", "연봉", "전화", "휴대폰", "이메일", "메일",
    "고객명", "프로젝트명", "도면", "계약", "계정", "비밀번호", "password",
    "api key", "apikey", "token", "secret", ".env", "ssh", "telegram id", "chat id",
    "/users/", "/volumes/", "내부 경로", "영수증", "증빙", "정산", "카드전표",
    "세금계산서", "거래명세서", "사업자번호",
    "이력서", "지원자", "후보자", "학력", "출생", "생년", "경력증명", "주요 고객", "이전 회사",
]

PAID_AI_STRATEGIC_KEYWORDS = [
    "전략", "사업성", "가격", "mrr", "손익분기", "상품화", "우선순위", "로드맵",
    "시장", "포지셔닝", "스토어 전략", "수익화", "투자", "비용 구조", "경영 판단",
]


def _st():
    """server_total 지연 임포트 헬퍼 — 순환 참조 방지."""
    import backend.server_total as _mod
    return _mod


def _routing():
    """agent_routing 지연 임포트 헬퍼 — 순환 참조 방지."""
    import backend.agent_routing as _mod
    return _mod


# ---------------------------------------------------------------------------
# Section 8 내부 헬퍼 (stream_claude 전용)
# ---------------------------------------------------------------------------

def _extract_agent_name(system_role: str) -> str:
    bracket_match = re.search(r'\[([^\]]+)\]', system_role)
    if bracket_match:
        return bracket_match.group(1)
    st = _st()
    all_known = list(st.ALL_AGENTS) + list(st.EXTRA_KNOWLEDGE_AGENTS)
    for agent in sorted(all_known, key=len, reverse=True):
        if agent in system_role:
            return agent
    if "CEO" in system_role:
        return "CEO"
    if "조율차장" in system_role or "PM" in system_role:
        return "조율차장"
    return ""


def _parse_sections(knowledge: str) -> list[tuple[str, str]]:
    sections: list[tuple[str, str]] = []
    current_heading = "기본 기준"
    current_lines: list[str] = []
    for line in knowledge.split("\n"):
        if line.startswith("## "):
            body = "\n".join(current_lines).strip()
            if body:
                sections.append((current_heading, body))
            current_heading = line[3:].strip()
            current_lines = []
        elif not line.startswith("# "):
            current_lines.append(line)
    body = "\n".join(current_lines).strip()
    if body:
        sections.append((current_heading, body))
    return sections


def _score_and_pick(sections: list[tuple[str, str]], user_prompt: str) -> list[tuple[int, str, str]]:
    prompt_words = {
        w for w in re.split(r'[\s,./·()\[\]「」『』\-]', user_prompt.lower()) if len(w) > 1
    }
    scored = [
        (sum(1 for w in prompt_words if w in (h + " " + b).lower()), h, b)
        for h, b in sections
    ]
    scored.sort(key=lambda x: -x[0])
    return [s for s in scored if s[0] > 0][:3] or scored[:2]


def _compose_knowledge_response(agent_name: str, user_prompt: str, knowledge: str) -> str:
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    sections = _parse_sections(knowledge)
    if not sections:
        return ""
    top = _score_and_pick(sections, user_prompt)
    sections_text = "\n\n".join(f"▶ {h}\n{b}" for _, h, b in top)
    return (
        f"[{agent_name}] 지식 베이스 기반 검토 ({now})\n\n"
        f"{sections_text}\n\n"
        f"※ 축적 지식 {len(sections)}개 항목 중 관련도 상위 {len(top)}개 추출."
    )


# ---------------------------------------------------------------------------
# DeepSeek 예산 관리
# ---------------------------------------------------------------------------

def current_budget_month() -> str:
    return datetime.datetime.now().strftime("%Y-%m")


def load_deepseek_budget_registry() -> dict:
    if not _DEEPSEEK_BUDGET_FILE.exists():
        return {"monthly_budget_usd": _DEEPSEEK_MONTHLY_BUDGET_USD, "months": {}}
    try:
        registry = json.loads(_DEEPSEEK_BUDGET_FILE.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        registry = {"months": {}}
    registry.setdefault("monthly_budget_usd", _DEEPSEEK_MONTHLY_BUDGET_USD)
    registry.setdefault("months", {})
    return registry


def save_deepseek_budget_registry(registry: dict) -> None:
    _DEEPSEEK_BUDGET_FILE.parent.mkdir(parents=True, exist_ok=True)
    _DEEPSEEK_BUDGET_FILE.write_text(
        json.dumps(registry, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def deepseek_month_usage(month: str | None = None) -> float:
    month = month or current_budget_month()
    registry = load_deepseek_budget_registry()
    month_data = registry.get("months", {}).get(month, {})
    return float(month_data.get("estimated_spend_usd", 0.0))


def deepseek_budget_remaining(month: str | None = None) -> float:
    registry = load_deepseek_budget_registry()
    budget = float(registry.get("monthly_budget_usd", _DEEPSEEK_MONTHLY_BUDGET_USD))
    return round(max(budget - deepseek_month_usage(month), 0.0), 4)


def can_use_deepseek_budget(estimated_cost: float | None = None) -> bool:
    estimated = estimated_cost if estimated_cost is not None else _DEEPSEEK_ESTIMATED_CALL_COST_USD
    return deepseek_budget_remaining() >= estimated


def record_deepseek_budget_use(*, workflow_id: str, target_agent: str, estimated_cost: float | None = None) -> None:
    month = current_budget_month()
    estimated = round(float(estimated_cost if estimated_cost is not None else _DEEPSEEK_ESTIMATED_CALL_COST_USD), 4)
    registry = load_deepseek_budget_registry()
    months = registry.setdefault("months", {})
    month_data = months.setdefault(month, {"estimated_spend_usd": 0.0, "calls": []})
    month_data["estimated_spend_usd"] = round(float(month_data.get("estimated_spend_usd", 0.0)) + estimated, 4)
    month_data.setdefault("calls", []).append({
        "timestamp": datetime.datetime.now().isoformat(timespec="seconds"),
        "workflow_id": workflow_id,
        "target_agent": target_agent,
        "estimated_cost_usd": estimated,
    })
    save_deepseek_budget_registry(registry)


# ---------------------------------------------------------------------------
# AI 스트리밍
# ---------------------------------------------------------------------------

async def stream_claude(system_role: str, user_prompt: str, allow_web_search: bool = True):
    """지식 베이스 우선 → 부족하면 웹 검색 폴백 → 결과 자동 저장 후 스트리밍."""
    st = _st()
    agent_name = _extract_agent_name(system_role)
    knowledge = st.read_agent_knowledge(agent_name) if agent_name else ""
    composed = _compose_knowledge_response(agent_name, user_prompt, knowledge) if len(knowledge) >= _KNOWLEDGE_MIN_CHARS else ""

    if not composed and allow_web_search:
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        yield f"[{agent_name}] 지식 베이스 부족 → 웹 검색 중... "
        await asyncio.sleep(0.1)
        search_result = await _search_web_for_knowledge(agent_name, user_prompt)
        if search_result:
            query = _build_search_query(agent_name, user_prompt)
            _save_search_result_to_knowledge(agent_name, query, search_result)
            composed = (
                f"[{agent_name}] 웹 검색 결과 ({now}) — 지식 베이스에 자동 저장됨\n\n"
                f"{search_result}\n\n"
                f"※ 이 내용은 지식 베이스에 저장되어 다음 요청부터 즉시 활용됩니다."
            )
        else:
            composed = (
                f"[{agent_name}] 지식 베이스 및 웹 검색 모두 결과 없음 ({now}).\n"
                f"/api/knowledge-update 로 직접 지식을 추가해주세요."
            )
    elif not composed:
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        composed = (
            f"[{agent_name}] 로컬 지식 베이스 기반 응답 ({now})\n\n"
            "일반 CS 문의는 API 토큰 소모 없이 처리하도록 설정되어 있습니다. "
            "현재 담당 지식 베이스의 내용이 부족하므로, FAQ/응답 템플릿을 보강하면 더 정확히 답변할 수 있습니다."
        )

    for word in composed.split(" "):
        await asyncio.sleep(0.04)
        yield word + " "


# ---------------------------------------------------------------------------
# 에이전트 타겟 추론 (기업 파이프라인 라우팅)
# ---------------------------------------------------------------------------

def infer_target_agent(user_text: str) -> str:
    """문맥에서 타겟 실무 부서를 추출합니다."""
    st = _st()
    rt = _routing()
    lower_text = user_text.lower()
    if any(keyword in lower_text for keyword in ["노트북lm", "notebooklm", "슬라이드", "ppt", "강의안", "퀴즈", "교육 콘텐츠", "교육콘텐츠", "학습자료", "강의자료"]):
        return "러닝콘텐츠디자이너"
    if any(keyword in lower_text for keyword in ["교육", "온보딩", "신규 직원", "신입", "연차별", "커리큘럼", "l&d", "learning", "멘토링", "직무교육"]):
        return "교육컨설팅"
    intent = rt.infer_request_intent(user_text)
    if intent == "support":
        return "고객지원 CS"
    if any(keyword in lower_text for keyword in ["문 위치", "문짝", "문틀", "door"]):
        return "건축"
    if any(keyword in lower_text for keyword in ["개인정보", "privacy", "보안", "api key", "토큰", "외부 통신", "데이터 전송", "모델 데이터"]):
        return "라이선스_보안관"
    if any(keyword in lower_text for keyword in ["이력서", "resume", "cv", "지원자", "후보자", "채용", "서류 검토", "서류심사", "인재 평가", "인재평가", "경력 분석", "경력 대시보드", "평가 보고서"]):
        return "HR_인재분석관"
    if any(keyword in lower_text for keyword in ["영수증", "증빙", "경비", "비용 정산", "비용정산", "정산", "세금계산서", "거래명세서", "카드전표", "receipt", "expense"]):
        return "경비정산_AI"
    if any(keyword in lower_text for keyword in ["가격", "mrr", "매출", "손익분기", "사업성", "구독 가격"]):
        return "CFO"
    if any(keyword in lower_text for keyword in ["엑셀", "excel", "xlsx", "csv", "openxml", "워크북", "시트", "리포트 자동화", "보고서 자동화"]):
        return "엑셀자동화"
    if any(keyword in lower_text for keyword in ["qwen", "로컬 코더", "로컬 1차", "개발 업무", "업무지시", "일반 코드", "리팩토링"]):
        return "프로그램개발"
    target_agent = "Revit_Addin" if any(keyword in lower_text for keyword in ["revit", "레빗"]) else "공조배관"
    if any(keyword in lower_text for keyword in ["navisworks", "navis", "나비스웍스", "나비스"]):
        target_agent = "Navisworks_Addin"
    if any(keyword in lower_text for keyword in ["배포", "설치", "installer", "addin manifest", ".addin"]):
        target_agent = "배포문서"
    if any(keyword in lower_text for keyword in ["test", "테스트", "qa", "검증", "빌드"]):
        target_agent = "빌드검증"
    if any(keyword in lower_text for keyword in ["요구사항", "기획", "명세", "spec"]):
        target_agent = "요구사항분석"
    if any(keyword in lower_text for keyword in ["autodesk store", "app store", "스토어", "심사", "판매", "출시", "submit", "submission"]):
        target_agent = "스토어심사"
    if any(keyword in lower_text for keyword in ["installer", "msi", "패키징", "설치파일", "bundle", "배포 패키지"]):
        target_agent = "제품패키징"
    if any(keyword in lower_text for keyword in ["license", "licensing", "entitlement", "구독", "결제", "paypal", "bluesnap"]):
        target_agent = "라이선스결제"
    if any(keyword in lower_text for keyword in ["privacy", "개인정보", "support", "지원", "고객지원", "환불", "문의"]):
        target_agent = "고객지원 CS"
    for agent in st.ALL_AGENTS:
        if agent in user_text:
            target_agent = agent
            break
    return target_agent


# ---------------------------------------------------------------------------
# AI 실행 정책
# ---------------------------------------------------------------------------

def contains_paid_ai_blocked_signal(user_text: str) -> bool:
    lower_text = user_text.lower()
    return any(keyword.lower() in lower_text for keyword in PAID_AI_BLOCK_KEYWORDS)


def should_use_paid_ai(target_agent: str, user_text: str, workflow: dict | None = None) -> bool:
    """DeepSeek API는 전략/상품화 판단에만 제한적으로 사용한다."""
    st = _st()
    if not st.PAID_AI_ENABLED:
        return False
    if contains_paid_ai_blocked_signal(user_text):
        return False
    if not can_use_deepseek_budget():
        return False
    workflow_id = workflow.get("id") if workflow else ""
    if workflow_id in LOCAL_ONLY_WORKFLOW_IDS:
        return False
    if target_agent in LOCAL_ONLY_AGENTS:
        return False
    if workflow_id in DEEPSEEK_CANDIDATE_WORKFLOW_IDS:
        return True
    if target_agent in DEEPSEEK_CANDIDATE_AGENTS:
        lower_text = user_text.lower()
        return any(keyword in lower_text for keyword in PAID_AI_STRATEGIC_KEYWORDS)
    return False


def ai_execution_policy_summary(target_agent: str, user_text: str, workflow: dict | None = None, force_local_only: bool = False) -> dict:
    st = _st()
    if force_local_only:
        return {"mode": "local_only", "reason": "팀원/관리팀 또는 명시적 로컬 전용 요청"}
    if not st.PAID_AI_ENABLED:
        return {"mode": "local_only", "reason": "PAID_AI_ENABLED 비활성화"}
    if contains_paid_ai_blocked_signal(user_text):
        return {"mode": "local_only", "reason": "민감정보/내부정보 신호 감지"}
    remaining = deepseek_budget_remaining()
    if not can_use_deepseek_budget():
        return {"mode": "local_only", "reason": f"월 DeepSeek 예산 잔액 부족 (${remaining:.2f} 남음)"}
    workflow_id = workflow.get("id") if workflow else ""
    if workflow_id in LOCAL_ONLY_WORKFLOW_IDS:
        return {"mode": "local_only", "reason": f"{workflow_id} 워크플로우는 로컬 전용"}
    if target_agent in LOCAL_ONLY_AGENTS:
        return {"mode": "local_only", "reason": f"{target_agent} 담당 업무는 로컬 전용"}
    if should_use_paid_ai(target_agent, user_text, workflow):
        return {"mode": "deepseek_allowed", "reason": f"전략/상품화/사업성 판단 후보, 월 예산 잔액 약 ${remaining:.2f}"}
    return {"mode": "local_first", "reason": "로컬 처리 후 필요 시 관리자 판단"}


# ---------------------------------------------------------------------------
# 기업 파이프라인 (CEO → PM → 실무팀 지휘 체계)
# ---------------------------------------------------------------------------

async def process_corporate_pipeline(user_text, reply_msg, force_local_only: bool = False, deliver_full_result: bool = False):
    st = _st()
    rt = _routing()
    import backend.collaboration as collaboration

    st.current_active_agent = "조율차장"
    request_intent = rt.infer_request_intent(user_text)
    if request_intent == "ambiguous":
        st.agent_states["조율차장"]["status"] = "Active"
        st.agent_states["조율차장"]["message"] = "요청 의도 확인 대기: 고객 문의 답변인지 개발/기술 검토인지 분류 필요."
        await st.send_state_to_dashboard()
        await reply_msg.edit_text(rt.intent_confirmation_message(user_text))
        st.agent_states["조율차장"]["status"] = "Idle"
        await st.send_state_to_dashboard()
        return

    target_agent = infer_target_agent(user_text)
    workflows = st.active_collaboration_workflows()
    workflow = collaboration.select_collaboration_workflow(user_text, target_agent, request_intent, workflows)
    target_agent = collaboration.determine_primary_agent(user_text, target_agent, workflow, request_intent)
    use_paid_ai = should_use_paid_ai(target_agent, user_text, workflow)
    if workflow.get("local_only"):
        use_paid_ai = False
    if force_local_only:
        use_paid_ai = False
    ai_policy = ai_execution_policy_summary(target_agent, user_text, workflow, force_local_only=force_local_only)
    review_agents = rt.infer_discipline_review_agents(user_text) if collaboration.should_run_discipline_review(workflow, target_agent, set(st.DISCIPLINE_KEYWORDS.keys())) else []
    collaboration_participants = rt.build_collaboration_plan(workflow, target_agent, review_agents)
    local_coder_gate = collaboration.local_coder_gate(user_text, workflow)
    if ai_policy["mode"] != "deepseek_allowed":
        local_coder_gate = {
            **local_coder_gate,
            "api_escalation_policy": f"{local_coder_gate['api_escalation_policy']} / AI 배치: {ai_policy['reason']}",
        }
    if force_local_only:
        local_coder_gate = {
            **local_coder_gate,
            "mode": "team_local_qwen_only",
            "qwen_role": "allowed_primary_or_collaborator",
            "api_escalation_policy": "팀원/관리팀 요청은 DeepSeek API를 사용하지 않는다. Qwen Coder와 로컬 지식만 사용한다.",
            "instruction": "최종 결과물은 Mac에 파일로 저장하지 않고 Telegram 회신으로 전달한다.",
        }
    await st.update_reply_progress(
        reply_msg,
        st.build_telegram_progress_report(
            step="1/6 접수 및 라우팅 완료",
            workflow_name=workflow["name"],
            target_agent=target_agent,
            detail="요청 의도 분석 완료. 담당 부서와 협업 팀원을 배정했습니다.",
            participants=collaboration_participants,
        ),
    )

    st.ensure_agent_state("CEO")
    st.current_active_agent = "CEO"
    st.agent_states["CEO"]["status"] = "Active"
    st.agent_states["CEO"]["message"] = f"{workflow['name']} 케이스 접수. 비즈니스 리스크 및 부서 배정 판단 개시."
    await st.send_state_to_dashboard()
    await st.update_reply_progress(
        reply_msg,
        st.build_telegram_progress_report(
            step="2/6 CEO 판단 중",
            workflow_name=workflow["name"],
            target_agent=target_agent,
            detail="제품 가치, 위험도, 우선순위를 검토하고 있습니다.",
            participants=collaboration_participants,
        ),
    )

    ceo_prompt = (
        "당신은 Revit/Navisworks Add-in을 개발하는 BIM 소프트웨어 기업의 CEO입니다. "
        "요청의 제품 가치, 리스크, 개발 우선순위를 판단하고 실무팀에 지시를 내리세요: "
        f"{user_text}"
    )
    ceo_reply = ""
    async for token in stream_claude("LUA BIM LABS CEO", ceo_prompt, allow_web_search=use_paid_ai):
        ceo_reply += token
        st.agent_states["CEO"]["message"] = ceo_reply
        st.agent_states["CEO"]["tokens"] += 1
        await st.send_state_to_dashboard()

    st.agent_states["CEO"]["status"] = "Idle"
    await st.update_reply_progress(
        reply_msg,
        st.build_telegram_progress_report(
            step="3/6 조율차장 배정 중",
            workflow_name=workflow["name"],
            target_agent=target_agent,
            detail="CEO 판단 완료. 조율차장이 실행 순서와 협업 경계를 정리하고 있습니다.",
            participants=collaboration_participants,
        ),
    )
    await asyncio.sleep(1)

    st.current_active_agent = "조율차장"
    st.ensure_agent_state("조율차장")
    st.agent_states["조율차장"]["status"] = "Active"
    st.agent_states["조율차장"]["message"] = f"CEO 지시 수령. [{workflow['name']}] 프로세스로 담당 부서 [{target_agent}] 및 협업 팀원 배정."
    pm_reply = ""
    async for token in stream_claude("총괄 PM 조율차장", f"실무 부서 {target_agent}의 Add-in 개발 작업을 조율하세요.", allow_web_search=use_paid_ai):
        pm_reply += token
        st.agent_states["조율차장"]["message"] = pm_reply
        st.agent_states["조율차장"]["tokens"] += 1
        await st.send_state_to_dashboard()

    st.agent_states["조율차장"]["status"] = "Idle"
    await st.update_reply_progress(
        reply_msg,
        st.build_telegram_progress_report(
            step="4/6 주관 부서 분석 중",
            workflow_name=workflow["name"],
            target_agent=target_agent,
            detail=f"조율차장 검토 완료. [{target_agent}]에서 실무 분석을 진행하고 있습니다.",
            participants=collaboration_participants,
        ),
    )
    await asyncio.sleep(1)

    st.current_active_agent = target_agent
    st.ensure_agent_state(target_agent)
    st.agent_states[target_agent]["status"] = "Active"
    st.agent_states[target_agent]["message"] = f"{workflow['name']} 주관 검토 시작."
    final_solution = ""
    deepseek_used = False
    system_role = (
        append_korean_response_instruction(
            f"당신은 LUA BIM LABS의 [{target_agent}] 전문 개발 엔지니어입니다. "
            "Autodesk 공식 Revit/Navisworks API 제약을 존중하고, C#/.NET Add-in 구조, manifest, "
            "빌드/배포/테스트 관점까지 포함해 실행 가능한 개발안을 작성하세요. "
            "상용 판매 예정 제품은 Autodesk App Store 심사, 설치 경험, 개인정보/지원 정책, 결제/라이선스 리스크도 함께 검토하세요."
        )
    )

    try:
        if not use_paid_ai:
            raise RuntimeError("일반 CS 문의: API 토큰 무소모 로컬 응답 모드")
        if not st.DEEPSEEK_API_KEY or st.DEEPSEEK_API_KEY == "sk-fake-key-for-test":
            raise RuntimeError("DEEPSEEK_API_KEY 미설정: 로컬 백업 스트리밍으로 전환")
        response = await st.deepseek_client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": system_role},
                {"role": "user", "content": user_text}
            ],
            stream=True
        )
        async for chunk in response:
            t = chunk.choices[0].delta.content
            if t:
                deepseek_used = True
                final_solution += t
                st.agent_states[target_agent]["message"] = final_solution
                st.agent_states[target_agent]["tokens"] += 1
                await st.send_state_to_dashboard()
        if deepseek_used:
            record_deepseek_budget_use(workflow_id=workflow["id"], target_agent=target_agent)
    except Exception:
        async for token in stream_claude(system_role, user_text, allow_web_search=use_paid_ai):
            final_solution += token
            st.agent_states[target_agent]["message"] = final_solution
            st.agent_states[target_agent]["tokens"] += 1
            await st.send_state_to_dashboard()

    st.agent_states[target_agent]["status"] = "Idle"
    await st.update_reply_progress(
        reply_msg,
        st.build_telegram_progress_report(
            step="5/6 협업 팀원 검토 중",
            workflow_name=workflow["name"],
            target_agent=target_agent,
            detail="주관 부서 분석 완료. Qwen/QA/빌드/문서 담당 검토를 순차 진행합니다.",
            participants=collaboration_participants,
        ),
    )

    collaboration_reports = []
    pending_collaborators = [
        collaborator for collaborator in collaboration_participants
        if collaborator not in {"CEO", "조율차장", target_agent} and collaborator not in review_agents
    ]
    for index, collaborator in enumerate(pending_collaborators, start=1):
        await st.update_reply_progress(
            reply_msg,
            st.build_telegram_progress_report(
                step=f"5/6 협업 팀원 검토 중 ({index}/{len(pending_collaborators)})",
                workflow_name=workflow["name"],
                target_agent=target_agent,
                detail=f"[{collaborator}] 검토를 진행하고 있습니다.",
                participants=collaboration_participants,
            ),
        )
        report = await rt.run_collaboration_stage(collaborator, workflow, user_text, allow_web_search=False)
        collaboration_reports.append(report)

    review_reports = []
    knowledge_context = st.build_knowledge_context(review_agents)
    for review_agent in review_agents:
        st.ensure_agent_state(review_agent)
        st.current_active_agent = review_agent
        st.agent_states[review_agent]["status"] = "Active"
        st.agent_states[review_agent]["message"] = f"{target_agent} 개발안에 대한 {review_agent} 공정 지식 검토 시작."
        await st.send_state_to_dashboard()
        review_prompt = (
            f"개발 대상: {target_agent}\n사용자 요청:\n{user_text}\n\n"
            f"공정별 업데이트 지식 베이스:\n{knowledge_context or '저장된 지식 없음'}\n\n"
            f"{review_agent} 공정 관점에서 Add-in 요구사항에 반드시 반영해야 할 데이터, 예외 조건, "
            "검토 로직, UI 경고, 보고서 항목을 짧고 실행 가능하게 제안하세요."
        )
        review_text = ""
        async for token in stream_claude(f"{review_agent} 공정 지식 검토관", review_prompt, allow_web_search=use_paid_ai):
            review_text += token
            st.agent_states[review_agent]["message"] = review_text
            st.agent_states[review_agent]["tokens"] += 1
            await st.send_state_to_dashboard()
        st.agent_states[review_agent]["status"] = "Idle"
        review_reports.append(f"[{review_agent} 검토 의견]\n{review_text.strip()}")

    st.current_active_agent = "조율차장"
    st.agent_states["조율차장"]["status"] = "Active"
    await st.update_reply_progress(
        reply_msg,
        st.build_telegram_progress_report(
            step="6/6 최종 보고서 병합 중",
            workflow_name=workflow["name"],
            target_agent=target_agent,
            detail="각 AI 팀원 의견을 병합하고 텔레그램 요약 보고를 작성하고 있습니다.",
            participants=collaboration_participants,
        ),
    )
    workflow_section = collaboration.build_workflow_summary(workflow, collaboration_participants, use_paid_ai)
    collaboration_section = "\n\n".join(collaboration_reports) if collaboration_reports else "추가 협업 팀원 의견 없음."
    boundary_section = collaboration.build_role_boundary_summary(collaboration_participants)
    discipline_section = "\n\n".join(review_reports) if review_reports else "지정된 공정 검토 없음. 케이스별 협업 프로세스 기준으로 진행."
    local_coder_section = (
        "[로컬 개발 게이트]\n"
        f"- AI 배치 모드: {ai_policy['mode']} ({ai_policy['reason']})\n"
        f"- 모드: {local_coder_gate['mode']}\n"
        f"- 로컬 모델: {local_coder_gate['local_model']}\n"
        f"- Plan 필수: {'예' if local_coder_gate['plan_required'] else '아니오'}\n"
        f"- Qwen 역할: {local_coder_gate['qwen_role']}\n"
        f"- 검증 담당: {local_coder_gate['verification_owner']}\n"
        f"- 최고지배자 실기 검증 필요: {'예' if local_coder_gate['requires_supreme_validation'] else '아니오'}\n"
        f"- API 활용 기준: {local_coder_gate['api_escalation_policy']}\n"
        f"- 지침: {local_coder_gate['instruction']}"
    )

    full_report = (
        f"📝 [LUA BIM LABS 실무 결과 보고서]\n\n"
        f"■ 결재 라인: CEO 승인 완료 ➡️ 총괄 PM 검토 완료\n"
        f"■ 주관 부서: {target_agent} 엔지니어링 파트\n\n"
        f"{workflow_section}\n\n{local_coder_section}\n\n"
        f"----------------------------------------\n{final_solution}\n"
        f"\n\n{boundary_section}\n"
        f"\n\n[AI 팀원 협업 의견]\n{collaboration_section}\n"
        f"\n\n[공정 지식 반영 의견]\n{discipline_section}\n"
        f"----------------------------------------\n"
        f"본 검토서는 대시보드 동기화 릴레이를 거쳐 최종 출도되었습니다."
    )
    if force_local_only:
        full_report += (
            "\n\n[팀원/관리팀 로컬 실행 정책]\n"
            "- DeepSeek API 사용: 금지\n- Qwen Coder/로컬 지식 기반 개발: 허용\n"
            "- Mac 로컬 파일 저장: 금지\n- 최종 결과 전달: Telegram 회신 기준\n"
        )
    full_report = enforce_korean_answer(full_report, fallback_subject=user_text[:80] or "기업 파이프라인 요청")

    st.agent_states["조율차장"]["message"] = full_report
    await st.send_state_to_dashboard()
    telegram_summary = st.build_telegram_summary_report(
        target_agent=target_agent,
        workflow=workflow,
        collaboration_participants=collaboration_participants,
        local_coder_gate=local_coder_gate,
        final_solution=final_solution,
        collaboration_reports=collaboration_reports,
    )
    await st.update_reply_progress(reply_msg, telegram_summary)
    if deliver_full_result:
        await st.send_reply_chunks(reply_msg, full_report)

    st.agent_states["조율차장"]["status"] = "Idle"
    await st.send_state_to_dashboard()
