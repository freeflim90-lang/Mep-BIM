from __future__ import annotations

import os
import re
import json
import asyncio
import datetime
from contextlib import asynccontextmanager
from pathlib import Path
from typing import Optional
import httpx
from fastapi import FastAPI, Header, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, Update
from telegram.ext import Application, CallbackQueryHandler, CommandHandler, MessageHandler, filters, ContextTypes
from openai import AsyncOpenAI
import backend.collaboration as collaboration
import backend.github_integration as github_integration
import backend.local_coder as local_coder
import backend.qwen_product_drafts as qwen_product_drafts
from backend.email_notifications import gmail_settings, send_gmail
from backend.core.paths import (
    CURATION_DIR,
    DATA_DIR,
    FRONTEND_DIR,
    GLOBAL_OBSIDIAN_VAULT,
    PROJECT_ROOT,
    TEAM_REQUESTS_DIR,
)
from backend.dashboard_ws import (
    ConnectionManager,
    broadcast_json,
    build_decision_log_payload,
    build_state_update_payload,
    dashboard_websocket_session,
)
from backend.models import (
    AddinTaskRequest, KnowledgeUpdateRequest,
    RevitAssistantChatRequest, RevitAssistantFeedbackRequest,
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
    append_korean_response_instruction, enforce_korean_answer,
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
from backend.reasoning_feedback import append_reasoning_feedback, is_reasoning_digest_reply
from backend.reasoning_feedback import (
    append_deepseek_final_review,
    build_deepseek_final_review_prompt,
    has_sensitive_external_review_risk,
    latest_reasoning_digest_path,
)
from backend.model_routing import agent_model_map, deepseek_final_review_model, model_routing_status
from backend.final_answer_review import review_final_answer_with_deepseek
from backend.knowledge_approval import (
    append_knowledge_approval_candidate,
    find_knowledge_approval_candidate,
    knowledge_approval_message,
    save_knowledge_approval_registry,
)
from backend.management_excel_approval import (
    approve_management_excel_request,
    build_management_excel_approval_prompt,
    find_management_excel_request,
    reject_management_excel_request,
)
from backend.telegram_team_access import telegram_chat_allowed as team_telegram_chat_allowed
from backend.revit_assistant_security import (
    extract_bearer_token,
    require_revit_assistant_api_key,
    resolve_revit_feedback_note_path as resolve_revit_feedback_note_path_in_root,
)
from backend.revit_assistant_controller import (
    RevitAssistantChatDependencies,
    RevitAssistantFeedbackDependencies,
    handle_revit_assistant_chat,
    handle_revit_assistant_feedback,
)
from backend.revit_assistant_service import (
    RevitAssistantMetrics,
    luachat_health_payload,
    update_revit_feedback_note,
    write_luachat_metrics_daily_snapshot,
)
from backend.visitor_counter import VisitorCounter
from backend.routers.bim_command_center import create_bim_command_center_router
from backend.routers.bim_land import router as bim_land_router
from backend.routers.collaboration_operations import create_collaboration_operations_router
from backend.routers.contact_intake import create_contact_intake_router
from backend.routers.dashboard_tasks import build_addin_task_prompt, create_dashboard_tasks_router
from backend.routers.development_operations import create_development_operations_router
from backend.routers.knowledge_operations import create_knowledge_operations_router
from backend.routers.operations_status import create_operations_status_router
from backend.routers.organization import router as organization_router
from backend.routers.revit_assistant import create_revit_assistant_router

revit_assistant_metrics = RevitAssistantMetrics()
LUACHAT_METRICS_DAILY_FILE = PROJECT_ROOT / "runtime" / "luachat_metrics_daily.json"


def save_luachat_metrics_snapshot() -> None:
    try:
        write_luachat_metrics_daily_snapshot(
            path=LUACHAT_METRICS_DAILY_FILE,
            metrics=revit_assistant_metrics.snapshot(),
            now=datetime.datetime.now(),
        )
    except OSError as exc:
        print(f"⚠️ [LUAChat metrics] snapshot 저장 실패: {exc}")

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

@asynccontextmanager
async def app_lifespan(app: FastAPI):
    await startup_event()
    try:
        yield
    finally:
        await shutdown_event()


# =============================================================================
# SECTION 1 ── 시스템 초기화 · FastAPI · 조직 설정
#   - FastAPI 앱 / CORS / 에이전트 상태 / 조직 구조 / AI 클라이언트
# =============================================================================
app = FastAPI(lifespan=app_lifespan)
cors_origins = [origin.strip() for origin in os.environ.get("CORS_ORIGINS", "*").split(",")]

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials="*" not in cors_origins,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.mount("/static", StaticFiles(directory=FRONTEND_DIR / "static"), name="static")
app.mount("/mqa", StaticFiles(directory=PROJECT_ROOT / "obsidian_vaults" / "model_quality_auditor" / "Assets"), name="mqa_assets")
app.mount("/knowledge", StaticFiles(directory=PROJECT_ROOT / "obsidian_vaults" / "lua_bim_lab_global_map" / "Assets"), name="knowledge_assets")

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

TEAM_REQUEST_LOG = TEAM_REQUESTS_DIR / "telegram_knowledge_requests.md"
TEAM_TELEGRAM_USERS_FILE = TEAM_REQUESTS_DIR / "team_telegram_users.json"
AUTO_KNOWLEDGE_GAP_LOG = CURATION_DIR / "auto_knowledge_gap_log.md"
TEAM_QA_OBSIDIAN_DIR = GLOBAL_OBSIDIAN_VAULT / "NAS_Knowledge" / "Team_Telegram_QA"
TEAM_QA_MOC = TEAM_QA_OBSIDIAN_DIR / "MOC - Team Telegram QA.md"
REVIT_QA_OBSIDIAN_DIR = GLOBAL_OBSIDIAN_VAULT / "NAS_Knowledge" / "Revit_Assistant_QA"
REVIT_QA_MOC = REVIT_QA_OBSIDIAN_DIR / "MOC - Revit Assistant QA.md"
RESUME_INTAKE_DIR = DATA_DIR / "resume_intake" / "telegram"
TELEGRAM_KNOWLEDGE_SESSIONS: dict[str, dict] = {}


def resolve_revit_feedback_note_path(note_path: str) -> Path | None:
    """Resolve feedback note paths to the Revit QA vault only."""
    return resolve_revit_feedback_note_path_in_root(
        note_path,
        project_root=PROJECT_ROOT,
        allowed_root=REVIT_QA_OBSIDIAN_DIR,
    )

TEAM_REQUEST_KEYBOARD = ReplyKeyboardMarkup(
    [["📚 지식질문", "🔎 더 찾아줘", "🧩 개발"], ["🧠 추론첨언"]],
    resize_keyboard=True,
    one_time_keyboard=False,
    input_field_placeholder="질문을 그냥 입력하거나 버튼을 눌러주세요.",
)

def telegram_chat_allowed(update: Update) -> bool:
    return team_telegram_chat_allowed(
        update=update,
        env_raw=os.environ.get("TELEGRAM_TEAM_CHAT_IDS") or TELEGRAM_CHAT_ID or "",
        registry_path=TEAM_TELEGRAM_USERS_FILE,
    )

async def submit_knowledge_approval_candidate(
    update: KnowledgeUpdateRequest,
    result: dict,
    assessment: Optional[dict] = None,
) -> dict | None:
    item = append_knowledge_approval_candidate(
        update=update,
        result=result,
        assessment=assessment,
        project_root=PROJECT_ROOT,
    )
    if not item:
        return None

    telegram_chat_id = os.environ.get("TELEGRAM_CHAT_ID")
    if telegram_chat_id and getattr(app.state, "tg_app", None):
        try:
            await app.state.tg_app.bot.send_message(
                chat_id=telegram_chat_id,
                text=knowledge_approval_message(item),
                reply_markup=TEAM_REQUEST_KEYBOARD,
            )
        except Exception as exc:
            print(f"⚠️ [Knowledge approval notify] {exc}")
    else:
        print(f"⚠️ [Knowledge approval] Telegram 미설정 또는 봇 없음: {item.get('id', 'unknown')}")
    return item

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


async def deepseek_reasoning_final_review(*, feedback_path: Path, feedback: str, conclusion: str) -> str:
    enabled = os.environ.get("DEEPSEEK_FINAL_REVIEW_ENABLED", "true").lower() in {"1", "true", "yes", "on"}
    model = deepseek_final_review_model(f"{feedback}\n\n{conclusion}")
    if not enabled:
        return append_deepseek_final_review(feedback_path, "", model=model, skipped_reason="DEEPSEEK_FINAL_REVIEW_ENABLED 비활성화")
    if not PAID_AI_ENABLED:
        return append_deepseek_final_review(feedback_path, "", model=model, skipped_reason="PAID_AI_ENABLED 비활성화")
    if not DEEPSEEK_API_KEY or DEEPSEEK_API_KEY == "sk-fake-key-for-test":
        return append_deepseek_final_review(feedback_path, "", model=model, skipped_reason="DEEPSEEK_API_KEY 미설정")
    if not can_use_deepseek_budget():
        return append_deepseek_final_review(feedback_path, "", model=model, skipped_reason="월 DeepSeek 예산 잔액 부족")
    external_payload = f"{feedback}\n\n{conclusion}"
    if has_sensitive_external_review_risk(external_payload):
        return append_deepseek_final_review(feedback_path, "", model=model, skipped_reason="민감정보 또는 내부 경로 위험 신호 감지")

    digest_path = latest_reasoning_digest_path()
    digest_text = digest_path.read_text(encoding="utf-8", errors="ignore") if digest_path else ""
    prompt = build_deepseek_final_review_prompt(feedback=feedback, conclusion=conclusion, digest_text=digest_text)
    response = await deepseek_client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "system",
                "content": (
                    "당신은 LUA BIM LABS의 최종 추론 검토관입니다. "
                    "로컬 추론과 대표 실무 첨언을 검토하되, 민감정보를 추정하지 않고 "
                    "논리 허점, 사업화 리스크, 다음 질문, 최종 사고 원칙만 한국어로 정리합니다."
                ),
            },
            {"role": "user", "content": prompt},
        ],
        max_tokens=1600,
    )
    content = response.choices[0].message.content or ""
    review = sanitize_outbound_text(content.strip())[:3500]
    if review:
        record_deepseek_budget_use(workflow_id="reasoning_training_final_review", target_agent="전략기획")
    return append_deepseek_final_review(feedback_path, review, model=model)


async def reply_reasoning_feedback_result(update: Update, feedback_path: Path, conclusion: str, final_review: str) -> None:
    header = (
        "🧠 [추론 첨언 저장 완료]\n\n"
        "대표님의 생각을 추론 훈련 루프에 저장했습니다.\n"
        f"기록: {feedback_path.relative_to(PROJECT_ROOT).as_posix()}"
    )
    body = f"{conclusion}\n\n{final_review}".strip()
    full = f"{header}\n\n{body}"
    if len(full) <= 3500:
        await update.message.reply_text(full, reply_markup=TEAM_REQUEST_KEYBOARD)
        return
    await update.message.reply_text(header, reply_markup=TEAM_REQUEST_KEYBOARD)
    await send_reply_chunks(update.message, body, max_chars=3200)

# normalize_query_text, normalize_team_button_text → backend/text_utils.py 임포트

# =============================================================================
# SECTION 4 ── 지식 베이스 검색 · 점수화 · 답변 생성 (→ backend/knowledge_engine.py)
# =============================================================================
from backend.knowledge_engine import (
    knowledge_search_files, query_terms, score_knowledge_text,
    extract_relevant_excerpt, search_local_knowledge,
    infer_knowledge_agent_from_query, build_knowledge_answer, build_combined_answer,
    assess_knowledge_answer_quality, assess_team_telegram_answer_readiness,
    auto_supplement_knowledge_gap,
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
    is_owner_telegram_chat,
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
    can_use_deepseek_budget, deepseek_budget_remaining, record_deepseek_budget_use,
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
    await broadcast_json(
        manager,
        build_state_update_payload(agent_states=agent_states, current_active_agent=current_active_agent),
    )


async def log_to_dashboard(tag: str, message: str):
    """수신반에 실시간 로그 항목을 추가합니다."""
    await broadcast_json(manager, build_decision_log_payload(tag=tag, message=message))


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
        "🧩 개발: 개발/자동화/툴 제작 요청을 조직 라우터로 넘깁니다.\n"
        "🧠 추론첨언: 직전 추론 훈련 다이제스트에 대표 실무 의견을 붙입니다.\n\n"
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
            append_korean_response_instruction(
                "당신은 LUA BIM LABS의 MEP BIM 전문 어시스턴트입니다. "
                "제공된 지식 베이스를 참고해 질문에 실무적이고 자연스러운 한국어로 답변합니다. "
                "불필요한 헤더, 태그, 위키 링크 없이 핵심 내용만 전달합니다."
            )
        ),
        timeout=30,
    )
    if result.get("ok") and result.get("response"):
        return enforce_korean_answer(result["response"].strip(), fallback_subject=query)
    return ""


async def process_team_knowledge_question(update: Update, query: str):
    agent = infer_knowledge_agent_from_query(query)
    await log_to_dashboard("T4_TELEGRAM", f"📥 질문 수신: {query[:80]}")
    ensure_agent_state("지식업데이트")
    agent_states["지식업데이트"]["status"] = "Active"
    agent_states["지식업데이트"]["message"] = f"팀원 Telegram 질문 검색 중: {query[:80]}"
    await send_state_to_dashboard()

    progress_msg = await update.message.reply_text("🔍 검색 중...", reply_markup=TEAM_REQUEST_KEYBOARD)

    # 로컬 지식 먼저 조회하고, 점수뿐 아니라 답변 노이즈/에이전트 불일치까지 평가한다.
    local_matches = search_local_knowledge(query)
    top_score = local_matches[0]["score"] if local_matches else 0
    local_answer_preview = build_knowledge_answer(query, local_matches)
    readiness = assess_team_telegram_answer_readiness(
        query,
        agent,
        local_matches,
        local_answer_preview,
    )

    # 로컬 지식이 충분하면 웹 검색 생략. 부족하면 자동 보강 검색으로 전환.
    if not readiness["should_search"]:
        search_result = ""
        await log_to_dashboard("T4_TELEGRAM", f"📚 로컬 지식으로 답변 (score={top_score}): {query[:50]}")
    else:
        await log_to_dashboard(
            "T4_TELEGRAM",
            f"🔎 로컬 답변 품질 보강 필요 ({', '.join(readiness['reasons'])}): {query[:50]}",
        )
        web_task = asyncio.create_task(_search_web_for_knowledge(agent, query))
        search_result = await web_task

    # 웹 결과 + 로컬 지식을 컨텍스트로 조합
    raw_context = build_combined_answer(query, search_result, local_matches)

    # Qwen 로컬 모델로 자연어 합성 (가능한 경우)
    answer = await _synthesize_with_qwen(query, raw_context) or raw_context
    answer = enforce_korean_answer(answer, fallback_subject=query)

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
    deepseek_review = await review_final_answer_with_deepseek(
        query=query,
        answer=answer,
        agent=agent,
        source_tag=source_tag,
        client=deepseek_client,
        api_key=DEEPSEEK_API_KEY,
        workflow_id="team_telegram_final_answer_review",
    )
    answer = deepseek_review["answer"]
    answer = f"[{source_tag}]\n\n{answer}"
    final_assessment = assess_knowledge_answer_quality(query, agent, local_matches, answer)

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
            assessment=readiness,
            search_result=search_result,
        )
    elif not final_assessment["ok"]:
        append_auto_knowledge_gap_log(
            query=query,
            agent=agent,
            assessment=final_assessment,
            search_result="로컬 답변 품질 기준 미달. 외부 검색은 실행되지 않았으며 수동 지식 보강 필요.",
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
        "quality": {**final_assessment, "deepseek_review": deepseek_review},
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
        collected_update = KnowledgeUpdateRequest(
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
        )
        collected_result = append_knowledge_update(collected_update)
        await submit_knowledge_approval_candidate(
            collected_update,
            collected_result,
            {
                "ok": True,
                "reasons": ["자동 수집 완료", "QA 후보 저장", "최고 지배자 승인 대기"],
                "top_score": "-",
            },
        )
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

async def handle_knowledge_approve_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_owner_telegram_chat(update):
        await update.message.reply_text("지식 승인 권한이 없습니다.")
        return
    if not context.args:
        await update.message.reply_text("형식: /kapprove 후보ID")
        return

    candidate_id = context.args[0].strip()
    registry, item = find_knowledge_approval_candidate(candidate_id)
    if not item:
        await update.message.reply_text(f"후보 ID를 찾지 못했습니다: {candidate_id}")
        return
    if item.get("status") not in {"pending_owner_approval", "rejected"}:
        await update.message.reply_text(f"이미 처리된 후보입니다. 현재 상태: {item.get('status')}")
        return

    approved_tags = ",".join(
        tag for tag in [item.get("tags", ""), "owner-approved", "manual-knowledge"]
        if tag
    )
    result = append_knowledge_update(KnowledgeUpdateRequest(
        agent=item["agent"],
        title=f"승인 지식: {item['title']}",
        source=f"owner-approved:{item.get('source', 'unknown')}",
        tags=approved_tags,
        content=(
            f"승인 후보 ID: {item['id']}\n"
            f"최고 지배자 승인일: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
            f"{item.get('content', '').strip()}"
        ),
    ))

    item["status"] = "approved_promoted"
    item["approved_at"] = datetime.datetime.now().isoformat(timespec="seconds")
    item["approved_by"] = telegram_user_label(update)
    item["promoted_path"] = str(Path(result["path"]).relative_to(PROJECT_ROOT))
    item["promote_skipped"] = bool(result.get("skipped"))
    save_knowledge_approval_registry(registry)
    await refresh_obsidian_after_knowledge_update()

    await update.message.reply_text(
        "✅ [지식 후보 승인 완료]\n\n"
        f"후보 ID: {item['id']}\n"
        f"담당 지식: {item['agent']}\n"
        f"반영 위치: {item['promoted_path']}\n"
        f"중복 여부: {'중복으로 본문 추가 생략' if item['promote_skipped'] else '신규 반영'}",
        reply_markup=TEAM_REQUEST_KEYBOARD,
    )

async def handle_knowledge_reject_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_owner_telegram_chat(update):
        await update.message.reply_text("지식 반려 권한이 없습니다.")
        return
    if not context.args:
        await update.message.reply_text("형식: /kreject 후보ID 사유")
        return

    candidate_id = context.args[0].strip()
    reason = " ".join(context.args[1:]).strip() or "사유 미기재"
    registry, item = find_knowledge_approval_candidate(candidate_id)
    if not item:
        await update.message.reply_text(f"후보 ID를 찾지 못했습니다: {candidate_id}")
        return

    item["status"] = "rejected_by_owner"
    item["rejected_at"] = datetime.datetime.now().isoformat(timespec="seconds")
    item["rejected_by"] = telegram_user_label(update)
    item["rejection_reason"] = sanitize_outbound_text(reason)
    save_knowledge_approval_registry(registry)
    await refresh_obsidian_after_knowledge_update()

    await update.message.reply_text(
        "⛔ [지식 후보 반려]\n\n"
        f"후보 ID: {item['id']}\n"
        f"담당 지식: {item['agent']}\n"
        f"사유: {item['rejection_reason']}",
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

    approve_management_excel_request(item, approved_by=telegram_user_label(update))
    save_management_excel_requests(registry)

    reply_msg = await update.message.reply_text(
        "✅ [관리팀 Excel 자동화 승인]\n\n"
        f"요청 ID: {item['id']}\n"
        "자동화 파이프라인을 실행합니다.",
        reply_markup=TEAM_REQUEST_KEYBOARD,
    )
    launch_background_task(process_corporate_pipeline(
        build_management_excel_approval_prompt(item),
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

    reject_management_excel_request(
        item,
        rejected_by=telegram_user_label(update),
        reason=reason,
        sanitizer=sanitize_outbound_text,
    )
    save_management_excel_requests(registry)
    await update.message.reply_text(
        "⛔ [관리팀 Excel 자동화 반려]\n\n"
        f"요청 ID: {item['id']}\n"
        f"사유: {item['rejection_reason']}",
        reply_markup=TEAM_REQUEST_KEYBOARD,
    )

async def _redeliberate_and_notify(item: dict) -> None:
    import backend.csuite as csuite
    revised = await csuite.redeliberate_after_rejection(item)
    await csuite.notify_owner_revised_direction(revised)


def _csuite_reject_reason_keyboard(decision_id: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("💰 예산 초과", callback_data=f"csuite_reject:{decision_id}:예산 초과"),
            InlineKeyboardButton("🎯 방향 불일치", callback_data=f"csuite_reject:{decision_id}:회사 방향과 불일치"),
        ],
        [
            InlineKeyboardButton("⏰ 시기상조", callback_data=f"csuite_reject:{decision_id}:현재 시기상조"),
            InlineKeyboardButton("✍️ 직접 입력", callback_data=f"csuite_reject_start:{decision_id}"),
        ],
    ])


async def _process_csuite_rejection(query_or_update, decision_id: str, reason: str, original_text: str = ""):
    """반려 처리 + DeepSeek 재심의 + 소유주에게 수정 방향 보고."""
    import backend.csuite as csuite
    msg, item = csuite.owner_reject(decision_id, reason)
    if query_or_update and original_text:
        await query_or_update.edit_message_text(f"{original_text}\n\n{msg}")
    if item:
        revised = await csuite.redeliberate_after_rejection(item)
        await csuite.notify_owner_revised_direction(revised)


async def handle_csuite_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """C-suite 비용 결정 인라인 버튼 콜백 처리."""
    query = update.callback_query
    await query.answer()

    chat_id = str(query.message.chat.id)
    owner_chat_id = os.environ.get("TELEGRAM_CHAT_ID", "")
    if chat_id != owner_chat_id:
        await query.answer("승인 권한이 없습니다.", show_alert=True)
        return

    import backend.csuite as csuite
    data = query.data or ""

    if data.startswith("csuite_approve:"):
        decision_id = data.split(":", 1)[1]
        result = csuite.owner_approve(decision_id)
        await query.edit_message_text(f"{query.message.text}\n\n{result}")

    elif data.startswith("csuite_reject_start:"):
        # 직접 입력 선택 — 세션에 대기 상태 등록
        decision_id = data.split(":", 1)[1]
        TELEGRAM_KNOWLEDGE_SESSIONS[chat_id] = {
            **TELEGRAM_KNOWLEDGE_SESSIONS.get(chat_id, {}),
            "pending_mode": "csuite_reject",
            "pending_csuite_decision_id": decision_id,
        }
        await query.message.reply_text(
            f"🚫 [{decision_id}] 반려 사유를 직접 입력해주세요.",
            reply_markup=TEAM_REQUEST_KEYBOARD,
        )

    elif data.startswith("csuite_reject:"):
        # 프리셋 사유 버튼 선택
        parts = data.split(":", 2)
        decision_id = parts[1]
        reason = parts[2] if len(parts) > 2 else "사유 미기재"
        launch_background_task(
            _process_csuite_rejection(query, decision_id, reason, query.message.text)
        )

    elif data.startswith("csuite_reason_select:"):
        # 반려 사유 선택 단계 — 프리셋 버튼 표시
        decision_id = data.split(":", 1)[1]
        await query.edit_message_reply_markup(
            reply_markup=_csuite_reject_reason_keyboard(decision_id)
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

    if is_reasoning_digest_reply(update):
        feedback_path, conclusion = append_reasoning_feedback(update, text)
        final_review = await deepseek_reasoning_final_review(feedback_path=feedback_path, feedback=text, conclusion=conclusion)
        await reply_reasoning_feedback_result(update, feedback_path, conclusion, final_review)
        await refresh_obsidian_after_knowledge_update()
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
    if text == "🧠 추론첨언":
        session["pending_mode"] = "reasoning_feedback"
        await update.message.reply_text(
            "🧠 추론 첨언 내용을 보내주세요.\n\n"
            "방금/최근 추론 훈련 다이제스트에 연결해서 실무 예외, 고객 설명 언어, 체크리스트/자동화 후보로 저장하겠습니다.",
            reply_markup=TEAM_REQUEST_KEYBOARD,
        )
        return True

    pending_mode = session.get("pending_mode")
    if pending_mode == "csuite_reject":
        import backend.csuite as csuite
        session["pending_mode"] = None
        decision_id = session.pop("pending_csuite_decision_id", "")
        msg, item = csuite.owner_reject(decision_id, text)
        await update.message.reply_text(msg, reply_markup=TEAM_REQUEST_KEYBOARD)
        if item:
            launch_background_task(
                _redeliberate_and_notify(item)
            )
        return True
    if pending_mode == "development":
        session["pending_mode"] = None
        await process_team_development_request(update, text)
        return True
    if pending_mode == "ask":
        session["pending_mode"] = None
        await process_team_knowledge_question(update, text)
        return True
    if pending_mode == "reasoning_feedback":
        session["pending_mode"] = None
        feedback_path, conclusion = append_reasoning_feedback(update, text)
        final_review = await deepseek_reasoning_final_review(feedback_path=feedback_path, feedback=text, conclusion=conclusion)
        await reply_reasoning_feedback_result(update, feedback_path, conclusion, final_review)
        await refresh_obsidian_after_knowledge_update()
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

    # 소유주 채팅 → C-suite 심의 레이어 먼저 실행
    if is_owner_telegram_chat(update):
        import backend.csuite as csuite
        reply_msg = await update.message.reply_text(
            "🏛️ [C-suite 심의 중] CEO · COO · CFO 검토를 시작합니다...",
            reply_markup=TEAM_REQUEST_KEYBOARD,
        )
        decision = await csuite.csuite_deliberate_with_deepseek(user_text)
        synthesis = decision.get("deepseek_synthesis", "결정문 생성 실패")

        if decision["requires_owner_approval"]:
            await reply_msg.edit_text(
                f"💰 [C-suite 심의 완료 — 비용 수반]\n\n{synthesis[:600]}\n\n"
                "승인 요청을 아래 메시지로 발송합니다."
            )
            await csuite.notify_owner_cost_approval(decision)
            return

        # 비용 없음 → C-suite 자율 결정 보고 후 파이프라인 실행
        await reply_msg.edit_text(
            f"✅ [C-suite 자율 결정]\n\n{synthesis[:800]}\n\n실행 파이프라인을 시작합니다."
        )
        await log_to_dashboard("T4_TELEGRAM", f"📥 C-suite 승인 후 파이프라인: {user_text[:80]}")
        exec_msg = await update.message.reply_text(
            "🏢 [LUA BIM LABS 기업 라우터] 파이프라인 실행 중...",
            reply_markup=TEAM_REQUEST_KEYBOARD,
        )
        launch_background_task(process_corporate_pipeline(user_text, exec_msg))
        return

    # 팀원 채팅 → 기존 파이프라인 직접 실행
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
    await process_corporate_pipeline(build_addin_task_prompt(task), DashboardReply())

# 7. FastAPI 엔드포인트 및 웹소켓 터널
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
    await dashboard_websocket_session(websocket=websocket, manager=manager, send_state=send_state_to_dashboard)

@app.websocket("/ws/state")
async def websocket_state_compat_endpoint(websocket: WebSocket):
    await dashboard_websocket_session(websocket=websocket, manager=manager, send_state=send_state_to_dashboard)

async def revit_assistant_chat(
    request: RevitAssistantChatRequest,
    x_lua_bim_api_key: Optional[str] = Header(default=None, alias="X-LUA-BIM-API-Key"),
    authorization: Optional[str] = Header(default=None, alias="Authorization"),
):
    return await handle_revit_assistant_chat(
        request=request,
        api_key=x_lua_bim_api_key,
        authorization=authorization,
        deps=RevitAssistantChatDependencies(
            extract_bearer_token=extract_bearer_token,
            require_api_key=require_revit_assistant_api_key,
            build_context_prompt=build_revit_context_prompt,
            infer_agent=infer_knowledge_agent_from_query,
            search_local_knowledge=search_local_knowledge,
            prioritize_matches=prioritize_agent_matches,
            knowledge_agents=KNOWLEDGE_AGENTS,
            build_local_answer=build_revit_assistant_answer,
            search_web=_search_web_for_knowledge,
            build_context=build_combined_answer,
            synthesize=_synthesize_with_qwen,
            enforce_answer=lambda text, fallback: enforce_korean_answer(text, fallback_subject=fallback),
            sanitizer=sanitize_outbound_text,
            append_knowledge_update=append_knowledge_update,
            knowledge_update_factory=KnowledgeUpdateRequest,
            append_gap_log=append_auto_knowledge_gap_log,
            metrics=revit_assistant_metrics,
            save_metrics_snapshot=save_luachat_metrics_snapshot,
            project_root=PROJECT_ROOT,
            agent_states=agent_states,
            ensure_agent_state=ensure_agent_state,
            save_note=save_revit_qa_to_obsidian,
            send_state=send_state_to_dashboard,
            refresh_knowledge=refresh_obsidian_after_knowledge_update,
            launch_background_task=launch_background_task,
            fallback_note_dir=PROJECT_ROOT / "runtime" / "revit_assistant_qa_fallback",
            final_answer_review=lambda **kwargs: review_final_answer_with_deepseek(
                **kwargs,
                client=deepseek_client,
                api_key=DEEPSEEK_API_KEY,
                workflow_id="luachat_final_answer_review",
            ),
        ),
    )

_visitor_counter = VisitorCounter(DATA_DIR / "visitor_count.json")


async def revit_assistant_feedback(
    request: RevitAssistantFeedbackRequest,
    x_lua_bim_api_key: Optional[str] = Header(default=None, alias="X-LUA-BIM-API-Key"),
    authorization: Optional[str] = Header(default=None, alias="Authorization"),
):
    return await handle_revit_assistant_feedback(
        request=request,
        api_key=x_lua_bim_api_key,
        authorization=authorization,
        deps=RevitAssistantFeedbackDependencies(
            extract_bearer_token=extract_bearer_token,
            require_api_key=require_revit_assistant_api_key,
            resolve_note_path=resolve_revit_feedback_note_path,
            update_note=update_revit_feedback_note,
            sanitizer=sanitize_outbound_text,
            rebuild_revit_qa_moc=rebuild_revit_qa_moc,
            refresh_knowledge=refresh_obsidian_after_knowledge_update,
            launch_background_task=launch_background_task,
            metrics=revit_assistant_metrics,
            save_metrics_snapshot=save_luachat_metrics_snapshot,
            now=datetime.datetime.now,
        ),
    )

async def luachat_health():
    return luachat_health_payload(
        obsidian_vault=GLOBAL_OBSIDIAN_VAULT,
        project_root=PROJECT_ROOT,
        token_required=bool(os.environ.get("LUA_CHAT_TOKEN") or os.environ.get("REVIT_ASSISTANT_API_KEYS")),
        search_providers={
            "tavily": bool(os.environ.get("TAVILY_API_KEY")),
            "google_cse": bool(os.environ.get("GOOGLE_API_KEY") and os.environ.get("GOOGLE_CSE_ID")),
            "naver": bool(os.environ.get("NAVER_CLIENT_ID") and os.environ.get("NAVER_CLIENT_SECRET")),
            "duckduckgo": True,
        },
        metrics=revit_assistant_metrics.snapshot(),
        metrics_snapshot_path=LUACHAT_METRICS_DAILY_FILE.relative_to(PROJECT_ROOT).as_posix(),
    )


app.include_router(create_revit_assistant_router(
    chat_handler=revit_assistant_chat,
    feedback_handler=revit_assistant_feedback,
    health_handler=luachat_health,
))
app.include_router(create_bim_command_center_router(project_root=PROJECT_ROOT))
app.include_router(create_development_operations_router(
    github_integration=github_integration,
    local_coder=local_coder,
    qwen_product_drafts=qwen_product_drafts,
    collaboration=collaboration,
    active_collaboration_workflows=active_collaboration_workflows,
    agent_states=agent_states,
    ensure_agent_state=ensure_agent_state,
    send_state_to_dashboard=send_state_to_dashboard,
))
app.include_router(create_contact_intake_router(
    project_root=PROJECT_ROOT,
    telegram_bot_token=TELEGRAM_BOT_TOKEN,
    telegram_chat_id=TELEGRAM_CHAT_ID,
    gmail_settings=gmail_settings,
    send_gmail=send_gmail,
))
app.include_router(create_knowledge_operations_router(
    project_root=PROJECT_ROOT,
    ensure_knowledge_base=ensure_knowledge_base,
    knowledge_agents=KNOWLEDGE_AGENTS,
    knowledge_dir=KNOWLEDGE_DIR,
    append_knowledge_update=append_knowledge_update,
    submit_knowledge_approval_candidate=submit_knowledge_approval_candidate,
    ensure_agent_state=ensure_agent_state,
    agent_states=agent_states,
    send_state_to_dashboard=send_state_to_dashboard,
    get_persistent_gaps=get_persistent_gaps,
))
app.include_router(create_collaboration_operations_router(
    collaboration=collaboration,
    active_collaboration_workflows=active_collaboration_workflows,
    preview_collaboration_route=preview_collaboration_route,
    ensure_agent_state=ensure_agent_state,
    agent_states=agent_states,
))
app.include_router(create_dashboard_tasks_router(
    run_addin_task=run_dashboard_addin_task,
    launch_background_task=launch_background_task,
))
app.include_router(create_operations_status_router(
    frontend_dir=FRONTEND_DIR,
    agents=ALL_AGENTS,
    telegram_enabled=lambda: bool(os.environ.get("TELEGRAM_BOT_TOKEN")),
    telegram_chat_configured=lambda: bool(TELEGRAM_CHAT_ID),
    github_configured=github_integration.is_configured,
    local_coder_enabled=local_coder.enabled,
    visitor_counter=lambda: _visitor_counter,
    model_routing_status=model_routing_status,
    agent_model_map=agent_model_map,
    paid_ai_enabled=lambda: PAID_AI_ENABLED,
    deepseek_api_configured=lambda: bool(DEEPSEEK_API_KEY and DEEPSEEK_API_KEY != "sk-fake-key-for-test"),
    deepseek_budget_remaining=deepseek_budget_remaining,
))

# =============================================================================
# BIM LAND 게임 엔진 API (→ backend/routers/bim_land.py)
# =============================================================================
app.include_router(bim_land_router)
app.include_router(organization_router)

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
    app.state.tg_app.add_handler(CommandHandler("kapprove", handle_knowledge_approve_command))
    app.state.tg_app.add_handler(CommandHandler("kreject", handle_knowledge_reject_command))
    app.state.tg_app.add_handler(CommandHandler("approve", handle_approve_command))
    app.state.tg_app.add_handler(CommandHandler("reject", handle_reject_command))
    app.state.tg_app.add_handler(CallbackQueryHandler(handle_csuite_callback, pattern=r"^csuite_"))
    app.state.tg_app.add_handler(MessageHandler(filters.Document.ALL, handle_telegram_document))
    app.state.tg_app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_telegram_message))
    try:
        await app.state.tg_app.initialize()
        # 이전 폴링/웹훅 세션 충돌 방지: 시작 전 webhook 제거
        await app.state.tg_app.bot.delete_webhook(drop_pending_updates=True)
        await app.state.tg_app.start()
        await app.state.tg_app.updater.start_polling(drop_pending_updates=True)
        print("📡 [시스템] 텔레그램 엔터프라이즈 라우팅 폴링 채널 개방 완료.")
    except Exception as tg_err:
        app.state.tg_app = None
        print(f"🟡 [Telegram] 네트워크 오류로 봇 초기화 실패: {tg_err} — 봇 없이 대시보드 백엔드만 기동합니다.")

async def shutdown_event():
    if not getattr(app.state, "tg_app", None):
        print("⚠️ [시스템] 백엔드 프로세스가 정상 종료되었습니다.")
        return
    await app.state.tg_app.updater.stop()
    await app.state.tg_app.stop()
    await app.state.tg_app.shutdown()
    print("⚠️ [시스템] 백엔드 프로세스가 정상 종료되었습니다.")
