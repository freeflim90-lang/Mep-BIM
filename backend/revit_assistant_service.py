from __future__ import annotations

import datetime as dt
import json
import re
from pathlib import Path
from typing import Any, Awaitable, Callable


OPERATIONAL_KNOWLEDGE_AGENTS = {"지식업데이트", "지식큐레이터"}
KNOWLEDGE_CANDIDATE_TAGS = "qa,auto-collect,revit-addin,search-assisted,knowledge-candidate,needs-review"


class RevitAssistantMetrics:
    def __init__(self) -> None:
        self.chat_total = 0
        self.chat_success = 0
        self.chat_local = 0
        self.chat_search_assisted = 0
        self.feedback_total = 0
        self.feedback_updated = 0
        self.error_total = 0
        self.error_stages: dict[str, int] = {}

    def record_chat_success(self, *, search_result: str) -> None:
        self.chat_total += 1
        self.chat_success += 1
        if search_result:
            self.chat_search_assisted += 1
        else:
            self.chat_local += 1

    def record_chat_error(self, stage: str) -> None:
        self.chat_total += 1
        self.error_total += 1
        self.error_stages[stage] = self.error_stages.get(stage, 0) + 1

    def record_feedback(self, status: str) -> None:
        self.feedback_total += 1
        if status == "updated":
            self.feedback_updated += 1

    def snapshot(self) -> dict[str, Any]:
        return {
            "chat_total": self.chat_total,
            "chat_success": self.chat_success,
            "chat_local": self.chat_local,
            "chat_search_assisted": self.chat_search_assisted,
            "feedback_total": self.feedback_total,
            "feedback_updated": self.feedback_updated,
            "error_total": self.error_total,
            "error_stages": dict(sorted(self.error_stages.items())),
        }


def source_tag_for_revit_answer(*, matches: list[dict[str, Any]], top_score: int | float, search_result: str) -> str:
    has_local = bool(matches and top_score >= 10)
    has_web = bool(search_result)
    if top_score >= 40:
        return f"📚 지식 베이스 (score {top_score})"
    if has_local and has_web:
        return f"📚 지식 베이스 (score {top_score}) + 🔍 웹 검색 보강"
    if has_local:
        return f"📚 지식 베이스 (score {top_score})"
    if has_web:
        return "🔍 웹 검색"
    return "❓ 지식 없음 — 지식 베이스 보강 필요"


def resolve_knowledge_candidate_agent(
    *,
    agent: str,
    query: str,
    knowledge_agents: set[str] | list[str] | tuple[str, ...],
    infer_agent: Callable[[str], str],
    fallback_agent: str = "건축",
) -> str:
    known_agents = set(knowledge_agents)
    save_agent = agent if agent in known_agents and agent not in OPERATIONAL_KNOWLEDGE_AGENTS else infer_agent(query)
    if save_agent in OPERATIONAL_KNOWLEDGE_AGENTS or save_agent not in known_agents:
        return fallback_agent
    return save_agent


def build_search_assisted_knowledge_candidate(
    *,
    agent: str,
    query: str,
    question: str,
    answer: str,
    search_result: str,
    knowledge_agents: set[str] | list[str] | tuple[str, ...],
    infer_agent: Callable[[str], str],
    sanitizer: Callable[[str], str],
) -> dict[str, str] | None:
    if not search_result:
        return None

    clean_answer = sanitizer(answer.split("\n\n📚")[0].strip())
    if not clean_answer or len(clean_answer) <= 20:
        return None

    save_agent = resolve_knowledge_candidate_agent(
        agent=agent,
        query=query,
        knowledge_agents=knowledge_agents,
        infer_agent=infer_agent,
    )
    return {
        "agent": save_agent,
        "title": f"Q: {question[:60]}",
        "source": "search-assisted-qa",
        "tags": KNOWLEDGE_CANDIDATE_TAGS,
        "content": (
            f"Status: needs-review\n\n"
            f"Question:\n{sanitizer(question.strip())}\n\n"
            f"Draft answer:\n{clean_answer}\n\n"
            f"Search evidence:\n{sanitizer(search_result.strip())[:2500]}"
        ),
    }


def persist_revit_knowledge_side_effects(
    *,
    knowledge_candidate: dict[str, str] | None,
    search_result: str,
    query: str,
    agent: str,
    top_score: int | float,
    append_knowledge_update: Callable[[Any], Any],
    knowledge_update_factory: Callable[..., Any],
    append_gap_log: Callable[..., Any],
) -> None:
    if knowledge_candidate:
        append_knowledge_update(knowledge_update_factory(**knowledge_candidate))

    if search_result:
        append_gap_log(
            query=query,
            agent=agent,
            assessment={"reasons": [], "top_score": top_score, "top_path": ""},
            search_result=search_result,
        )


async def compose_revit_assistant_answer(
    *,
    query: str,
    question: str,
    agent: str,
    matches: list[dict[str, Any]],
    top_score: int | float,
    knowledge_agents: set[str] | list[str] | tuple[str, ...],
    build_local_answer: Callable[[str, list[dict[str, Any]], str], str],
    search_web: Callable[[str, str], Awaitable[str]],
    build_context: Callable[[str, str, list[dict[str, Any]]], str],
    synthesize: Callable[[str, str], Awaitable[str]],
    enforce_answer: Callable[[str, str], str],
    infer_agent: Callable[[str], str],
    sanitizer: Callable[[str], str],
) -> dict[str, Any]:
    search_result = ""
    if top_score >= 40:
        answer = build_local_answer(query, matches, agent)
    else:
        search_result = await search_web(agent, query)
        raw_context = build_context(query, search_result, matches)
        answer = await synthesize(query, raw_context) or raw_context
        answer = enforce_answer(answer, question.strip() or "LUAChat 질문")

    source_tag = source_tag_for_revit_answer(matches=matches, top_score=top_score, search_result=search_result)
    candidate = build_search_assisted_knowledge_candidate(
        agent=agent,
        query=query,
        question=question,
        answer=answer,
        search_result=search_result,
        knowledge_agents=knowledge_agents,
        infer_agent=infer_agent,
        sanitizer=sanitizer,
    )
    return {
        "answer": answer,
        "source_tag": source_tag,
        "search_result": search_result,
        "knowledge_candidate": candidate,
    }


def serialize_revit_sources(matches: list[dict[str, Any]], *, project_root: Path, limit: int = 5) -> list[dict[str, Any]]:
    sources: list[dict[str, Any]] = []
    for match in matches[:limit]:
        match_path = match.get("path")
        if isinstance(match_path, Path):
            try:
                rel = match_path.relative_to(project_root).as_posix()
            except ValueError:
                rel = match_path.as_posix()
        else:
            rel = str(match_path)
        sources.append({"path": rel, "score": match.get("score", 0)})
    return sources


def build_revit_chat_response(
    *,
    agent: str,
    answer: str,
    matches: list[dict[str, Any]],
    search_result: str,
    note_path: Path,
    project_root: Path,
    note_archive_mode: str = "obsidian",
) -> dict[str, Any]:
    return {
        "status": "ok",
        "brand": "LUA BIM LABS",
        "agent": agent,
        "answer": answer,
        "sources": serialize_revit_sources(matches, project_root=project_root),
        "note_path": note_path.relative_to(project_root).as_posix(),
        "note_archive_mode": note_archive_mode,
        "needs_more": not bool(matches) and not bool(search_result),
    }


def build_revit_error_response(
    *,
    stage: str,
    exc: Exception,
    sanitizer: Callable[[str], str],
    agent: str = "",
) -> dict[str, Any]:
    reason = sanitizer(str(exc)).strip()[:500] or exc.__class__.__name__
    return {
        "status": "error",
        "brand": "LUA BIM LABS",
        "agent": agent,
        "stage": stage,
        "reason": reason,
        "answer": "",
        "sources": [],
        "needs_more": True,
    }


def build_revit_partial_chat_response(
    *,
    agent: str,
    answer: str,
    matches: list[dict[str, Any]],
    search_result: str,
    project_root: Path,
    warning_stage: str,
    warning: Exception,
    sanitizer: Callable[[str], str],
) -> dict[str, Any]:
    reason = sanitizer(str(warning)).strip()[:500] or warning.__class__.__name__
    return {
        "status": "partial",
        "brand": "LUA BIM LABS",
        "agent": agent,
        "answer": answer,
        "sources": serialize_revit_sources(matches, project_root=project_root),
        "note_path": None,
        "needs_more": not bool(matches) and not bool(search_result),
        "warning_stage": warning_stage,
        "warning": reason,
    }


def mark_revit_assistant_processing(
    *,
    agent_states: dict[str, dict[str, Any]],
    agent: str,
    message: str,
    ensure_agent_state: Callable[[str], None],
) -> None:
    ensure_agent_state(agent)
    agent_states[agent]["status"] = "Active"
    agent_states[agent]["message"] = f"Revit Assistant 질문 처리: {message[:60]}"
    agent_states[agent]["tokens"] += 1
    ensure_agent_state("지식업데이트")
    agent_states["지식업데이트"]["message"] = "Revit Assistant Q&A를 Obsidian 지식 루프에 기록했습니다."


def mark_revit_assistant_idle(
    *,
    agent_states: dict[str, dict[str, Any]],
    agent: str,
    ensure_agent_state: Callable[[str], None],
) -> None:
    ensure_agent_state(agent)
    agent_states[agent]["status"] = "Idle"


def fallback_revit_note_title(message: str, *, now: dt.datetime) -> str:
    stem = re.sub(r"[^0-9A-Za-z가-힣_-]+", "_", message.strip()).strip("_")[:60]
    return f"QA-FALLBACK-{now.strftime('%Y%m%d-%H%M%S')}-{stem or 'revit_assistant_qa'}.md"


def write_revit_qa_fallback_note(
    *,
    fallback_dir: Path,
    request: Any,
    answer: str,
    agent: str,
    search_result: str,
    source_tag: str,
    top_score: int | float,
    primary_error: Exception,
    now: dt.datetime | None = None,
) -> Path:
    timestamp = now or dt.datetime.now()
    fallback_dir.mkdir(parents=True, exist_ok=True)
    path = fallback_dir / fallback_revit_note_title(request.message, now=timestamp)
    content = (
        "---\n"
        "type: revit-assistant-qa-fallback\n"
        "status: fallback-archive-needs-obsidian-replay\n"
        f"date: {timestamp.date().isoformat()}\n"
        f"agent: {agent}\n"
        f"source_tag: \"{source_tag}\"\n"
        f"top_score: {top_score}\n"
        "---\n\n"
        "# Revit Assistant QA Fallback Archive\n\n"
        "Primary Obsidian QA archive failed. This fallback preserves the customer answer and replay context.\n\n"
        "## Primary Archive Error\n\n"
        f"```text\n{primary_error}\n```\n\n"
        "## Request\n\n"
        f"- user_id: {getattr(request, 'user_id', '') or 'revit_user'}\n"
        f"- client_version: {getattr(request, 'client_version', '') or ''}\n\n"
        f"{getattr(request, 'message', '').strip()}\n\n"
        "## Revit Context\n\n"
        f"```text\n{getattr(request, 'revit_context', '') or '선택 요소 없음'}\n```\n\n"
        "## Answer\n\n"
        f"{answer}\n\n"
        "## Search Result\n\n"
        f"```text\n{search_result or '검색 보강 없음'}\n```\n"
    )
    path.write_text(content, encoding="utf-8")
    return path


def save_revit_qa_note_with_fallback(
    *,
    save_note: Callable[..., Path],
    fallback_note_dir: Path | None,
    request: Any,
    answer: str,
    agent: str,
    matches: list[dict[str, Any]],
    search_result: str,
    source_tag: str,
    top_score: int | float,
) -> tuple[Path, str]:
    try:
        return (
            save_note(
                request=request,
                answer=answer,
                agent=agent,
                matches=matches,
                search_result=search_result,
                source_tag=source_tag,
                top_score=top_score,
            ),
            "obsidian",
        )
    except Exception as primary_error:
        if fallback_note_dir is None:
            raise
        try:
            return (
                write_revit_qa_fallback_note(
                    fallback_dir=fallback_note_dir,
                    request=request,
                    answer=answer,
                    agent=agent,
                    search_result=search_result,
                    source_tag=source_tag,
                    top_score=top_score,
                    primary_error=primary_error,
                ),
                "fallback",
            )
        except Exception:
            raise primary_error


async def finalize_revit_assistant_chat(
    *,
    request: Any,
    answer: str,
    agent: str,
    matches: list[dict[str, Any]],
    search_result: str,
    source_tag: str,
    top_score: int | float,
    project_root: Path,
    agent_states: dict[str, dict[str, Any]],
    ensure_agent_state: Callable[[str], None],
    save_note: Callable[..., Path],
    send_state: Callable[[], Awaitable[Any]],
    refresh_knowledge: Callable[[], Awaitable[Any]],
    launch_background_task: Callable[[Awaitable[Any]], Any],
    fallback_note_dir: Path | None = None,
) -> dict[str, Any]:
    note_path, note_archive_mode = save_revit_qa_note_with_fallback(
        save_note=save_note,
        fallback_note_dir=fallback_note_dir,
        request=request,
        answer=answer,
        agent=agent,
        matches=matches,
        search_result=search_result,
        source_tag=source_tag,
        top_score=top_score,
    )
    mark_revit_assistant_processing(
        agent_states=agent_states,
        agent=agent,
        message=request.message,
        ensure_agent_state=ensure_agent_state,
    )
    await send_state()
    mark_revit_assistant_idle(
        agent_states=agent_states,
        agent=agent,
        ensure_agent_state=ensure_agent_state,
    )
    await send_state()
    launch_background_task(refresh_knowledge())
    return build_revit_chat_response(
        agent=agent,
        answer=answer,
        matches=matches,
        search_result=search_result,
        note_path=note_path,
        project_root=project_root,
        note_archive_mode=note_archive_mode,
    )


def luachat_health_payload(
    *,
    obsidian_vault: Path,
    project_root: Path,
    token_required: bool,
    search_providers: dict[str, bool],
    metrics: dict[str, Any] | None = None,
    metrics_snapshot_path: str | None = None,
) -> dict[str, Any]:
    payload = {
        "status": "ok",
        "service": "LUAChat Mac mini server",
        "chat_endpoint": "/api/luachat",
        "feedback_endpoint": "/api/luachat/feedback",
        "obsidian_vault": obsidian_vault.relative_to(project_root).as_posix(),
        "token_required": token_required,
        "search_providers": search_providers,
    }
    if metrics is not None:
        payload["metrics"] = metrics
    if metrics_snapshot_path is not None:
        payload["metrics_snapshot_path"] = metrics_snapshot_path
    return payload


def write_luachat_metrics_daily_snapshot(
    *,
    path: Path,
    metrics: dict[str, Any],
    now: dt.datetime,
) -> dict[str, Any]:
    date_key = now.date().isoformat()
    payload: dict[str, Any] = {"service": "luachat", "days": {}}

    if path.exists():
        try:
            loaded = json.loads(path.read_text(encoding="utf-8"))
            if isinstance(loaded, dict):
                payload.update(loaded)
        except (OSError, json.JSONDecodeError):
            payload = {"service": "luachat", "days": {}}

    days = payload.get("days")
    if not isinstance(days, dict):
        days = {}
        payload["days"] = days

    row = {
        "date": date_key,
        "updated_at": now.isoformat(timespec="seconds"),
        "metrics": metrics,
    }
    days[date_key] = row
    payload["latest_date"] = date_key

    path.parent.mkdir(parents=True, exist_ok=True)
    temp_path = path.with_suffix(path.suffix + ".tmp")
    temp_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    temp_path.replace(path)
    return row


def update_revit_feedback_note(
    *,
    note_path: Path | None,
    note_path_label: str,
    user_id: str,
    feedback: str,
    is_good: bool,
    now: dt.datetime,
    sanitizer: Callable[[str], str],
    rebuild_revit_qa_moc: Callable[[], Any],
    refresh_knowledge: Callable[[], Awaitable[Any]],
    launch_background_task: Callable[[Awaitable[Any]], Any],
) -> dict[str, str]:
    if not note_path or not note_path.exists() or not note_path.is_file():
        return {"status": "ignored", "reason": "note_path not found"}

    try:
        text = note_path.read_text(encoding="utf-8", errors="ignore")
        text = apply_revit_feedback_to_text(
            text,
            user_id=user_id,
            feedback=feedback,
            is_good=is_good,
            now=now,
            sanitizer=sanitizer,
        )
        note_path.write_text(text, encoding="utf-8")
        rebuild_revit_qa_moc()
        launch_background_task(refresh_knowledge())
        return {"status": "updated", "note_path": note_path_label}
    except OSError as exc:
        return {"status": "rejected", "reason": str(exc)}


def apply_revit_feedback_to_text(
    text: str,
    *,
    user_id: str,
    feedback: str,
    is_good: bool,
    now: dt.datetime,
    sanitizer: Callable[[str], str],
) -> str:
    status = "answered-good" if is_good else "knowledge-gap-needs-review"
    updated = re.sub(r"^status:\s*.+$", f"status: {status}", text, count=1, flags=re.MULTILINE)
    safe_feedback = sanitizer(feedback.strip() or ("좋아요" if is_good else "아쉬워요"))
    return (
        updated
        + f"\n\n## Revit Assistant 피드백 ({now.strftime('%Y-%m-%d %H:%M:%S')})\n"
        + f"- User: {sanitizer(user_id)}\n"
        + f"- Result: {'good' if is_good else 'needs-review'}\n\n"
        + f"{safe_feedback}\n"
    )
