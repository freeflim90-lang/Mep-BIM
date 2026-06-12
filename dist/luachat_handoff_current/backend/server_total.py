from __future__ import annotations

import os
import re
import json
import asyncio
import copy
import datetime
from pathlib import Path
from typing import Optional
import httpx
from fastapi import FastAPI, Header, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from telegram import ReplyKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from openai import AsyncOpenAI
import backend.collaboration as collaboration
import backend.github_integration as github_integration
import backend.local_coder as local_coder
import backend.qwen_product_drafts as qwen_product_drafts
from backend.core.paths import DATA_DIR, FRONTEND_DIR, GLOBAL_OBSIDIAN_VAULT, PROJECT_ROOT
from backend.bim_command_center.feature_registry import list_phase1_features, validate_feature_registry
from backend.bim_command_center.settings_profiles import (
    ProfileScope,
    SettingsProfile,
    SettingsProfileError,
    default_profile_store,
)
from backend.models import (
    AddinTaskRequest, KnowledgeUpdateRequest, RoutePreviewRequest,
    GitHubRepoListRequest, LocalCoderDraftRequest, QwenProductDraftRunRequest,
    SettingsProfileSaveRequest, RevitAssistantChatRequest, RevitAssistantFeedbackRequest,
)
from backend.knowledge_store import (
    ALL_AGENTS,
    DEFAULT_KNOWLEDGE,
    DISCIPLINE_GROUPS,
    DISCIPLINE_KEYWORDS,
    EXTRA_KNOWLEDGE_AGENTS,
    KNOWLEDGE_AGENTS,
    KNOWLEDGE_DIR,
    ORGANIZATION,
    QA_KNOWLEDGE_DIR,
    append_knowledge_update,
    ensure_knowledge_base,
    knowledge_file_path,
    qa_knowledge_file_path,
)
from backend.text_utils import (
    sanitize_outbound_text, sanitize_resume_text_for_ai,
    normalize_query_text, normalize_team_button_text,
    launch_background_task, log_background_task_result,
    build_telegram_summary_report, build_telegram_progress_report,
    update_reply_progress, send_reply_chunks,
    telegram_session_key, telegram_user_label, is_resume_document,
    extract_pdf_text_local, build_local_resume_report,
)
from backend.obsidian_notes import (
    append_team_request_log, slugify_obsidian_title, infer_qa_domain,
    ensure_team_qa_moc, rebuild_team_qa_moc, save_team_qa_to_obsidian,
    ensure_revit_qa_moc, rebuild_revit_qa_moc,
    build_revit_context_prompt, build_revit_assistant_answer,
    save_revit_qa_to_obsidian, append_team_qa_feedback,
)
from backend.routers.bim_land import router as bim_land_router

DEEPSEEK_BUDGET_FILE = DATA_DIR / "ai_usage" / "deepseek_monthly_budget.json"
DEEPSEEK_MONTHLY_BUDGET_USD = float(os.environ.get("DEEPSEEK_MONTHLY_BUDGET_USD", "50"))
DEEPSEEK_ESTIMATED_CALL_COST_USD = float(os.environ.get("DEEPSEEK_ESTIMATED_CALL_COST_USD", "0.35"))

def load_local_env(path=None):
    """Load simple KEY=VALUE pairs for local development without adding a dependency."""
    path = Path(path) if path else PROJECT_ROOT / ".env"
    if not os.path.exists(path):
        return
    with open(path, "r", encoding="utf-8") as env_file:
        for raw_line in env_file:
            line = raw_line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, value = line.split("=", 1)
            os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))

load_local_env()

# =============================================================================
# SECTION 1 ── 시스템 초기화 · FastAPI · 조직 설정
#   - FastAPI 앱 / CORS / 에이전트 상태 / 조직 구조 / AI 클라이언트
# =============================================================================
app = FastAPI()
cors_origins = [origin.strip() for origin in os.environ.get("CORS_ORIGINS", "*").split(",")]

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials="*" not in cors_origins,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.mount("/static", StaticFiles(directory=FRONTEND_DIR / "static"), name="static")

# DeepSeek 코어 클라이언트 지정 (내부 인프라용)
DEEPSEEK_API_KEY = os.environ.get("DEEPSEEK_API_KEY", "sk-fake-key-for-test")
PAID_AI_ENABLED = os.environ.get("PAID_AI_ENABLED", "false").lower() in {"1", "true", "yes", "on"}
deepseek_client = AsyncOpenAI(api_key=DEEPSEEK_API_KEY, base_url="https://api.deepseek.com")
TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "fake-bot-token")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")

# 글로벌 상태 저장소 초기화 (토큰 및 메시지 맵)
agent_states = {
    agent: {"status": "Idle", "tokens": 0, "message": ""}
    for agent in ALL_AGENTS
}

current_active_agent = "CEO"  # 라우팅 시작점은 항상 CEO

# =============================================================================
# SECTION 2 ── Pydantic 모델 (→ backend/models.py)
# =============================================================================
# 모델 클래스는 backend/models.py 에서 일괄 임포트 (파일 상단 참조).

class DashboardReply:
    async def edit_text(self, text: str):
        agent_states["조율차장"]["message"] = text
        await send_state_to_dashboard()

# =============================================================================
# SECTION 3 ── 유틸리티 · 텍스트 처리 · 에이전트 상태 관리
#   순수 함수: backend/text_utils.py 에서 임포트 (파일 상단 참조)
#   서버 전역 상태에 의존하는 함수만 이 파일에 유지
# =============================================================================

def ensure_agent_state(agent: str) -> None:
    if agent not in agent_states:
        agent_states[agent] = {"status": "Idle", "tokens": 0, "message": ""}

def reset_agent_status(agent: str) -> None:
    ensure_agent_state(agent)
    agent_states[agent]["status"] = "Idle"

for _agent in KNOWLEDGE_AGENTS:
    ensure_agent_state(_agent)

def active_collaboration_workflows() -> list[dict]:
    return collaboration.load_collaboration_workflows(KNOWLEDGE_DIR)

TEAM_REQUEST_LOG = DATA_DIR / "team_requests" / "telegram_knowledge_requests.md"
TEAM_TELEGRAM_USERS_FILE = DATA_DIR / "team_requests" / "team_telegram_users.json"
MANAGEMENT_EXCEL_AUTOMATION_REQUESTS = DATA_DIR / "automation_requests" / "management_excel_automation_requests.json"
AUTO_KNOWLEDGE_GAP_LOG = DATA_DIR / "knowledge_quality" / "auto_knowledge_gap_log.md"
TEAM_QA_OBSIDIAN_DIR = GLOBAL_OBSIDIAN_VAULT / "NAS_Knowledge" / "Team_Telegram_QA"
TEAM_QA_MOC = TEAM_QA_OBSIDIAN_DIR / "MOC - Team Telegram QA.md"
REVIT_QA_OBSIDIAN_DIR = GLOBAL_OBSIDIAN_VAULT / "NAS_Knowledge" / "Revit_Assistant_QA"
REVIT_QA_MOC = REVIT_QA_OBSIDIAN_DIR / "MOC - Revit Assistant QA.md"
RESUME_INTAKE_DIR = DATA_DIR / "resume_intake" / "telegram"
TELEGRAM_KNOWLEDGE_SESSIONS: dict[str, dict] = {}


def require_revit_assistant_api_key(api_key: Optional[str]) -> None:
    configured = {
        item.strip()
        for item in os.environ.get("REVIT_ASSISTANT_API_KEYS", "").split(",")
        if item.strip()
    }
    if not configured:
        return
    if not api_key or api_key.strip() not in configured:
        raise HTTPException(status_code=401, detail="invalid revit assistant api key")

TEAM_REQUEST_KEYBOARD = ReplyKeyboardMarkup(
    [["📚 지식질문", "🔎 더 찾아줘", "🧩 개발"]],
    resize_keyboard=True,
    one_time_keyboard=False,
    input_field_placeholder="질문을 그냥 입력하거나 버튼을 눌러주세요.",
)

def telegram_chat_allowed(update: Update) -> bool:
    allowed_raw = os.environ.get("TELEGRAM_TEAM_CHAT_IDS") or TELEGRAM_CHAT_ID or ""
    allowed = {item.strip() for item in allowed_raw.split(",") if item.strip()}
    if TEAM_TELEGRAM_USERS_FILE.exists():
        try:
            registry = json.loads(TEAM_TELEGRAM_USERS_FILE.read_text(encoding="utf-8"))
            for user in registry.get("users", []):
                chat_id = str(user.get("telegram_chat_id", "")).strip()
                if chat_id and user.get("status") != "disabled":
                    allowed.add(chat_id)
        except (OSError, json.JSONDecodeError) as exc:
            print(f"⚠️ [Telegram team registry] {exc}")
    if not allowed:
        return True
    chat_id = str(update.effective_chat.id) if update.effective_chat else ""
    return chat_id in allowed

async def deepseek_resume_report(masked_text: str, file_name: str) -> str | None:
    if os.environ.get("RESUME_DEEPSEEK_FALLBACK_ENABLED", "false").lower() not in {"1", "true", "yes", "on"}:
        return None
    if not PAID_AI_ENABLED or not DEEPSEEK_API_KEY or DEEPSEEK_API_KEY == "sk-fake-key-for-test":
        return None
    if not can_use_deepseek_budget():
        return None
    response = await deepseek_client.chat.completions.create(
        model=os.environ.get("DEEPSEEK_MODEL", "deepseek-chat"),
        messages=[
            {
                "role": "system",
                "content": (
                    "당신은 LUA BIM LABS의 HR_인재분석관입니다. "
                    "마스킹된 이력서 텍스트만 바탕으로 채용 검토 초안을 작성하고, "
                    "개인정보 추정이나 차별적 판단을 하지 마세요."
                ),
            },
            {
                "role": "user",
                "content": (
                    f"파일명: {sanitize_outbound_text(file_name)}\n\n"
                    "다음 마스킹된 이력서 텍스트를 바탕으로 1페이지 인재 평가 보고서 초안을 작성하세요. "
                    "S/A/B 등급은 근거와 함께 초안으로만 표시하고, 최종 판단은 사람이 한다고 명시하세요.\n\n"
                    f"{masked_text[:10000]}"
                ),
            },
        ],
        max_tokens=1800,
    )
    record_deepseek_budget_use(workflow_id="resume_analysis_dashboard", target_agent="HR_인재분석관")
    content = response.choices[0].message.content or ""
    return sanitize_outbound_text(content.strip())[:3800] if content.strip() else None

# normalize_query_text, normalize_team_button_text → backend/text_utils.py 임포트

# =============================================================================
# SECTION 4 ── 지식 베이스 검색 · 점수화 · 답변 생성 (→ backend/knowledge_engine.py)
# =============================================================================
from backend.knowledge_engine import (
    knowledge_search_files, query_terms, score_knowledge_text,
    extract_relevant_excerpt, search_local_knowledge,
    infer_knowledge_agent_from_query, build_knowledge_answer, build_combined_answer,
    assess_knowledge_answer_quality, auto_supplement_knowledge_gap,
    append_auto_knowledge_gap_log, build_more_research_answer,
    prioritize_agent_matches, count_gap_occurrences, get_persistent_gaps,
    _EXCLUDED_KNOWLEDGE_STEMS,
)

# =============================================================================
# SECTION 5 ── Obsidian 노트 · QA 아카이브 · 팀 요청 로그 (→ backend/obsidian_notes.py)
# =============================================================================
# 모든 Obsidian 함수는 backend/obsidian_notes.py 에서 임포트 (파일 상단 참조).

# =============================================================================
# SECTION 6 ── 인텐트 추론 · 에이전트 라우팅 · 협업 워크플로우 (→ backend/agent_routing.py)
# =============================================================================
from backend.agent_routing import (
    is_management_excel_automation_request,
    load_management_excel_requests, save_management_excel_requests,
    infer_discipline_review_agents, infer_request_intent,
    intent_confirmation_message, select_collaboration_workflow,
    build_collaboration_plan, run_collaboration_stage,
    compose_local_agent_opinion, preview_collaboration_route,
    refresh_obsidian_after_knowledge_update,
    read_agent_knowledge, build_knowledge_context,
    COLLABORATION_WORKFLOWS,
)

# =============================================================================
# SECTION 7 ── WebSocket · 대시보드 상태 브로드캐스트 · 웹 검색 파이프라인
#   [WebSocket]
#   - ConnectionManager (broadcast, connect, disconnect)
#   - send_state_to_dashboard, log_to_dashboard
#   [에이전트 응답 생성]
#   - _extract_agent_name, _parse_sections, _compose_knowledge_response
#   [웹 검색 API]
#   - _build_search_query
#   - _search_tavily (include_answer=True, AI 요약 포함)
#   - _search_naver (웹문서 + 뉴스, 한국어 최적)
#   - _search_google_cse (403 시 graceful fallback)
#   - _search_duckduckgo
#   - _search_web_for_knowledge (병렬 검색 → 병합)
# =============================================================================
class ConnectionManager:
    def __init__(self):
        self.active_connections: set[WebSocket] = set()

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.add(websocket)
        print(f"📡 [웹소켓] 대시보드 클라이언트 연결 성공. (총 연결수: {len(self.active_connections)})")

    def disconnect(self, websocket: WebSocket):
        self.active_connections.discard(websocket)
        print(f"⚠️ [웹소켓] 대시보드 세션 종료. (남은 연결수: {len(self.active_connections)})")

    async def broadcast(self, message: str):
        stale_connections = []
        for connection in list(self.active_connections):
            try:
                await connection.send_text(message)
            except Exception:
                stale_connections.append(connection)
        for connection in stale_connections:
            self.disconnect(connection)

manager = ConnectionManager()
# 에이전트 응답 생성 함수 및 웹 검색 파이프라인 → backend/web_search.py & backend/ai_pipeline.py
from backend.web_search import (
    _AGENT_SEARCH_CONTEXT, _KNOWLEDGE_MIN_CHARS,
    _build_search_query, _search_tavily, _search_duckduckgo,
    _search_google_cse, _search_naver,
    _search_web_for_knowledge, _save_search_result_to_knowledge,
)

# =============================================================================
# SECTION 8 ── AI 스트리밍 · DeepSeek 예산 · 기업 파이프라인 (→ backend/ai_pipeline.py)
# =============================================================================
from backend.ai_pipeline import (
    _extract_agent_name, _parse_sections, _score_and_pick, _compose_knowledge_response,
    current_budget_month, load_deepseek_budget_registry, save_deepseek_budget_registry,
    can_use_deepseek_budget, record_deepseek_budget_use,
    stream_claude, infer_target_agent,
    should_use_paid_ai, ai_execution_policy_summary,
    process_corporate_pipeline,
    LOCAL_ONLY_WORKFLOW_IDS, DEEPSEEK_CANDIDATE_WORKFLOW_IDS,
    LOCAL_ONLY_AGENTS, DEEPSEEK_CANDIDATE_AGENTS,
    PAID_AI_BLOCK_KEYWORDS, PAID_AI_STRATEGIC_KEYWORDS,
)

# =============================================================================
# SECTION 9 ── Telegram 봇 핸들러 · 팀 지식 질문 처리
#   [대시보드 상태]
#   - send_state_to_dashboard, log_to_dashboard
#   [팀 지식 질문 플로우]
#   - handle_team_help/ask/more/ok/fix_command
#   - process_team_knowledge_question (로컬 score≥40 → 로컬, 미달 → 웹검색)
#   - process_team_more_request (더 찾아줘 보강)
#   [개발 요청 / 승인 / 거절]
#   - process_team_development_request
#   - handle_approve/reject_command
#   [자연어 메시지 라우팅]
#   - handle_team_natural_message, handle_telegram_message
#   - handle_telegram_document (PDF 이력서 처리)
# =============================================================================
async def send_state_to_dashboard():
    """전체 부서의 토큰 상태와 현재 가동 에이전트 패킷을 웹소켓으로 실시간 브로드캐스트합니다."""
    payload = {
        "type": "STATE_UPDATE",
        "data": copy.deepcopy(agent_states),
        "current": current_active_agent,
        "total_tokens": sum(int(a.get("tokens", 0)) for a in agent_states.values())
    }
    await manager.broadcast(json.dumps(payload, ensure_ascii=False))


async def log_to_dashboard(tag: str, message: str):
    """수신반에 실시간 로그 항목을 추가합니다."""
    payload = {
        "type": "DECISION_LOG",
        "tag": tag,
        "message": message,
    }
    await manager.broadcast(json.dumps(payload, ensure_ascii=False))


# 6. 텔레그램 이벤트 헨들러 라우터
async def handle_team_help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not telegram_chat_allowed(update):
        await update.message.reply_text("이 채팅방은 LUA BIM LABS 팀 요청 채널로 등록되어 있지 않습니다.")
        return
    await update.message.reply_text(
        "📘 [LUA BIM LABS 팀 지식 요청 사용법]\n\n"
        "팀원용 기능은 세 가지만 열려 있습니다.\n\n"
        "📚 지식질문: 기존 Obsidian 지식에서 먼저 답변합니다.\n"
        "🔎 더 찾아줘: 직전 답변이 부족할 때 추가 지식을 수집하고 Obsidian 갱신 후 다시 답변합니다.\n"
        "🧩 개발: 개발/자동화/툴 제작 요청을 조직 라우터로 넘깁니다.\n\n"
        "질문은 버튼을 누른 뒤 이어서 보내거나, 그냥 문장으로 보내도 됩니다.\n"
        "예: 덕트 점검구 기준 알려줘\n\n"
        "주의: 고객명, 프로젝트명, 도면, 계약정보, 개인정보는 Telegram에 올리지 마세요.",
        reply_markup=TEAM_REQUEST_KEYBOARD,
    )

async def handle_team_ask_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not telegram_chat_allowed(update):
        await update.message.reply_text("이 채팅방은 LUA BIM LABS 팀 요청 채널로 등록되어 있지 않습니다.")
        return
    raw_text = update.message.text or ""
    query = normalize_query_text(raw_text, "/ask")
    if not query:
        await update.message.reply_text("질문 내용을 함께 보내주세요. 예: /ask Revit 뷰 템플릿 복사 기준 알려줘")
        return
    await process_team_knowledge_question(update, query)

async def _synthesize_with_qwen(query: str, context: str) -> str:
    """로컬 Qwen 모델로 지식 컨텍스트를 자연어 답변으로 합성한다. 실패 시 빈 문자열 반환."""
    if not context or len(context) < 20:
        return ""
    # 마크다운 노이즈 제거 (헤더, 위키 링크, 소스/태그 메타라인)
    clean_lines = []
    for line in context.splitlines():
        stripped = line.strip()
        if not stripped:
            continue
        if stripped.startswith("##") or stripped.startswith("- Source:") or stripped.startswith("- Tags:") or stripped.startswith("- Links:"):
            continue
        stripped = re.sub(r"\[\[([^\]]+)\]\]", r"\1", stripped)
        clean_lines.append(stripped)
    clean_context = "\n".join(clean_lines).strip()
    if not clean_context:
        return ""
    result = await local_coder.generate_qa(
        prompt=(
            f"질문: {query}\n\n"
            f"참고 지식:\n{clean_context[:2000]}\n\n"
            "위 참고 지식을 바탕으로 질문에 대해 간결하고 실무적인 한국어로 답변하세요. "
            "마크다운 헤더나 메타 정보는 제외하고 핵심 내용만 자연스럽게 정리하세요."
        ),
        system=(
            "당신은 LUA BIM LABS의 MEP BIM 전문 어시스턴트입니다. "
            "제공된 지식 베이스를 참고해 질문에 실무적이고 자연스러운 한국어로 답변합니다. "
            "불필요한 헤더, 태그, 위키 링크 없이 핵심 내용만 전달합니다."
        ),
        timeout=30,
    )
    if result.get("ok") and result.get("response"):
        return sanitize_outbound_text(result["response"].strip())
    return ""


async def process_team_knowledge_question(update: Update, query: str):
    agent = infer_knowledge_agent_from_query(query)
    await log_to_dashboard("T4_TELEGRAM", f"📥 질문 수신: {query[:80]}")
    ensure_agent_state("지식업데이트")
    agent_states["지식업데이트"]["status"] = "Active"
    agent_states["지식업데이트"]["message"] = f"팀원 Telegram 질문 검색 중: {query[:80]}"
    await send_state_to_dashboard()

    progress_msg = await update.message.reply_text("🔍 검색 중...", reply_markup=TEAM_REQUEST_KEYBOARD)

    # 로컬 지식 먼저 조회
    local_matches = search_local_knowledge(query)
    top_score = local_matches[0]["score"] if local_matches else 0

    # 로컬 지식이 충분하면(score >= 40) 웹 검색 생략
    if top_score >= 40:
        search_result = ""
        await log_to_dashboard("T4_TELEGRAM", f"📚 로컬 지식으로 답변 (score={top_score}): {query[:50]}")
    else:
        web_task = asyncio.create_task(_search_web_for_knowledge(agent, query))
        search_result = await web_task

    # 웹 결과 + 로컬 지식을 컨텍스트로 조합
    raw_context = build_combined_answer(query, search_result, local_matches)

    # Qwen 로컬 모델로 자연어 합성 (가능한 경우)
    answer = await _synthesize_with_qwen(query, raw_context) or raw_context

    # 답변 소스 표기 (로컬 지식 베이스 / 웹 검색 구분)
    has_local = bool(local_matches and top_score >= 10)
    has_web   = bool(search_result)
    if has_local and has_web:
        source_tag = f"📚 지식 베이스 (score {top_score}) + 🔍 웹 검색 보강"
    elif has_local:
        source_tag = f"📚 지식 베이스 (score {top_score})"
    elif has_web:
        source_tag = "🔍 웹 검색"
    else:
        source_tag = "❓ 지식 없음 — 지식 베이스 보강 필요"
    answer = f"[{source_tag}]\n\n{answer}"

    # 수집된 지식을 도메인 파일에 저장 (운영 에이전트 제외)
    if search_result:
        _OPERATIONAL = {"지식업데이트", "지식큐레이터"}
        save_agent = agent if agent in KNOWLEDGE_AGENTS and agent not in _OPERATIONAL else infer_knowledge_agent_from_query(query)
        if save_agent in _OPERATIONAL:
            save_agent = "건축"
        # 도메인 지식 파일에는 정제된 답변만 저장 (raw 검색 결과 전체 X)
        clean_answer = sanitize_outbound_text(answer.split("\n\n📚")[0].strip())
        if clean_answer and len(clean_answer) > 20:
            append_knowledge_update(KnowledgeUpdateRequest(
                agent=save_agent,
                title=f"Q: {query[:60]}",
                source="telegram-qa",
                tags="qa,auto-collect",
                content=clean_answer,
            ))
        # 운영 로그는 별도 파일에만 기록
        append_auto_knowledge_gap_log(
            query=query, agent=agent,
            assessment={"reasons": [], "top_score": 0, "top_path": ""},
            search_result=search_result,
        )

    await update_reply_progress(progress_msg, answer)
    qa_note_path = save_team_qa_to_obsidian(
        update=update,
        query=query,
        answer=answer,
        agent=agent,
        matches=local_matches,
    )
    key = telegram_session_key(update)
    TELEGRAM_KNOWLEDGE_SESSIONS[key] = {
        "query": query,
        "agent": agent,
        "matches": [
            {
                "path": str(match["path"].relative_to(PROJECT_ROOT)),
                "score": match["score"],
            }
            for match in local_matches
        ],
        "answer": answer,
        "qa_note_path": str(qa_note_path),
        "created_at": datetime.datetime.now().isoformat(timespec="seconds"),
    }
    append_team_request_log(
        update=update,
        query=query,
        action="ask",
        agent=agent,
        result=f"{answer}\n\nObsidian Q&A 기록: {qa_note_path.relative_to(PROJECT_ROOT)}",
    )
    await refresh_obsidian_after_knowledge_update()

    agent_states["지식업데이트"]["status"] = "Idle"
    agent_states["지식업데이트"]["tokens"] += 1
    await send_state_to_dashboard()

async def handle_team_more_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not telegram_chat_allowed(update):
        await update.message.reply_text("이 채팅방은 LUA BIM LABS 팀 요청 채널로 등록되어 있지 않습니다.")
        return

    extra = normalize_query_text(update.message.text or "", "/more")
    await process_team_more_request(update, extra)

async def process_team_more_request(update: Update, extra: str = ""):
    key = telegram_session_key(update)
    session = TELEGRAM_KNOWLEDGE_SESSIONS.get(key)
    if not session or not session.get("query"):
        await update.message.reply_text("보강할 최근 지식 질문이 없습니다. 먼저 📚 지식질문을 눌러 질문을 보내주세요.", reply_markup=TEAM_REQUEST_KEYBOARD)
        return

    query = session["query"]
    agent = session["agent"]
    progress_msg = await update.message.reply_text(
        "🔎 [더 찾아줘 접수]\n\n"
        "기존 답변의 부족분을 기준으로 추가 지식을 수집하고 있습니다. "
        "수집 결과를 지식베이스와 Obsidian에 반영한 뒤 다시 답변드리겠습니다.",
        reply_markup=TEAM_REQUEST_KEYBOARD,
    )
    content = (
        "팀원이 기존 Obsidian 답변이 부족하다고 회신했다.\n\n"
        f"원 질문: {query}\n"
        f"추가 요청: {extra or '추가 설명 없음'}\n\n"
        "처리 기준:\n"
        "1. 내부 지식에서 누락된 기준을 우선 보강한다.\n"
        "2. 외부 검색 또는 공식 문서 확인이 필요한 항목은 자동 수집 후 지식 업데이트 후보로 표시한다.\n"
        "3. 고객명, 프로젝트명, 개인정보는 수집하지 않는다."
    )
    gap_result = append_knowledge_update(KnowledgeUpdateRequest(
        agent=agent,
        title="Telegram 팀원 보강 요청",
        source=f"telegram:{telegram_user_label(update)}",
        tags="telegram,team-request,knowledge-gap,needs-review",
        content=content,
    ))

    ensure_agent_state("지식업데이트")
    agent_states["지식업데이트"]["status"] = "Active"
    agent_states["지식업데이트"]["message"] = f"{agent} 추가 지식 자동 수집 중: {query[:80]}"
    await send_state_to_dashboard()

    search_prompt = f"{query}\n\n추가 요청: {extra or '부족한 부분을 더 찾아줘'}"
    search_result = await _search_web_for_knowledge(agent, search_prompt)
    if search_result:
        collected_result = append_knowledge_update(KnowledgeUpdateRequest(
            agent=agent,
            title="Telegram 더 찾아줘 자동 수집 결과",
            source=f"telegram-auto-search:{telegram_user_label(update)}",
            tags="telegram,team-request,auto-collect,needs-review",
            content=(
                f"원 질문: {query}\n"
                f"추가 요청: {extra or '추가 설명 없음'}\n\n"
                "자동 수집 결과:\n\n"
                f"{search_result}\n\n"
                "검토 기준: 공식 문서 여부, 최신성, 프로젝트 적용 가능성, 보안/개인정보 포함 여부를 확인한 뒤 표준/교육/FAQ 후보로 승격한다."
            ),
        ))
    else:
        collected_result = gap_result

    await update_reply_progress(
        progress_msg,
        "🧭 [지식 업데이트 중]\n\n"
        f"담당 지식: {agent}\n"
        f"보강 기록: {Path(gap_result['path']).relative_to(PROJECT_ROOT)}\n"
        "Obsidian 그래프와 전역 지식맵을 갱신하고 있습니다.",
    )
    append_team_qa_feedback(
        session.get("qa_note_path"),
        "보강요청",
        f"추가 요청: {extra or '추가 설명 없음'}\n"
        f"보강 등록 위치: {Path(gap_result['path']).relative_to(PROJECT_ROOT)}\n"
        f"자동 수집 위치: {Path(collected_result['path']).relative_to(PROJECT_ROOT)}\n\n"
        f"{search_result or '자동 수집 결과 없음. 지식 공백으로 검토 필요.'}",
    )
    await refresh_obsidian_after_knowledge_update()

    refreshed_matches = search_local_knowledge(query, limit=5)
    final_answer = build_more_research_answer(query, agent, search_result, refreshed_matches)
    session["answer"] = final_answer
    session["matches"] = [
        {
            "path": str(match["path"].relative_to(PROJECT_ROOT)),
            "score": match["score"],
        }
        for match in refreshed_matches
    ]
    session["updated_at"] = datetime.datetime.now().isoformat(timespec="seconds")
    append_team_request_log(
        update=update,
        query=query,
        action="more",
        agent=agent,
        result=(
            f"보강 요청 등록: {gap_result['path']}\n"
            f"자동 수집 등록: {collected_result['path']}\n\n"
            f"{final_answer}"
        ),
    )
    agent_states["지식업데이트"]["status"] = "Idle"
    agent_states["지식업데이트"]["tokens"] += 1
    await send_state_to_dashboard()

    await update_reply_progress(progress_msg, final_answer)

async def handle_team_ok_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not telegram_chat_allowed(update):
        await update.message.reply_text("이 채팅방은 LUA BIM LABS 팀 요청 채널로 등록되어 있지 않습니다.")
        return
    key = telegram_session_key(update)
    session = TELEGRAM_KNOWLEDGE_SESSIONS.get(key)
    if not session:
        await update.message.reply_text("완료 처리할 최근 지식 질문이 없습니다.", reply_markup=TEAM_REQUEST_KEYBOARD)
        return
    append_team_request_log(
        update=update,
        query=session["query"],
        action="ok",
        agent=session["agent"],
        result="사용자가 기존 Obsidian 답변이 충분하다고 확인함.",
    )
    append_team_qa_feedback(
        session.get("qa_note_path"),
        "충분",
        "사용자가 기존 Obsidian 답변이 충분하다고 확인함.",
    )
    await refresh_obsidian_after_knowledge_update()
    await update.message.reply_text("✅ 확인했습니다. 해당 답변을 충분한 지식 응답으로 기록했습니다.", reply_markup=TEAM_REQUEST_KEYBOARD)

async def handle_team_fix_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not telegram_chat_allowed(update):
        await update.message.reply_text("이 채팅방은 LUA BIM LABS 팀 요청 채널로 등록되어 있지 않습니다.")
        return
    raw = normalize_query_text(update.message.text or "", "/fix")
    parts = [part.strip() for part in raw.split("|", 2)]
    if len(parts) < 3:
        await update.message.reply_text("형식: /fix 담당분야 | 제목 | 추가할 기준", reply_markup=TEAM_REQUEST_KEYBOARD)
        return
    agent, title, content = parts
    if agent not in KNOWLEDGE_AGENTS:
        agent = infer_knowledge_agent_from_query(agent)
    result = append_knowledge_update(KnowledgeUpdateRequest(
        agent=agent,
        title=title,
        source=f"telegram:{telegram_user_label(update)}",
        tags="telegram,team-fix,manual-knowledge",
        content=content,
    ))
    append_team_request_log(update=update, query=raw, action="fix", agent=agent, result=f"직접 지식 추가: {result['path']}")
    await refresh_obsidian_after_knowledge_update()
    await update.message.reply_text(
        "🛠️ [지식 직접 반영 완료]\n\n"
        f"담당 지식: {agent}\n"
        f"업데이트 위치: {Path(result['path']).relative_to(PROJECT_ROOT)}\n"
        "Obsidian 그래프 갱신까지 완료했습니다.",
        reply_markup=TEAM_REQUEST_KEYBOARD,
    )

async def handle_approve_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_owner_telegram_chat(update):
        await update.message.reply_text("승인 권한이 없습니다.")
        return
    if not context.args:
        await update.message.reply_text("형식: /approve 요청ID")
        return
    request_id = context.args[0].strip()
    registry, item = find_management_excel_request(request_id)
    if not item:
        await update.message.reply_text(f"요청 ID를 찾지 못했습니다: {request_id}")
        return
    if item.get("status") not in {"pending_approval", "rejected"}:
        await update.message.reply_text(f"이미 처리된 요청입니다. 현재 상태: {item.get('status')}")
        return

    now = datetime.datetime.now().isoformat(timespec="seconds")
    item["status"] = "approved_running"
    item["approved_at"] = now
    item["approved_by"] = telegram_user_label(update)
    item["execution_note"] = "승인 후 corporate excel automation pipeline 실행"
    save_management_excel_requests(registry)

    reply_msg = await update.message.reply_text(
        "✅ [관리팀 Excel 자동화 승인]\n\n"
        f"요청 ID: {item['id']}\n"
        "자동화 파이프라인을 실행합니다.",
        reply_markup=TEAM_REQUEST_KEYBOARD,
    )
    launch_background_task(process_corporate_pipeline(
        "관리팀 Excel 자동화 승인 요청\n"
        f"요청 ID: {item['id']}\n"
        f"요청자: {item['requester']}\n"
        f"요청 내용:\n{item['request_text']}\n\n"
        "처리 기준:\n"
        "1. 실제 파일을 직접 변경하기 전 샘플 데이터와 출력 스키마를 먼저 확정한다.\n"
        "2. Python/openpyxl 기반 자동화를 우선 검토한다.\n"
        "3. 개인정보/급여/계약정보가 포함되면 실행 전 보안 검토로 중단한다.\n"
        "4. 산출물은 XLSX/CSV, 검증 로그, 처리 요약을 포함한다.",
        reply_msg,
    ))

async def handle_reject_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_owner_telegram_chat(update):
        await update.message.reply_text("반려 권한이 없습니다.")
        return
    if not context.args:
        await update.message.reply_text("형식: /reject 요청ID 사유")
        return
    request_id = context.args[0].strip()
    reason = " ".join(context.args[1:]).strip() or "사유 미기재"
    registry, item = find_management_excel_request(request_id)
    if not item:
        await update.message.reply_text(f"요청 ID를 찾지 못했습니다: {request_id}")
        return

    item["status"] = "rejected"
    item["rejected_at"] = datetime.datetime.now().isoformat(timespec="seconds")
    item["rejected_by"] = telegram_user_label(update)
    item["rejection_reason"] = reason
    save_management_excel_requests(registry)
    await update.message.reply_text(
        "⛔ [관리팀 Excel 자동화 반려]\n\n"
        f"요청 ID: {item['id']}\n"
        f"사유: {reason}",
        reply_markup=TEAM_REQUEST_KEYBOARD,
    )

async def process_team_development_request(update: Update, request_text: str):
    key = telegram_session_key(update)
    TELEGRAM_KNOWLEDGE_SESSIONS[key] = {
        **TELEGRAM_KNOWLEDGE_SESSIONS.get(key, {}),
        "pending_mode": None,
    }
    if is_management_excel_automation_request(request_text):
        reply_msg = await update.message.reply_text(
            "📊 [관리팀 Excel 자동화 요청 접수]\n\n"
            "승인 없이 Qwen Coder 기반 자동화 검토를 시작합니다.\n"
            "DeepSeek API는 사용하지 않으며, Mac에 결과 파일을 저장하지 않고 Telegram으로 결과를 회신합니다.",
            reply_markup=TEAM_REQUEST_KEYBOARD,
        )
        launch_background_task(process_corporate_pipeline(
            "관리팀 Excel 자동화 요청\n"
            f"요청자: {telegram_user_label(update)}\n"
            f"요청 내용:\n{request_text}\n\n"
            "처리 기준:\n"
            "1. DeepSeek API 사용 금지.\n"
            "2. Qwen_Coder_8B와 엑셀자동화가 Python/openpyxl 기반 초안을 우선 작성.\n"
            "3. 실제 회사 파일은 Mac에 저장하지 않고, 샘플 구조와 Telegram 회신 가능한 코드/절차/검증표만 작성.\n"
            "4. 개인정보, 급여, 계약, 계정정보 등 중요 데이터는 답변에 포함하지 말고 마스킹/제외 기준을 제시.\n"
            "5. 최종 결과물은 Telegram 메시지로 질문자에게 전달.",
            reply_msg,
            force_local_only=True,
            deliver_full_result=True,
        ))
        return

    reply_msg = await update.message.reply_text(
        "🧩 [개발 요청 접수]\n"
        "Qwen Coder와 로컬 지식 기반으로 개발/자동화 라우터에 넘깁니다. DeepSeek API는 사용하지 않습니다.",
        reply_markup=TEAM_REQUEST_KEYBOARD,
    )
    launch_background_task(process_corporate_pipeline(
        "팀원 개발 요청\n"
        f"요청자: {telegram_user_label(update)}\n"
        f"요청 내용:\n{request_text}\n\n"
        "처리 기준: DeepSeek API 사용 금지, Qwen Coder/로컬 지식 기반 개발 허용, Mac 로컬 결과물 저장 금지, Telegram 최종 회신.",
        reply_msg,
        force_local_only=True,
        deliver_full_result=True,
    ))

async def handle_team_natural_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> bool:
    if not telegram_chat_allowed(update):
        return False
    text = normalize_team_button_text(update.message.text or "")
    if not text:
        return True

    key = telegram_session_key(update)
    session = TELEGRAM_KNOWLEDGE_SESSIONS.setdefault(key, {})

    if text == "📚 지식질문":
        session["pending_mode"] = "ask"
        await update.message.reply_text("📚 지식 질문 내용을 보내주세요. 예: 덕트 점검구 기준 알려줘", reply_markup=TEAM_REQUEST_KEYBOARD)
        return True
    if text == "🔎 더 찾아줘":
        await process_team_more_request(update)
        return True
    if text == "🧩 개발":
        session["pending_mode"] = "development"
        await update.message.reply_text("🧩 개발/자동화 요청 내용을 보내주세요. 예: Navisworks 간섭 결과를 담당자별 Excel로 정리하고 싶어", reply_markup=TEAM_REQUEST_KEYBOARD)
        return True

    pending_mode = session.get("pending_mode")
    if pending_mode == "development":
        session["pending_mode"] = None
        await process_team_development_request(update, text)
        return True
    if pending_mode == "ask":
        session["pending_mode"] = None
        await process_team_knowledge_question(update, text)
        return True

    if any(keyword in text for keyword in ["더 찾아줘", "부족", "보강", "추가로 찾아", "다시 찾아"]):
        await process_team_more_request(update, text)
        return True
    if text.startswith("개발") or text.startswith("자동화") or any(keyword in text.lower() for keyword in ["addin", "add-in", "revit api", "navisworks api", "qwen"]):
        await process_team_development_request(update, text)
        return True

    await process_team_knowledge_question(update, text)
    return True

async def handle_telegram_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    if not user_text:
        return

    if await handle_team_natural_message(update, context):
        return

    # 비동기 백그라운드 파이프라인 태스크 런칭
    await log_to_dashboard("T4_TELEGRAM", f"📥 기업 파이프라인 요청: {user_text[:80]}")
    reply_msg = await update.message.reply_text("🏢 [LUA BIM LABS 기업 라우터] 요청 접수 완료. 의도 분석을 시작합니다...")
    launch_background_task(process_corporate_pipeline(user_text, reply_msg))

async def handle_telegram_document(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not telegram_chat_allowed(update):
        await update.message.reply_text("이 채팅방은 LUA BIM LABS 팀 요청 채널로 등록되어 있지 않습니다.")
        return
    document = update.message.document if update.message else None
    if not document:
        return
    if not is_resume_document(update):
        await update.message.reply_text(
            "📎 파일을 받았습니다. 이력서 분석 대상이면 PDF 파일명 또는 캡션에 `이력서`, `resume`, `cv`, `지원자`, `채용` 중 하나를 포함해 다시 보내주세요.",
            reply_markup=TEAM_REQUEST_KEYBOARD,
        )
        return

    ensure_agent_state("HR_인재분석관")
    agent_states["HR_인재분석관"]["status"] = "Active"
    agent_states["HR_인재분석관"]["message"] = "Telegram 이력서 PDF 수신. 로컬 텍스트 추출 및 분석 준비 중."
    await send_state_to_dashboard()

    progress_msg = await update.message.reply_text(
        "🧾 [HR_인재분석관 이력서 접수]\n\n"
        "PDF를 로컬로 내려받아 텍스트 추출을 시도합니다. 외부 API에는 원본 파일을 보내지 않습니다.",
        reply_markup=TEAM_REQUEST_KEYBOARD,
    )
    now = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    safe_file_name = re.sub(r"[^A-Za-z0-9가-힣_.-]+", "_", document.file_name or "resume.pdf")
    intake_dir = RESUME_INTAKE_DIR / now
    intake_dir.mkdir(parents=True, exist_ok=True)
    pdf_path = intake_dir / safe_file_name

    try:
        tg_file = await context.bot.get_file(document.file_id)
        await tg_file.download_to_drive(custom_path=str(pdf_path))
        text, extractor = extract_pdf_text_local(pdf_path)
        if not text:
            await update_reply_progress(
                progress_msg,
                "⚠️ [로컬 PDF 텍스트 추출 불가]\n\n"
                "현재 환경에 `pypdf`, `PyPDF2`, `pdfplumber`, `pdftotext` 중 사용 가능한 로컬 PDF 추출기가 없습니다. "
                "스캔본 PDF라면 OCR도 필요합니다.\n\n"
                "DeepSeek 보조 분석은 원본 PDF를 직접 보내지 않고, 텍스트 추출 및 개인정보 마스킹이 된 경우에만 사용할 수 있습니다.",
            )
            return

        masked_text = sanitize_resume_text_for_ai(text)
        report = build_local_resume_report(text, document.file_name or safe_file_name)
        deepseek_report = await deepseek_resume_report(masked_text, document.file_name or safe_file_name)
        if deepseek_report:
            report = (
                "🧠 [DeepSeek 보조 분석 사용]\n"
                "- 조건: RESUME_DEEPSEEK_FALLBACK_ENABLED + PAID_AI_ENABLED 활성\n"
                "- 원본 PDF 전송: 없음\n"
                "- 전송 텍스트: 로컬 추출 후 마스킹된 텍스트\n\n"
                f"{deepseek_report}"
            )

        report_path = intake_dir / "resume_analysis_report.md"
        report_path.write_text(report + "\n", encoding="utf-8")
        append_team_request_log(
            update=update,
            query=f"Telegram 이력서 PDF 분석: {document.file_name}",
            action="resume-analysis",
            agent="HR_인재분석관",
            result=f"extractor={extractor}\nreport={report_path.relative_to(PROJECT_ROOT)}\n\n{report}",
        )
        await update_reply_progress(progress_msg, report)
    except Exception as exc:
        await update_reply_progress(
            progress_msg,
            f"⚠️ [이력서 분석 실패]\n\n로컬 처리 중 오류가 발생했습니다: {sanitize_outbound_text(str(exc))}",
        )
    finally:
        agent_states["HR_인재분석관"]["status"] = "Idle"
        agent_states["HR_인재분석관"]["tokens"] += 1
        await send_state_to_dashboard()

async def run_dashboard_addin_task(task: AddinTaskRequest):
    prompt = (
        f"[{task.target} Add-in 개발 요청]\n"
        f"공정: {task.discipline}\n"
        f"우선순위: {task.priority}\n"
        f"제목: {task.title}\n"
        f"요청 내용:\n{task.request}"
    )
    await process_corporate_pipeline(prompt, DashboardReply())

# 7. FastAPI 엔드포인트 및 웹소켓 터널
async def dashboard_websocket_session(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        # 최초 연결 시 현재까지 누적된 상태값 스냅샷 즉시 밀어주기
        await send_state_to_dashboard()
        while True:
            raw_message = await websocket.receive_text()
            if not raw_message:
                continue
            try:
                command = json.loads(raw_message)
            except json.JSONDecodeError:
                continue
            if command.get("type") == "PING":
                await websocket.send_text(json.dumps({"type": "PONG"}, ensure_ascii=False))
    except WebSocketDisconnect:
        manager.disconnect(websocket)
    except Exception as exc:
        print(f"⚠️ [웹소켓] 예외 종료: {exc}")
        manager.disconnect(websocket)

# =============================================================================
# SECTION 10 ── FastAPI HTTP / WebSocket 엔드포인트 · 서버 시작/종료
#   [WebSocket]
#   - /ws/office  (대시보드 실시간 상태)
#   - /ws/state   (하위 호환)
#   [HTTP API]
#   - GET  /dashboard, /
#   - POST /api/addin-task, /api/knowledge-update
#   - GET  /api/knowledge-agents, /api/collaboration-workflows
#   - GET  /api/github/status, /api/github/repos
#   - GET  /api/local-coder/status, POST /api/local-coder/draft
#   - GET/POST /api/bim-command-center/*, /api/revit-assistant/*
#   [서버 라이프사이클]
#   - startup_event (Telegram 봇 초기화, Obsidian MOC 생성)
#   - shutdown_event (Telegram 봇 종료)
# =============================================================================
@app.websocket("/ws/office")
async def websocket_endpoint(websocket: WebSocket):
    await dashboard_websocket_session(websocket)

@app.websocket("/ws/state")
async def websocket_state_compat_endpoint(websocket: WebSocket):
    await dashboard_websocket_session(websocket)

@app.get("/")
async def health_check():
    return {
        "status": "running",
        "service": "LUA BIM LABS integrated backend",
        "agents": ALL_AGENTS,
        "telegram_enabled": bool(os.environ.get("TELEGRAM_BOT_TOKEN")),
        "telegram_chat_configured": bool(TELEGRAM_CHAT_ID),
        "github_configured": github_integration.is_configured(),
        "local_coder_enabled": local_coder.enabled(),
    }

@app.get("/dashboard")
async def dashboard():
    return FileResponse(FRONTEND_DIR / "index.html")

@app.post("/api/addin-task")
async def create_addin_task(task: AddinTaskRequest):
    if not task.request.strip():
        return {"status": "rejected", "reason": "request is empty"}
    launch_background_task(run_dashboard_addin_task(task))
    return {
        "status": "accepted",
        "target": task.target,
        "title": task.title
    }

@app.get("/api/knowledge-agents")
async def list_knowledge_agents():
    ensure_knowledge_base()
    return {
        "agents": KNOWLEDGE_AGENTS,
        "directory": KNOWLEDGE_DIR
    }

@app.post("/api/knowledge-update")
async def create_knowledge_update(update: KnowledgeUpdateRequest):
    try:
        result = append_knowledge_update(update)
    except ValueError as exc:
        return {"status": "rejected", "reason": str(exc)}
    ensure_agent_state(update.agent)
    agent_states[update.agent]["message"] = f"지식 업데이트 반영: {update.title[:60]}"
    agent_states[update.agent]["tokens"] += 1
    await send_state_to_dashboard()
    return {
        "status": "updated",
        **result,
    }

@app.get("/api/collaboration-workflows")
async def list_collaboration_workflows():
    workflows = active_collaboration_workflows()
    return {
        "workflows": [
            {
                "id": workflow["id"],
                "name": workflow["name"],
                "primary": workflow["primary"],
                "participants": workflow["participants"],
                "steps": workflow["steps"],
                "local_only": workflow["local_only"],
            }
            for workflow in workflows
        ]
    }

@app.get("/api/role-boundaries")
async def list_role_boundaries():
    return {"roles": collaboration.ROLE_BOUNDARIES}

@app.get("/api/collaboration-audit")
async def collaboration_audit():
    workflows = active_collaboration_workflows()
    return {
        "workflow_count": len(workflows),
        "issues": collaboration.audit_collaboration_workflows(workflows),
    }

@app.get("/api/daily-idea-report")
async def daily_idea_report():
    report = collaboration.build_daily_idea_report(limit=3)
    for participant in report["participants"]:
        ensure_agent_state(participant)
        agent_states[participant]["status"] = "Idle"
    agent_states["아이디어발굴"]["message"] = "최고지배자 일일 3대 아이디어 보고 준비 완료. 유료 API 호출 없이 로컬 산식으로 산출."
    return {
        "status": "ok",
        **report,
    }

@app.get("/api/knowledge-gap/persistent")
async def persistent_knowledge_gaps(min_count: int = 3):
    """min_count 이상 반복된 미해결 지식 갭 목록 반환."""
    gaps = get_persistent_gaps(min_count=min_count)
    return {
        "status": "ok",
        "min_count": min_count,
        "total": len(gaps),
        "gaps": gaps,
    }


@app.get("/api/github/status")
async def github_status():
    try:
        result = await github_integration.check_connection()
    except github_integration.GitHubIntegrationError as exc:
        return {
            "status": "error",
            "configured": github_integration.is_configured(),
            "reason": str(exc),
        }
    agent_states["인프라_DevOps (Obsidian)"]["message"] = (
        "GitHub 연동 상태 확인 완료. 토큰은 환경변수에서만 읽고 응답에는 노출하지 않음."
    )
    return result

@app.get("/api/github/repos")
async def github_repositories(limit: int = 20):
    try:
        result = await github_integration.list_repositories(limit=limit)
    except github_integration.GitHubIntegrationError as exc:
        return {
            "status": "error",
            "configured": github_integration.is_configured(),
            "reason": str(exc),
        }
    return {
        "status": "ok",
        **result,
    }

@app.get("/api/local-coder/status")
async def local_coder_status():
    result = await local_coder.status()
    ensure_agent_state("Qwen_Coder_8B")
    agent_states["Qwen_Coder_8B"]["message"] = (
        f"로컬 코더 상태 확인: {result['provider']} / {result['model']} / "
        f"reachable={result.get('reachable')} / model_available={result.get('model_available')}"
    )
    return {
        "status": "ok",
        **result,
    }

@app.post("/api/local-coder/draft")
async def local_coder_draft(draft: LocalCoderDraftRequest):
    if not draft.request.strip():
        return {"status": "rejected", "reason": "request is empty"}
    workflows = active_collaboration_workflows()
    workflow = collaboration.workflow_by_id(workflows, draft.workflow) or collaboration.workflow_by_id(workflows, "local_qwen_development") or workflows[0]
    workflow_specific_rules = ""
    if workflow["id"] == "excel_qwen_automation":
        workflow_specific_rules = (
            "현재 요청은 엑셀 자동화입니다. pandas를 사용하거나 언급하지 마세요. "
            "CSV 처리는 Python 표준 csv 라이브러리로 수행하고, XLSX 생성과 필터 표는 openpyxl로만 작성하세요.\n"
        )
    result = await local_coder.generate(
        (
            f"요청:\n{draft.request}\n\n"
            f"협업 프로세스: {workflow['name']}\n"
            f"{workflow_specific_rules}"
            "구현 언어 규칙: 엑셀 자동화는 반드시 Python 표준 csv 라이브러리 + openpyxl을 우선 제안하세요. "
            "pandas는 사용자가 명시적으로 요청하거나 대용량 분석이 필요한 경우에만 제안하세요. "
            "C# OpenXML은 .NET Add-in 연계가 명시된 경우에만 제안하세요. "
            "Lua 언어는 절대 제안하지 마세요.\n"
            "반드시 아래 4개 제목을 빠짐없이 사용하세요: Plan, Draft, Verification, API 필요성 판단. "
            "각 제목은 1-2문장만 작성하세요. "
            "API 필요성 판단에는 외부 API/Revit API/Navisworks API 호출 필요 여부와 '필요/불필요' 결론을 명시하세요. "
            "여기서 API 필요성 판단은 API Gateway 배포가 아니라 외부 API/Revit API/Navisworks API 호출 필요 여부를 의미합니다."
        ),
        system=(
            "당신은 LUA BIM LABS의 로컬 Qwen 코더입니다. 모든 개발은 목적과 검증 plan을 먼저 세웁니다. "
            "엑셀 자동화 기본 구현은 Python 표준 csv 라이브러리와 openpyxl 조합이며 .NET Add-in 연계가 필요할 때만 C# OpenXML을 제안합니다. "
            "응답은 항상 Plan, Draft, Verification, API 필요성 판단 네 섹션을 모두 포함합니다. "
            "Lua 언어는 사용자가 명시적으로 요청한 경우에만 제안합니다."
        ),
        num_predict=320,
        timeout=30,
    )
    return {
        "status": "ok" if result.get("ok") else "error",
        "workflow_id": workflow["id"],
        **result,
    }

@app.get("/api/qwen-product-drafts/status")
async def qwen_product_drafts_status():
    queue = qwen_product_drafts.load_queue()
    state = qwen_product_drafts.load_state()
    completed = set(state.get("completed", []))
    remaining = [task["id"] for task in queue.get("tasks", []) if task["id"] not in completed]
    return {
        "status": "ok",
        "product": queue["product"],
        "selected_item": queue["selected_item"],
        "completed": state.get("completed", []),
        "in_progress": state.get("in_progress"),
        "remaining": remaining,
        "last_report": state.get("last_report"),
    }

@app.post("/api/qwen-product-drafts/next")
async def qwen_product_drafts_next(request: QwenProductDraftRunRequest):
    result = await qwen_product_drafts.run_next(
        max_tasks=max(1, min(request.max_tasks, 3)),
        send_reports=request.send_telegram,
        advance_on_blocked=request.advance_on_blocked,
    )
    ensure_agent_state("Qwen_Coder_8B")
    latest = result.get("runs", [])[-1] if result.get("runs") else {}
    agent_states["Qwen_Coder_8B"]["status"] = "Idle"
    agent_states["Qwen_Coder_8B"]["message"] = (
        f"Model Quality Auditor 초안 큐 처리: {latest.get('task_id', 'none')} / "
        f"ok={latest.get('ok')} / next={latest.get('next_task')}"
    )
    await send_state_to_dashboard()
    return result

@app.get("/api/bim-command-center/features")
async def bim_command_center_features():
    errors = validate_feature_registry()
    return {
        "status": "ok" if not errors else "invalid",
        "product": "BIM Command Center for Revit",
        "selected_item": "BIMlize 기능 범위 내재화 - Phase 1 Simple Features",
        "principle": "Use benchmark scope only; do not copy names, UI, icons, text, or implementation.",
        "validation_errors": errors,
        "features": list_phase1_features(),
    }

@app.get("/api/bim-command-center/settings-profiles")
async def list_bim_command_center_settings_profiles(scope=None):
    try:
        profile_scope = ProfileScope(scope) if scope else None
        rows = default_profile_store(PROJECT_ROOT / "data" / "bim_command_center" / "settings_profiles").list_profiles(profile_scope)
    except (ValueError, SettingsProfileError) as exc:
        return {"status": "rejected", "reason": str(exc)}
    return {"status": "ok", "profiles": rows}

@app.post("/api/bim-command-center/settings-profiles")
async def save_bim_command_center_settings_profile(request: SettingsProfileSaveRequest):
    try:
        profile = SettingsProfile(
            name=request.name,
            scope=ProfileScope(request.scope),
            description=request.description,
            settings=request.settings,
        )
        path = default_profile_store(PROJECT_ROOT / "data" / "bim_command_center" / "settings_profiles").save(profile)
    except (ValueError, SettingsProfileError) as exc:
        return {"status": "rejected", "reason": str(exc)}
    return {
        "status": "saved",
        "profile": profile.to_dict(),
        "path": path.relative_to(PROJECT_ROOT).as_posix(),
    }

@app.post("/api/route-preview")
async def route_preview(preview: RoutePreviewRequest):
    if not preview.request.strip():
        return {"status": "rejected", "reason": "request is empty"}
    return {
        "status": "ok",
        **preview_collaboration_route(preview.request),
    }

@app.post("/api/revit-assistant/chat")
async def revit_assistant_chat(
    request: RevitAssistantChatRequest,
    x_lua_bim_api_key: Optional[str] = Header(default=None, alias="X-LUA-BIM-API-Key"),
):
    require_revit_assistant_api_key(x_lua_bim_api_key)
    if not request.message.strip():
        return {"status": "rejected", "reason": "message is empty"}

    query_with_context = build_revit_context_prompt(request.message, request.revit_context)
    agent = infer_knowledge_agent_from_query(query_with_context)
    matches = prioritize_agent_matches(search_local_knowledge(query_with_context, limit=5), agent)
    top_score = matches[0]["score"] if matches else 0
    search_result = ""

    if top_score >= 40:
        # 지식 베이스로 충분히 답변 가능
        answer = build_revit_assistant_answer(query_with_context, matches, agent)
        source_tag = f"📚 지식 베이스 (score {top_score})"
    else:
        # 지식 부족 → 웹 검색 후 합성하고, 확정 지식이 아닌 검토 후보로 축적
        search_result = await _search_web_for_knowledge(agent, query_with_context)
        raw_context = build_combined_answer(query_with_context, search_result, matches)
        answer = await _synthesize_with_qwen(query_with_context, raw_context) or raw_context

        has_local = bool(matches and top_score >= 10)
        has_web = bool(search_result)
        if has_local and has_web:
            source_tag = f"📚 지식 베이스 (score {top_score}) + 🔍 웹 검색 보강"
        elif has_local:
            source_tag = f"📚 지식 베이스 (score {top_score})"
        elif has_web:
            source_tag = "🔍 웹 검색"
        else:
            source_tag = "❓ 지식 없음 — 지식 베이스 보강 필요"

        if search_result:
            _OPERATIONAL = {"지식업데이트", "지식큐레이터"}
            save_agent = agent if agent in KNOWLEDGE_AGENTS and agent not in _OPERATIONAL else infer_knowledge_agent_from_query(query_with_context)
            if save_agent in _OPERATIONAL:
                save_agent = "건축"
            clean_answer = sanitize_outbound_text(answer.split("\n\n📚")[0].strip())
            if clean_answer and len(clean_answer) > 20:
                append_knowledge_update(KnowledgeUpdateRequest(
                    agent=save_agent,
                    title=f"Q: {request.message[:60]}",
                    source="search-assisted-qa",
                    tags="qa,auto-collect,revit-addin,search-assisted,knowledge-candidate,needs-review",
                    content=(
                        f"Status: needs-review\n\n"
                        f"Question:\n{sanitize_outbound_text(request.message.strip())}\n\n"
                        f"Draft answer:\n{clean_answer}\n\n"
                        f"Search evidence:\n{sanitize_outbound_text(search_result.strip())[:2500]}"
                    ),
                ))
            append_auto_knowledge_gap_log(
                query=query_with_context, agent=agent,
                assessment={"reasons": [], "top_score": top_score, "top_path": ""},
                search_result=search_result,
            )

    answer = f"[{source_tag}]\n\n{answer}"

    note_path = save_revit_qa_to_obsidian(
        request=request,
        answer=answer,
        agent=agent,
        matches=matches,
        search_result=search_result,
        source_tag=source_tag,
        top_score=top_score,
    )

    ensure_agent_state(agent)
    agent_states[agent]["status"] = "Active"
    agent_states[agent]["message"] = f"Revit Assistant 질문 처리: {request.message[:60]}"
    agent_states[agent]["tokens"] += 1
    ensure_agent_state("지식업데이트")
    agent_states["지식업데이트"]["message"] = "Revit Assistant Q&A를 Obsidian 지식 루프에 기록했습니다."
    await send_state_to_dashboard()
    agent_states[agent]["status"] = "Idle"
    await send_state_to_dashboard()
    launch_background_task(refresh_obsidian_after_knowledge_update())

    sources = []
    for match in matches[:5]:
        match_path = match.get("path")
        if isinstance(match_path, Path):
            try:
                rel = match_path.relative_to(PROJECT_ROOT).as_posix()
            except ValueError:
                rel = match_path.as_posix()
        else:
            rel = str(match_path)
        sources.append({"path": rel, "score": match.get("score", 0)})

    return {
        "status": "ok",
        "brand": "LUA BIM LABS",
        "agent": agent,
        "answer": answer,
        "sources": sources,
        "note_path": note_path.relative_to(PROJECT_ROOT).as_posix(),
        "needs_more": not bool(matches) and not bool(search_result),
    }

@app.post("/api/revit-assistant/feedback")
async def revit_assistant_feedback(
    request: RevitAssistantFeedbackRequest,
    x_lua_bim_api_key: Optional[str] = Header(default=None, alias="X-LUA-BIM-API-Key"),
):
    require_revit_assistant_api_key(x_lua_bim_api_key)
    note_path = PROJECT_ROOT / request.note_path if request.note_path else None
    if note_path and note_path.exists() and note_path.is_file():
        try:
            text = note_path.read_text(encoding="utf-8", errors="ignore")
            status = "answered-good" if request.is_good else "knowledge-gap-needs-review"
            text = re.sub(r"^status:\s*.+$", f"status: {status}", text, count=1, flags=re.MULTILINE)
            feedback = sanitize_outbound_text(request.feedback.strip() or ("좋아요" if request.is_good else "아쉬워요"))
            text += (
                f"\n\n## Revit Assistant 피드백 ({datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')})\n"
                f"- User: {sanitize_outbound_text(request.user_id)}\n"
                f"- Result: {'good' if request.is_good else 'needs-review'}\n\n"
                f"{feedback}\n"
            )
            note_path.write_text(text, encoding="utf-8")
            rebuild_revit_qa_moc()
            launch_background_task(refresh_obsidian_after_knowledge_update())
            return {"status": "updated", "note_path": request.note_path}
        except OSError as exc:
            return {"status": "rejected", "reason": str(exc)}
    return {"status": "ignored", "reason": "note_path not found"}

# =============================================================================
# BIM LAND 게임 엔진 API (→ backend/routers/bim_land.py)
# =============================================================================
app.include_router(bim_land_router)

@app.on_event("startup")
async def startup_event():
    print("🤖 [LUA BIM LABS 기업 체계] 통합 백엔드 가동 시작 (CEO 코어 활성화)")
    ensure_knowledge_base()
    if not TELEGRAM_BOT_TOKEN or TELEGRAM_BOT_TOKEN == "fake-bot-token":
        app.state.tg_app = None
        print("🟡 [Telegram] TELEGRAM_BOT_TOKEN 미설정: 봇 폴링 없이 대시보드 백엔드만 기동합니다.")
        return
    app.state.tg_app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
    app.state.tg_app.add_handler(CommandHandler("start", handle_team_help_command))
    app.state.tg_app.add_handler(CommandHandler("teamhelp", handle_team_help_command))
    app.state.tg_app.add_handler(CommandHandler("ask", handle_team_ask_command))
    app.state.tg_app.add_handler(CommandHandler("more", handle_team_more_command))
    app.state.tg_app.add_handler(CommandHandler("ok", handle_team_ok_command))
    app.state.tg_app.add_handler(CommandHandler("fix", handle_team_fix_command))
    app.state.tg_app.add_handler(MessageHandler(filters.Document.ALL, handle_telegram_document))
    app.state.tg_app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_telegram_message))
    try:
        await app.state.tg_app.initialize()
        await app.state.tg_app.start()
        await app.state.tg_app.updater.start_polling(drop_pending_updates=True)
        print("📡 [시스템] 텔레그램 엔터프라이즈 라우팅 폴링 채널 개방 완료.")
    except Exception as tg_err:
        app.state.tg_app = None
        print(f"🟡 [Telegram] 네트워크 오류로 봇 초기화 실패: {tg_err} — 봇 없이 대시보드 백엔드만 기동합니다.")

@app.on_event("shutdown")
async def shutdown_event():
    if not getattr(app.state, "tg_app", None):
        print("⚠️ [시스템] 백엔드 프로세스가 정상 종료되었습니다.")
        return
    await app.state.tg_app.updater.stop()
    await app.state.tg_app.stop()
    await app.state.tg_app.shutdown()
    print("⚠️ [시스템] 백엔드 프로세스가 정상 종료되었습니다.")
