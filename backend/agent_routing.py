"""
SECTION 6 ── 인텐트 추론 · 에이전트 라우팅 · 협업 워크플로우
  - infer_request_intent, intent_confirmation_message
  - infer_discipline_review_agents, infer_target_agent
  - COLLABORATION_WORKFLOWS, select_collaboration_workflow, score_workflow
  - run_collaboration_stage, compose_local_agent_opinion
  - build_collaboration_plan, build_workflow_summary
  - should_run_discipline_review, preview_collaboration_route
  - is_management_excel_automation_request, 엑셀 승인 요청 관련
  - refresh_obsidian_after_knowledge_update
  - read_agent_knowledge, build_knowledge_context
"""
from __future__ import annotations

import asyncio
import os
import re

import backend.collaboration as collaboration
import backend.local_coder as local_coder
from backend.core.paths import PROJECT_ROOT as _PROJECT_ROOT
from backend.management_excel_approval import (
    create_management_excel_request_item,
    find_management_excel_request,
    load_management_excel_requests,
    management_excel_report_text,
    next_management_excel_request_id,
    save_management_excel_requests,
    summarize_management_excel_request,
)


def _st():
    """server_total 지연 임포트 헬퍼 — 순환 참조 방지."""
    import backend.server_total as _mod
    return _mod


def _pipe():
    """ai_pipeline 지연 임포트 헬퍼 — 순환 참조 방지."""
    import backend.ai_pipeline as _mod
    return _mod


# ---------------------------------------------------------------------------
# Obsidian 갱신
# ---------------------------------------------------------------------------

async def refresh_obsidian_after_knowledge_update() -> None:
    commands = [
        [str(_PROJECT_ROOT / ".dev-venv" / "bin" / "python"), "scripts/mqa_obsidian_tools.py", "graph"],
        [str(_PROJECT_ROOT / ".dev-venv" / "bin" / "python"), "scripts/build_global_obsidian_map.py"],
    ]
    for command in commands:
        try:
            process = await asyncio.create_subprocess_exec(
                *command,
                cwd=str(_PROJECT_ROOT),
                stdout=asyncio.subprocess.DEVNULL,
                stderr=asyncio.subprocess.DEVNULL,
            )
            await process.wait()
        except Exception as exc:
            print(f"⚠️ [Obsidian refresh] {exc}")


# ---------------------------------------------------------------------------
# 지식 파일 읽기 (Section 6 자체 사용)
# ---------------------------------------------------------------------------

def read_agent_knowledge(agent: str, max_chars: int = 2600) -> str:
    st = _st()
    path = st.knowledge_file_path(agent)
    if not os.path.exists(path):
        return st.DEFAULT_KNOWLEDGE.get(agent, "")
    with open(path, "r", encoding="utf-8") as kb_file:
        content = kb_file.read().strip()
    return content[-max_chars:] if len(content) > max_chars else content


def build_knowledge_context(agents: list[str]) -> str:
    chunks = []
    for agent in agents:
        knowledge = read_agent_knowledge(agent)
        if knowledge:
            chunks.append(f"[{agent}]\n{knowledge}")
    return "\n\n".join(chunks)


# ---------------------------------------------------------------------------
# 관리팀 엑셀 자동화 요청 관리
# ---------------------------------------------------------------------------

def is_management_excel_automation_request(text: str) -> bool:
    lower = text.lower()
    excel_hit = any(keyword in lower for keyword in ["엑셀", "excel", "xlsx", "csv", "워크북", "시트", "피벗", "매크로", "openpyxl"])
    management_hit = any(keyword in lower for keyword in ["관리팀", "정산", "근태", "휴가", "비용", "구매", "자산", "라이선스", "월간", "보고서", "집계"])
    automation_hit = any(keyword in lower for keyword in ["자동화", "개발", "만들", "생성", "정리", "취합", "검토", "내보내기"])
    return excel_hit and (management_hit or automation_hit)


def create_management_excel_approval_request(update, request_text: str) -> dict:
    st = _st()
    registry = load_management_excel_requests()
    item = create_management_excel_request_item(
        request_text,
        requester=st.telegram_user_label(update),
        requester_chat_id=str(update.effective_chat.id if update.effective_chat else ""),
        registry=registry,
    )
    registry.setdefault("requests", []).append(item)
    save_management_excel_requests(registry)
    return item


async def notify_management_excel_approval_request(item: dict) -> None:
    st = _st()
    telegram_chat_id = os.environ.get("TELEGRAM_CHAT_ID")
    if not telegram_chat_id or not getattr(st.app.state, "tg_app", None):
        print(f"⚠️ [Excel approval] TELEGRAM_CHAT_ID 또는 tg_app 없음: {item['id']}")
        return
    try:
        await st.app.state.tg_app.bot.send_message(
            chat_id=telegram_chat_id,
            text=management_excel_report_text(item),
            reply_markup=st.TEAM_REQUEST_KEYBOARD,
        )
    except Exception as exc:
        print(f"⚠️ [Excel approval notify] {exc}")


def is_owner_telegram_chat(update) -> bool:
    telegram_chat_id = os.environ.get("TELEGRAM_CHAT_ID")
    if not telegram_chat_id or not update.effective_chat:
        return False
    return str(update.effective_chat.id) == str(telegram_chat_id)


# ---------------------------------------------------------------------------
# 공종 검토 에이전트 추론
# ---------------------------------------------------------------------------

def infer_discipline_review_agents(text: str) -> list[str]:
    st = _st()
    lower_text = text.lower()
    review_agents: list[str] = []
    for group, agents in st.DISCIPLINE_GROUPS.items():
        if f"공정: {group}" in text or f"discipline: {group}" in lower_text:
            review_agents.extend(agents)
    for agent, keywords in st.DISCIPLINE_KEYWORDS.items():
        if any(keyword.lower() in lower_text for keyword in keywords):
            review_agents.append(agent)
    if any(keyword in lower_text for keyword in ["clash", "간섭", "coordination", "조율"]):
        review_agents.extend(["구조", "공조배관", "공조덕트", "소방기계", "전기"])
    deduped = []
    for agent in review_agents:
        if agent in st.ALL_AGENTS and agent not in deduped:
            deduped.append(agent)
    return deduped[:6]


# ---------------------------------------------------------------------------
# 인텐트 추론 키워드 상수
# ---------------------------------------------------------------------------

SUPPORT_INTENT_KEYWORDS = [
    "고객지원", "고객 지원", "고객 문의", "cs", "support", "문의",
    "환불", "라이선스", "라이센스", "결제", "구독", "인증", "사용법", "호환성",
    "안돼요", "안 되", "안됨", "오류", "실패", "하얗게", "안 보여",
]

TECHNICAL_INTENT_KEYWORDS = [
    "revit", "레빗", "navisworks", "나비스웍스", "addin", "add-in", "api",
    "개발", "구현", "코드", "c#", ".net", "디버그", "로그 분석", "exception",
    "요구사항", "기획", "명세", "빌드", "검증", "배포", "패키징", "스토어", "심사",
    "간섭", "clash", "공정", "qwen", "로컬 코더", "로컬 1차", "업무지시",
    "엑셀", "excel", "xlsx", "csv", "openxml", "리포트 자동화",
]

SUPPORT_CONFIRMATION_KEYWORDS = [
    "고객 문의로", "고객지원으로", "cs로", "문의 답변", "일반 문의", "고객 답변",
]

TECHNICAL_CONFIRMATION_KEYWORDS = [
    "개발 검토로", "기술 검토로", "개발 요청", "기술지원으로", "엔지니어링으로",
]

BUSINESS_INTENT_KEYWORDS = [
    "가격", "mrr", "매출", "손익분기", "사업성", "구독 가격", "플랜", "enterprise", "달러",
]

SUPPORT_TONE_KEYWORDS = [
    "안돼요", "안 되", "안됨", "도와줘", "문의", "고객", "답변", "오류", "실패",
]


def intent_keyword_hit(keyword: str, lower_text: str) -> bool:
    if keyword == "cs":
        return bool(re.search(r"(?<![a-z0-9])cs(?![a-z0-9])", lower_text))
    return keyword in lower_text


def is_under_specified_review(text: str, technical_hits: list[str]) -> bool:
    tokens = re.findall(r"[A-Za-z0-9_#+.\-가-힣]{1,}", text.lower())
    if len(tokens) > 4:
        return False
    generic_terms = {"검토", "문제", "위치", "모델", "문", "보", "확인", "봐줘", "해줘"}
    meaningful = [token for token in tokens if token not in generic_terms]
    has_generic_review = any(token in generic_terms for token in tokens)
    if not has_generic_review:
        return False
    strong_hits = {
        hit for hit in technical_hits
        if hit not in {"검토", "확인", "모델", "문제", "위치"}
    }
    return not meaningful or not strong_hits


def infer_request_intent(user_text: str) -> str:
    """사용자 의도를 support / technical / ambiguous 로 분류합니다."""
    st = _st()
    lower_text = user_text.lower()
    education_keywords = [
        "교육", "온보딩", "신규 직원", "신입", "연차별", "커리큘럼", "l&d", "learning",
        "멘토링", "직무교육", "교육자료", "교육 자료", "수습", "역량 매트릭스",
        "노트북lm", "notebooklm", "슬라이드", "ppt", "강의안", "퀴즈", "교육 콘텐츠", "교육콘텐츠", "학습자료", "강의자료",
    ]
    if any(intent_keyword_hit(keyword, lower_text) for keyword in SUPPORT_CONFIRMATION_KEYWORDS):
        return "support"
    if any(intent_keyword_hit(keyword, lower_text) for keyword in TECHNICAL_CONFIRMATION_KEYWORDS):
        return "technical"
    support_hits = [keyword for keyword in SUPPORT_INTENT_KEYWORDS if intent_keyword_hit(keyword, lower_text)]
    technical_hits = [keyword for keyword in TECHNICAL_INTENT_KEYWORDS if intent_keyword_hit(keyword, lower_text)]
    for workflow in st.active_collaboration_workflows():
        if workflow["id"] in {"support_general", "license_billing"}:
            continue
        technical_hits.extend(keyword for keyword in workflow["keywords"] if keyword in lower_text)
    explicit_support = any(intent_keyword_hit(keyword, lower_text) for keyword in ["고객지원", "고객 지원", "고객 문의", "cs"])
    explicit_technical = any(intent_keyword_hit(keyword, lower_text) for keyword in ["개발 요청", "기술 검토", "revit api", "navisworks api"])
    explicit_business = any(intent_keyword_hit(keyword, lower_text) for keyword in BUSINESS_INTENT_KEYWORDS)
    explicit_knowledge = any(intent_keyword_hit(keyword, lower_text) for keyword in ["지식", "knowledge", "kb"]) and any(keyword in lower_text for keyword in ["반영", "업데이트", "추가", "기준"])
    support_tone = any(intent_keyword_hit(keyword, lower_text) for keyword in SUPPORT_TONE_KEYWORDS)
    if any(keyword in lower_text for keyword in education_keywords):
        return "technical"
    if explicit_support:
        return "support"
    if explicit_technical:
        return "technical"
    if explicit_business:
        return "technical"
    if explicit_knowledge:
        return "technical"
    if support_tone and not explicit_technical:
        return "support"
    if support_hits and technical_hits:
        return "ambiguous"
    if support_hits:
        return "support"
    if is_under_specified_review(user_text, technical_hits):
        return "ambiguous"
    return "technical"


def intent_confirmation_message(user_text: str) -> str:
    return (
        "의도 확인이 필요합니다.\n\n"
        "이 질문을 어떤 방식으로 처리할까요?\n"
        "1. 고객 문의 답변: 환불, 라이선스, 결제, 사용법, FAQ 중심으로 답변\n"
        "2. 개발/기술 검토: Revit/Navisworks Add-in 개발, 로그, 코드, 배포 검토\n\n"
        "다시 보낼 때 앞에 의도를 붙여주세요.\n"
        "예: `고객 문의로 답변해줘: " + user_text + "`\n"
        "예: `개발 검토로 답변해줘: " + user_text + "`"
    )


# ---------------------------------------------------------------------------
# 협업 워크플로우 정의
# ---------------------------------------------------------------------------

COLLABORATION_WORKFLOWS = [
    {"id": "support_general", "name": "일반 고객 문의 대응", "primary": "고객지원 CS",
     "participants": ["고객지원 CS", "라이선스결제", "배포문서"],
     "keywords": ["고객지원", "고객 문의", "cs", "support", "문의", "사용법", "호환성", "환불"],
     "steps": ["문의 유형 분류 및 FAQ 매칭", "라이선스/결제/설치 항목만 필요한 경우 담당 지식 연결", "고객에게 보낼 1차 답변과 추가 확인 정보 정리"],
     "local_only": True},
    {"id": "license_billing", "name": "라이선스/결제/구독 검토", "primary": "라이선스결제",
     "participants": ["라이선스결제", "고객지원 CS", "CFO", "라이선스_보안관"],
     "keywords": ["라이선스", "라이센스", "결제", "구독", "entitlement", "paypal", "bluesnap", "가격", "환불"],
     "steps": ["구독/체험/만료/오프라인 캐시 상태 분류", "고객 응답 문구와 결제 정책 리스크 확인", "수익/수수료/세금 또는 보안 영향이 있으면 CFO/보안관 검토"],
     "local_only": True},
    {"id": "store_release", "name": "Autodesk Store 출시/심사 준비", "primary": "스토어심사",
     "participants": ["스토어심사", "제품패키징", "라이선스결제", "배포문서", "고객지원 CS", "라이선스_보안관"],
     "keywords": ["autodesk store", "app store", "스토어", "심사", "출시", "판매", "submit", "submission", "publisher"],
     "steps": ["심사 리스크와 제품 설명/스크린샷/지원 연락처 확인", "패키징, 라이선스, 개인정보, 지원 문서 준비 상태 점검", "제출 전 차단 이슈와 보완 작업을 릴리스 게이트로 정리"],
     "local_only": False},
    {"id": "packaging_install", "name": "설치/배포 패키징 검토", "primary": "제품패키징",
     "participants": ["제품패키징", "배포문서", "빌드검증", "고객지원 CS"],
     "keywords": ["설치", "배포", "installer", "msi", "addin manifest", ".addin", "패키징", "설치파일", "bundle"],
     "steps": ["설치/제거/업데이트 경로와 Revit Add-in manifest 확인", "빌드 검증과 smoke test 항목 연결", "고객용 설치 가이드와 실패 시 CS 응답 흐름 정리"],
     "local_only": True},
    {"id": "build_qa", "name": "빌드/QA/회귀 검증", "primary": "빌드검증",
     "participants": ["빌드검증", "QA_테스터", "프로그램개발", "배포문서"],
     "keywords": ["테스트", "qa", "검증", "빌드", "smoke", "회귀", "버그", "crash", "크래시"],
     "steps": ["지원 Revit/Navisworks 버전별 smoke test 범위 설정", "P1/P2 차단 이슈와 회귀 테스트 우선순위 분리", "릴리스 노트와 알려진 이슈 문서화"],
     "local_only": True},
    {"id": "requirements_scope", "name": "요구사항/범위 정의", "primary": "요구사항분석",
     "participants": ["요구사항분석", "프로젝트분석", "전략기획", "프로그램개발", "견적심사원"],
     "keywords": ["요구사항", "기획", "명세", "spec", "범위", "mvp", "기능 정의", "우선순위"],
     "steps": ["사용자 문제와 성공 기준을 user story로 정리", "MVP/제외 범위/향후 Pro 기능 분리", "공수, 일정 버퍼, 개발 리스크를 견적 기준으로 연결"],
     "local_only": True},
    {"id": "revit_development", "name": "Revit Add-in 개발", "primary": "Revit_Addin",
     "participants": ["Revit_Addin", "프로그램개발", "QA_테스터", "빌드검증", "배포문서"],
     "keywords": ["revit", "레빗", "revit api", "iexternalcommand", "패밀리", "뷰 템플릿", "스케줄"],
     "steps": ["Revit API 가능성과 트랜잭션 경계 확인", "명령 구조, 설정 저장, 예외 처리, 로그 기준 설계", "빌드/배포/QA 검증 항목으로 넘김"],
     "local_only": False},
    {"id": "navisworks_development", "name": "Navisworks Add-in 개발", "primary": "Navisworks_Addin",
     "participants": ["Navisworks_Addin", "프로그램개발", "엑셀자동화", "QA_테스터", "배포문서"],
     "keywords": ["navisworks", "navis", "나비스웍스", "나비스", "clash", "간섭", "clash detective"],
     "steps": ["Navisworks API/ClashResult 접근 범위 확인", "간섭 결과 필드와 Excel/CSV 내보내기 구조 설계", "대형 모델 성능과 보고서 검증 흐름 구성"],
     "local_only": False},
    {"id": "coordination_discipline", "name": "BIM 공정 조율/간섭 검토", "primary": "조율차장",
     "participants": ["조율차장", "건축", "구조", "공조배관", "공조덕트", "소방기계", "전기", "엑셀자동화"],
     "keywords": ["간섭", "clash", "coordination", "조율", "mep통합", "전체공정"],
     "steps": ["공정별 영향 범위와 우선순위 분류", "건축/구조/MEP 검토 의견 병합", "보고서 필드와 담당자/상태/우선순위 출력 구조 확정"],
     "local_only": True},
    {"id": "privacy_security", "name": "개인정보/보안/외부통신 검토", "primary": "라이선스_보안관",
     "participants": ["라이선스_보안관", "법무조항검토", "고객지원 CS", "배포문서", "스토어심사"],
     "keywords": ["개인정보", "privacy", "보안", "토큰", "api key", "외부 통신", "로그", "데이터 전송", "모델 데이터"],
     "steps": ["수집/저장/외부 전송 데이터 항목 식별", "로그와 정책 문서의 민감정보 노출 여부 검토", "스토어 설명, 개인정보 처리방침, 고객 고지 문구 반영"],
     "local_only": True},
    {"id": "pricing_revenue", "name": "가격/수익/사업성 검토", "primary": "CFO",
     "participants": ["CFO", "CEO", "글로벌_매출관리원", "전략기획", "브랜드마케팅"],
     "keywords": ["가격", "수익", "mrr", "매출", "손익분기", "구독 가격", "사업성", "플랜", "enterprise"],
     "steps": ["가격/플랜/수수료/세금 영향 정리", "MRR, 유료 전환, 지원 비용 기준으로 사업성 검토", "Store 포지셔닝과 마케팅 메시지로 연결"],
     "local_only": False},
    {"id": "docs_release", "name": "문서/릴리스 노트/고객 가이드", "primary": "배포문서",
     "participants": ["배포문서", "테크니컬_라이터", "브랜드마케팅", "고객지원 CS"],
     "keywords": ["문서", "가이드", "릴리스 노트", "사용자 가이드", "설명", "도움말", "changelog"],
     "steps": ["설치/첫 실행/제거/제한사항 문서 항목 정리", "스토어 설명과 실제 기능 일치 여부 확인", "CS FAQ와 릴리스 노트를 함께 업데이트"],
     "local_only": True},
    {"id": "knowledge_update", "name": "지식 베이스 업데이트", "primary": "지식업데이트",
     "participants": ["지식업데이트", "지식큐레이터", "프롬프트엔지니어", "조율차장"],
     "keywords": ["지식 업데이트", "knowledge", "kb", "학습", "문서 반영", "기준 추가", "큐레이션", "분류", "승격", "보류"],
     "steps": ["출처/태그/시간 기준으로 지식 항목 정리", "지식큐레이터가 목적성, 승격 후보, 보안검토 여부를 분류", "기존 지식과 충돌 여부 확인", "다음 라우팅에 반영될 키워드와 담당 에이전트 점검"],
     "local_only": True},
]


def score_workflow(workflow: dict, lower_text: str) -> int:
    return sum(1 for keyword in workflow["keywords"] if keyword in lower_text)


def select_collaboration_workflow(user_text: str, target_agent: str, request_intent: str) -> dict:
    lower_text = user_text.lower()
    if request_intent == "support":
        if any(keyword in lower_text for keyword in ["가격", "mrr", "매출", "손익분기", "사업성", "구독 가격"]):
            workflow_id = "pricing_revenue"
        elif any(keyword in lower_text for keyword in ["라이선스", "라이센스", "결제", "구독", "entitlement", "환불"]):
            workflow_id = "license_billing"
        else:
            workflow_id = "support_general"
        return next(w for w in COLLABORATION_WORKFLOWS if w["id"] == workflow_id)
    scored = sorted(
        ((score_workflow(workflow, lower_text), workflow) for workflow in COLLABORATION_WORKFLOWS),
        key=lambda item: item[0],
        reverse=True,
    )
    if scored and scored[0][0] > 0:
        return scored[0][1]
    for workflow in COLLABORATION_WORKFLOWS:
        if workflow["primary"] == target_agent:
            return workflow
    return next(w for w in COLLABORATION_WORKFLOWS if w["id"] == "requirements_scope")


def has_explicit_support_channel(user_text: str) -> bool:
    lower_text = user_text.lower()
    return any(keyword in lower_text for keyword in ["고객지원", "고객 지원", "고객 문의", "cs", "문의 답변", "일반 문의"])


def determine_primary_agent(user_text: str, target_agent: str, workflow: dict, request_intent: str) -> str:
    if request_intent == "support" and has_explicit_support_channel(user_text):
        return "고객지원 CS"
    return workflow["primary"] or target_agent


def build_collaboration_plan(workflow: dict, target_agent: str, review_agents: list[str]) -> list[str]:
    st = _st()
    participants = ["CEO", "조율차장"]
    participants.extend(workflow["participants"])
    if target_agent not in participants:
        participants.append(target_agent)
    participants.extend(review_agents)
    deduped = []
    for agent in participants:
        if agent and agent not in deduped:
            deduped.append(agent)
            st.ensure_agent_state(agent)
    return deduped


async def run_collaboration_stage(agent: str, workflow: dict, user_text: str, allow_web_search: bool) -> str:
    st = _st()
    st.ensure_agent_state(agent)
    st.current_active_agent = agent
    st.agent_states[agent]["status"] = "Active"
    st.agent_states[agent]["message"] = f"{workflow['name']} 협업 프로세스 참여 중."
    await st.send_state_to_dashboard()
    knowledge = read_agent_knowledge(agent, max_chars=2200)
    if agent == "Qwen_Coder_8B":
        qwen_prompt = (
            f"요청:\n{user_text}\n\n"
            f"협업 프로세스: {workflow['name']}\n"
            f"진행 단계:\n" + "\n".join(f"- {step}" for step in workflow.get("steps", [])) + "\n\n"
            "구현 언어 규칙: 엑셀 자동화는 반드시 Python/openpyxl을 우선 제안하세요. "
            "C# OpenXML은 .NET Add-in 연계가 명시된 경우에만 제안하세요. "
            "Lua 언어는 절대 제안하지 마세요.\n"
            "다음 형식으로 짧고 실행 가능하게 작성하세요.\n"
            "1. Plan: 목적, 입력, 출력, 제외 범위\n"
            "2. Draft: 구현 초안 또는 Add-in 가이드라인\n"
            "3. Verification: 로컬 검증 방법\n"
            "4. API 필요성 판단: 외부 API/Revit API/Navisworks API 호출이 필요한지, 필요 없다면 'API 필요 없음'이라고 명시\n"
        )
        qwen_result = await local_coder.generate(
            qwen_prompt,
            system=(
                "당신은 LUA BIM LABS 조직의 로컬 Qwen 코더입니다. "
                "엑셀 자동화는 주 업무로 구현 초안을 작성하고, "
                "Revit/Navisworks Add-in은 가이드라인과 정적 검토까지만 작성합니다. "
                "엑셀 자동화 기본 구현 언어는 Python/openpyxl이며 .NET Add-in 연계가 필요할 때만 C# OpenXML을 제안합니다. "
                "Lua 언어는 사용자가 명시적으로 요청한 경우에만 제안합니다. "
                "항상 plan을 먼저 제시하고, API 필요 여부를 보수적으로 판단합니다."
            ),
            num_predict=420,
            timeout=50,
        )
        if qwen_result.get("ok"):
            response = f"[{agent}] 로컬 Qwen 실행 결과 ({qwen_result.get('model')})\n{qwen_result['response']}"
        else:
            response = (
                f"[{agent}] 로컬 Qwen 실행 불가\n"
                f"- 사유: {qwen_result.get('reason')}\n"
                f"- 대체: {compose_local_agent_opinion(agent, workflow, user_text, knowledge)}"
            )
    else:
        response = compose_local_agent_opinion(agent, workflow, user_text, knowledge)
    st.agent_states[agent]["message"] = response
    st.agent_states[agent]["tokens"] += max(1, len(response.split()) // 12)
    await st.send_state_to_dashboard()
    await asyncio.sleep(0.08)
    st.agent_states[agent]["status"] = "Idle"
    await st.send_state_to_dashboard()
    return response


def compose_local_agent_opinion(agent: str, workflow: dict, user_text: str, knowledge: str) -> str:
    from backend.ai_pipeline import _parse_sections, _score_and_pick
    picked = _score_and_pick(_parse_sections(knowledge), user_text) if knowledge else []
    basis = picked[0][1] if picked else "저장 지식/기본 역할 기준"
    responsibility = {
        "CEO": "제품 방향·브랜드·우선순위를 결정하고 C-suite 심의를 주재한다.",
        "COO": "운영 KPI·릴리스 게이트·팀 자원 배분을 결정하고 실행 가능성을 판단한다.",
        "CFO": "비용·수익성·손익분기를 검토하고 예산 수반 여부를 명시한다.",
        "조율차장": "담당 팀 간 순서와 병목을 조율한다.",
        "고객지원 CS": "고객에게 보낼 1차 답변, 추가 확인 정보, 에스컬레이션 기준을 정리한다.",
        "라이선스결제": "구독/체험/만료/결제 상태와 Entitlement 흐름을 확인한다.",
        "스토어심사": "Autodesk Store 제출물과 심사 리스크를 확인한다.",
        "제품패키징": "설치/제거/업데이트와 배포 패키지 안정성을 본다.",
        "배포문서": "설치 가이드, 릴리스 노트, 지원 문서 일관성을 맞춘다.",
        "빌드검증": "지원 버전별 smoke test와 빌드 산출물 검증을 맡는다.",
        "QA_테스터": "재현 절차, 회귀 테스트, 차단 버그를 분리한다.",
        "요구사항분석": "사용자 문제, 범위, 성공 기준을 명확히 한다.",
        "프로그램개발": "구현 구조, 예외 처리, 코드 영향 범위를 검토한다.",
        "Qwen_Coder_8B": "API 토큰 없이 로컬에서 일반 개발 초안과 테스트 코드 초안을 만든다.",
        "경비정산_AI": "Telegram 영수증/증빙을 로컬에서 수집, 분류하고 정산표 초안을 만든다.",
        "HR_인재분석관": "이력서 PDF와 구조화 데이터를 로컬에서 분석해 채용 대시보드와 인재 평가 보고서 초안을 만든다.",
        "경영지원": "회계/세무 제출에 필요한 행정 자료와 확정 보관 기준을 확인한다.",
        "엑셀자동화": "Excel/CSV 보고서 구조, 필드, 필터, 대용량 출력 안정성을 설계한다.",
        "Revit_Addin": "Revit API, 명령 구조, 트랜잭션 리스크를 검토한다.",
        "Navisworks_Addin": "Navisworks API, Clash 데이터, 보고서 추출 구조를 검토한다.",
        "라이선스_보안관": "토큰, 개인정보, 로그, 외부 전송 리스크를 점검한다.",
        "법무조항검토": "정책, EULA, 고지 문구 리스크를 검토한다.",
        "테크니컬_라이터": "고객 언어로 문서를 짧고 정확하게 정리한다.",
        "브랜드마케팅": "스토어 설명과 고객 가치 표현을 정리한다.",
        "전략기획": "MVP, Pro, 향후 로드맵으로 나눈다.",
        "프로젝트분석": "대상 프로젝트와 반복 업무의 현실성을 본다.",
        "견적심사원": "공수, 일정 버퍼, 제외 범위를 검토한다.",
        "지식업데이트": "반복 문의와 결정 기준을 지식 베이스에 반영한다.",
    }.get(agent, f"{agent} 관점의 도메인 기준을 검토한다.")
    boundary = collaboration.role_boundary(agent)
    owns = ", ".join(boundary["owns"][:3])
    handoff = ", ".join(f"{key}->{value}" for key, value in list(boundary["handoff"].items())[:2])
    next_action = {
        "CEO": "제품 방향과 우선순위 결정을 한 줄로 명시하고, 예산/인력 수반 여부를 COO·CFO에게 넘길 항목으로 표시한다.",
        "COO": "릴리스 게이트 통과 여부, 팀 자원 배분 조정 필요 여부, 병목 지점을 조율차장에게 넘길 항목으로 명시한다.",
        "고객지원 CS": "고객에게는 필요한 환경 정보만 먼저 요청하고 실제 프로젝트 모델은 마지막 수단으로 둔다.",
        "라이선스결제": "구독 상태, Autodesk ID, 구매/갱신 링크, 오프라인 캐시 상태를 분리한다.",
        "스토어심사": "제품 설명, 개인정보, 지원 연락처, 심사 차단 요소를 제출 전 체크리스트로 만든다.",
        "제품패키징": "설치 실패 재현 정보와 제거/재설치 절차를 문서에 연결한다.",
        "빌드검증": "P1/P2 이슈가 있으면 출시를 막고 smoke test 결과를 남긴다.",
        "요구사항분석": "As a/I want/So that 형식으로 요구사항을 다시 정리한다.",
        "Qwen_Coder_8B": "Autodesk API 의존 코드는 확정하지 않고 프로그램개발 검토용 초안으로만 남긴다.",
        "경비정산_AI": "영수증 원본의 민감정보를 외부로 보내지 않고 누락/중복/불명확 항목을 먼저 표시한다.",
        "HR_인재분석관": "후보자 개인정보와 이전 회사/고객명은 외부 API로 보내지 않고 AI 등급은 최종 채용 판단으로 확정하지 않는다.",
        "경영지원": "최종 정산 자료는 회계/세무 전달용 증빙 목록으로 보관한다.",
        "엑셀자동화": "샘플 데이터, 열 정의, 파일 손상 방지, 인코딩, 필터 가능성을 먼저 검증한다.",
        "Revit_Addin": "모델 변경 명령은 Transaction 범위와 dry-run 여부를 먼저 정한다.",
        "Navisworks_Addin": "ClashResult 필드와 Excel 내보내기 필드를 먼저 확정한다.",
        "라이선스_보안관": "비밀값과 고객 모델 데이터가 로그/보고서에 남지 않게 제한한다.",
        "CFO": "지원 비용과 환불률까지 포함해 가격 판단을 보조하고, 예산 초과 시 CEO에게 에스컬레이션한다.",
        "지식큐레이터": "출처 신뢰도, 최신성, 승격 후보 여부를 판단해 표준/교육/FAQ 지식 라인으로 분류한다.",
    }.get(agent, "다음 단계로 넘길 확인 항목과 차단 리스크를 짧게 정리한다.")
    return (
        f"[{agent}] {workflow['name']} 협업 의견\n"
        f"- 역할: {responsibility}\n"
        f"- 경계: {owns}\n"
        f"- 경계 초과 시: {handoff}\n"
        f"- 근거: {basis}\n"
        f"- 조치: {next_action}"
    )


def build_workflow_summary(workflow: dict, participants: list[str], use_paid_ai: bool) -> str:
    steps = "\n".join(f"{idx + 1}. {step}" for idx, step in enumerate(workflow["steps"]))
    api_mode = "유료 API 사용 가능" if use_paid_ai and not workflow.get("local_only") else "로컬 지식 기반"
    return (
        f"[협업 프로세스]\n"
        f"- 케이스: {workflow['name']}\n"
        f"- 처리 모드: {api_mode}\n"
        f"- 참여 팀원: {' → '.join(participants)}\n"
        f"- 진행 순서:\n{steps}"
    )


def should_run_discipline_review(workflow: dict, target_agent: str) -> bool:
    st = _st()
    discipline_workflows = {"revit_development", "navisworks_development", "coordination_discipline"}
    discipline_agents = set(st.DISCIPLINE_KEYWORDS.keys())
    return workflow["id"] in discipline_workflows or target_agent in discipline_agents


def preview_collaboration_route(user_text: str) -> dict:
    pipe = _pipe()
    request_intent = infer_request_intent(user_text)
    if request_intent == "ambiguous":
        return {
            "intent": request_intent,
            "requires_confirmation": True,
            "confirmation_message": intent_confirmation_message(user_text),
        }
    target_agent = pipe.infer_target_agent(user_text)
    st = _st()
    workflows = st.active_collaboration_workflows()
    workflow = collaboration.select_collaboration_workflow(user_text, target_agent, request_intent, workflows)
    target_agent = collaboration.determine_primary_agent(user_text, target_agent, workflow, request_intent)
    use_paid_ai = pipe.should_use_paid_ai(target_agent, user_text, workflow)
    if workflow.get("local_only"):
        use_paid_ai = False
    ai_policy = pipe.ai_execution_policy_summary(target_agent, user_text, workflow)
    review_agents = infer_discipline_review_agents(user_text) if collaboration.should_run_discipline_review(workflow, target_agent, set(st.DISCIPLINE_KEYWORDS.keys())) else []
    participants = build_collaboration_plan(workflow, target_agent, review_agents)
    local_coder_gate = collaboration.local_coder_gate(user_text, workflow)
    return {
        "intent": request_intent,
        "requires_confirmation": False,
        "workflow_id": workflow["id"],
        "workflow_name": workflow["name"],
        "target_agent": target_agent,
        "participants": participants,
        "review_agents": review_agents,
        "use_paid_ai": use_paid_ai,
        "ai_execution_mode": ai_policy["mode"],
        "ai_policy_reason": ai_policy["reason"],
        "local_coder": local_coder_gate,
        "requires_supreme_validation": local_coder_gate["requires_supreme_validation"],
        "steps": workflow["steps"],
        "role_boundaries": {agent: collaboration.role_boundary(agent) for agent in participants},
    }
