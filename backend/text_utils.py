"""
텍스트 처리 · PDF 추출 · Telegram 메시지 빌더 유틸리티
  - 외부 상태(agent_states, deepseek_client 등) 에 의존하지 않는 순수 함수 모음.
  - deepseek_resume_report 처럼 서버 전역 클라이언트가 필요한 함수는 server_total.py 에 유지.
"""
from __future__ import annotations

import asyncio
import os
import re
import shutil
import subprocess
from pathlib import Path

from telegram import Update


# ── 텍스트 새니타이저 ──────────────────────────────────────────────────────────────

KOREAN_RESPONSE_INSTRUCTION = (
    "응답 언어 정책: 최종 답변은 항상 자연스러운 한국어 존댓말로 작성하세요. "
    "사용자가 다른 언어를 명시적으로 요청하지 않는 한 중국어, 일본어, 영어 문장으로 답하지 마세요. "
    "전문 용어, API 이름, 코드 식별자, URL은 원문을 유지해도 됩니다."
)


def append_korean_response_instruction(system: str = "") -> str:
    system = (system or "").strip()
    if KOREAN_RESPONSE_INSTRUCTION in system:
        return system
    return f"{system}\n\n{KOREAN_RESPONSE_INSTRUCTION}".strip()


def contains_likely_chinese_text(text: str) -> bool:
    """중국어식 CJK 문장이 섞였는지 보수적으로 감지한다."""
    if not text:
        return False
    cjk_count = sum(1 for char in text if "\u4e00" <= char <= "\u9fff")
    if cjk_count < 8:
        return False
    hangul_count = sum(1 for char in text if "\uac00" <= char <= "\ud7a3")
    letter_count = sum(1 for char in text if char.isalpha())
    if letter_count == 0:
        return False
    return cjk_count / letter_count > 0.12 and cjk_count > hangul_count * 0.4


def enforce_korean_answer(text: str, *, fallback_subject: str = "요청") -> str:
    sanitized = sanitize_outbound_text(text)
    if not contains_likely_chinese_text(sanitized):
        return sanitized
    return (
        "한국어가 아닌 문장이 감지되어 답변을 다시 정리해야 합니다.\n\n"
        f"{fallback_subject}에 대해서는 한국어 답변만 제공하도록 설정했습니다. "
        "같은 질문을 다시 보내주시면 한국어 기준으로 재생성하겠습니다."
    )


def sanitize_outbound_text(text: str) -> str:
    sanitized = text or ""
    sanitized = sanitized.replace("knowledge-gap-needs-review", "지식 보강 후보")
    sanitized = sanitized.replace("needs-review", "검토 필요")
    sanitized = re.sub(r"[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}", "[EMAIL_MASKED]", sanitized)
    sanitized = re.sub(r"\b\d{6}-\d{7}\b", "[RRN_MASKED]", sanitized)
    sanitized = re.sub(r"\b01[016789]-?\d{3,4}-?\d{4}\b", "[PHONE_MASKED]", sanitized)
    sanitized = re.sub(r"\b\d{9,}\b", "[LONG_ID_MASKED]", sanitized)
    return sanitized


def sanitize_resume_text_for_ai(text: str) -> str:
    sanitized = sanitize_outbound_text(text)
    sanitized = re.sub(r"\b(19|20)\d{2}[./-]?\d{0,2}[./-]?\d{0,2}\b", "[DATE_MASKED]", sanitized)
    sanitized = re.sub(r"(성명|이름|Name)\s*[:：]?\s*[가-힣A-Za-z]{2,20}", r"\1: [NAME_MASKED]", sanitized)
    sanitized = re.sub(r"(주소|Address)\s*[:：]?\s*[^\n]{3,80}", r"\1: [ADDRESS_MASKED]", sanitized)
    return sanitized[:12000]


def normalize_query_text(raw: str, command: str) -> str:
    text = raw.strip()
    if text.startswith(command):
        return text[len(command):].strip()
    return text


def normalize_team_button_text(text: str) -> str:
    return re.sub(r"\s+", " ", (text or "").strip())


# ── 비동기 백그라운드 태스크 헬퍼 ───────────────────────────────────────────────────

def launch_background_task(coro):
    task = asyncio.create_task(coro)
    task.add_done_callback(log_background_task_result)
    return task


def log_background_task_result(task):
    try:
        task.result()
    except asyncio.CancelledError:
        pass
    except Exception as exc:
        print(f"⚠️ [백그라운드 작업 오류] {exc}")


# ── Telegram 메시지 빌더 ────────────────────────────────────────────────────────────

def build_telegram_summary_report(
    *,
    target_agent: str,
    workflow: dict,
    collaboration_participants: list[str],
    local_coder_gate: dict,
    final_solution: str,
    collaboration_reports: list[str],
) -> str:
    qwen_report = next((r for r in collaboration_reports if r.startswith("[Qwen_Coder_8B]")), "")
    draft_preview_source = qwen_report or final_solution
    draft_preview = " ".join(draft_preview_source.split())[:900]
    participants = " → ".join(collaboration_participants[:8])
    return (
        "📝 [LUA BIM LABS 코드작성 프로세스 테스트 결과]\n\n"
        f"■ 협업 케이스: {workflow['name']}\n"
        f"■ 주관 부서: {target_agent}\n"
        f"■ 참여 흐름: {participants}\n"
        f"■ 로컬 코더: {local_coder_gate['qwen_role']} / {local_coder_gate['local_model']}\n"
        f"■ 최고지배자 실기 검증: {'필요' if local_coder_gate['requires_supreme_validation'] else '불필요'}\n"
        "■ 유료 API: 사용 안 함\n\n"
        "■ 처리 단계\n"
        "1. Plan 확인\n"
        "2. Draft 초안 작성\n"
        "3. Verification 검증 관점 확인\n"
        "4. API 필요성 판단\n\n"
        f"■ 초안 요약\n{draft_preview}\n\n"
        "상세 협업 로그와 전체 보고서는 대시보드 수신반에 동기화되었습니다."
    )


def build_telegram_progress_report(
    *,
    step: str,
    workflow_name: str,
    target_agent: str,
    detail: str,
    participants: list[str],
) -> str:
    participant_preview = " → ".join(participants[:7])
    return (
        "🏢 [LUA BIM LABS 기업 라우터]\n\n"
        f"■ 진행 단계: {step}\n"
        f"■ 협업 케이스: {workflow_name}\n"
        f"■ 주관 부서: {target_agent}\n"
        f"■ 현재 상태: {detail}\n"
        f"■ 참여 흐름: {participant_preview}\n\n"
        "처리 중입니다. 완료되면 이 메시지가 최종 요약 보고로 갱신됩니다."
    )


async def update_reply_progress(reply_msg, text: str) -> None:
    sanitized = sanitize_outbound_text(text)
    try:
        await reply_msg.edit_text(sanitized)
    except Exception as exc:
        print(f"⚠️ [Telegram] edit_text 실패 ({exc}), reply_text 폴백 전송 시도")
        try:
            await reply_msg.reply_text(sanitized)
        except Exception as exc2:
            print(f"⚠️ [Telegram] reply_text 폴백도 실패: {exc2}")


async def send_reply_chunks(reply_msg, text: str, max_chars: int = 3300) -> None:
    if not hasattr(reply_msg, "reply_text"):
        return
    chunks = [text[i:i + max_chars] for i in range(0, len(text), max_chars)]
    for idx, chunk in enumerate(chunks[:4], start=1):
        try:
            await reply_msg.reply_text(
                sanitize_outbound_text(f"📎 [최종 결과물 {idx}/{min(len(chunks), 4)}]\n\n{chunk}")
            )
        except Exception as exc:
            print(f"⚠️ [Telegram] 결과물 추가 전송 실패: {exc}")
            return


# ── Telegram Update 헬퍼 ────────────────────────────────────────────────────────────

def telegram_session_key(update: Update) -> str:
    chat_id = update.effective_chat.id if update.effective_chat else "unknown_chat"
    user_id = update.effective_user.id if update.effective_user else "unknown_user"
    return f"{chat_id}:{user_id}"


def telegram_user_label(update: Update) -> str:
    user = update.effective_user
    if not user:
        return "unknown"
    username = f"@{user.username}" if user.username else user.full_name
    return f"{username} ({user.id})"


def is_resume_document(update: Update) -> bool:
    document = update.message.document if update.message else None
    if not document:
        return False
    name = (document.file_name or "").lower()
    caption = (update.message.caption or "").lower()
    haystack = f"{name} {caption}"
    return name.endswith(".pdf") and any(
        keyword in haystack
        for keyword in ["이력서", "resume", "cv", "지원자", "후보자", "채용"]
    )


# ── PDF 텍스트 추출 ────────────────────────────────────────────────────────────────

def _extract_pdf_text_with_python(pdf_path: Path) -> str:
    extractors = []
    try:
        from pypdf import PdfReader  # type: ignore
        extractors.append(PdfReader)
    except Exception:
        pass
    try:
        from PyPDF2 import PdfReader  # type: ignore
        extractors.append(PdfReader)
    except Exception:
        pass
    for reader_cls in extractors:
        try:
            reader = reader_cls(str(pdf_path))
            text = "\n".join((page.extract_text() or "") for page in reader.pages[:20]).strip()
            if text:
                return text
        except Exception:
            continue
    try:
        import pdfplumber  # type: ignore
        with pdfplumber.open(str(pdf_path)) as pdf:
            text = "\n".join((page.extract_text() or "") for page in pdf.pages[:20]).strip()
            if text:
                return text
    except Exception:
        pass
    return ""


def extract_pdf_text_local(pdf_path: Path) -> tuple[str, str]:
    text = _extract_pdf_text_with_python(pdf_path)
    if text:
        return text, "python_pdf_library"
    pdftotext = shutil.which("pdftotext")
    if pdftotext:
        try:
            result = subprocess.run(
                [pdftotext, "-layout", str(pdf_path), "-"],
                check=False,
                capture_output=True,
                text=True,
                timeout=30,
            )
            if result.stdout.strip():
                return result.stdout.strip(), "pdftotext"
        except Exception:
            pass
    return "", "extraction_failed"


def build_local_resume_report(text: str, file_name: str) -> str:
    safe_text = sanitize_resume_text_for_ai(text)
    lines = [line.strip() for line in safe_text.splitlines() if line.strip()]
    first_lines = "\n".join(lines[:18])
    year_ranges = re.findall(
        r"(?:19|20)\d{2}\s*[~\-–]\s*(?:(?:19|20)\d{2}|현재|Present|present)", safe_text
    )
    skill_keywords = [
        "Revit", "Navisworks", "BIM", "AutoCAD", "Dynamo", "Python",
        "Excel", "MEP", "HVAC", "전기", "소방", "배관", "덕트", "CDE", "BEP",
    ]
    lower = safe_text.lower()
    skills = [kw for kw in skill_keywords if kw.lower() in lower]
    project_lines = [
        line for line in lines
        if any(k in line.lower() for k in ["project", "프로젝트", "현장", "공사", "설계", "bim"])
    ]
    report = (
        "🧾 [HR_인재분석관 로컬 이력서 분석 초안]\n\n"
        f"- 파일명: {sanitize_outbound_text(file_name)}\n"
        "- 처리 방식: 로컬 PDF 텍스트 추출 + 규칙 기반 1차 분석\n"
        "- 외부 API 전송: 없음\n\n"
        "【1. 추출 상태】\n"
        f"- 추출 텍스트 길이: {len(safe_text):,}자\n"
        f"- 감지된 경력 기간 표현: {len(year_ranges)}개\n"
        f"- 감지 기술 키워드: {', '.join(skills) if skills else '자동 감지 부족'}\n\n"
        "【2. 대시보드 후보 데이터】\n"
        "- 후보자 개요: 이름/연락처는 마스킹 후 검토 필요\n"
        "- 경력 타임라인: 연도/회사/직책 행을 기준으로 확인 필요\n"
        "- 프로젝트 분석: 프로젝트/현장/설계/BIM 포함 문장을 우선 후보로 추출\n"
        "- 기술 역량: 감지된 기술 키워드를 기준으로 1차 태깅\n\n"
        "【3. 프로젝트/경력 후보 문장】\n"
        + ("\n".join(f"- {sanitize_outbound_text(line)[:160]}" for line in project_lines[:8]) or "- 자동 추출 후보 없음")
        + "\n\n【4. 원문 앞부분 미리보기】\n"
        f"{first_lines[:1400]}\n\n"
        "【5. 다음 단계】\n"
        "- 로컬 LLM 또는 DeepSeek 보조 분석은 개인정보 마스킹 후에만 실행합니다.\n"
        "- AI 등급/S-A-B 평가는 최종 채용 판단이 아니라 면접 전 검토 초안으로만 사용합니다."
    )
    return report[:3800]
