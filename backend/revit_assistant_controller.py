from __future__ import annotations

import datetime as dt
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Awaitable, Callable

from backend.revit_assistant_service import (
    RevitAssistantMetrics,
    build_revit_error_response,
    build_revit_partial_chat_response,
    compose_revit_assistant_answer,
    finalize_revit_assistant_chat,
    persist_revit_knowledge_side_effects,
)


@dataclass(frozen=True)
class RevitAssistantChatDependencies:
    extract_bearer_token: Callable[[str | None], str | None]
    require_api_key: Callable[[str | None], None]
    build_context_prompt: Callable[[str, dict[str, Any]], str]
    infer_agent: Callable[[str], str]
    search_local_knowledge: Callable[..., list[dict[str, Any]]]
    prioritize_matches: Callable[[list[dict[str, Any]], str], list[dict[str, Any]]]
    knowledge_agents: set[str] | list[str] | tuple[str, ...]
    build_local_answer: Callable[[str, list[dict[str, Any]], str], str]
    search_web: Callable[[str, str], Awaitable[str]]
    build_context: Callable[[str, str, list[dict[str, Any]]], str]
    synthesize: Callable[[str, str], Awaitable[str]]
    enforce_answer: Callable[[str, str], str]
    sanitizer: Callable[[str], str]
    append_knowledge_update: Callable[[Any], Any]
    knowledge_update_factory: Callable[..., Any]
    append_gap_log: Callable[..., Any]
    metrics: RevitAssistantMetrics
    save_metrics_snapshot: Callable[[], None]
    project_root: Path
    agent_states: dict[str, dict[str, Any]]
    ensure_agent_state: Callable[[str], None]
    save_note: Callable[..., Path]
    send_state: Callable[[], Awaitable[Any]]
    refresh_knowledge: Callable[[], Awaitable[Any]]
    launch_background_task: Callable[[Awaitable[Any]], Any]
    fallback_note_dir: Path | None = None


@dataclass(frozen=True)
class RevitAssistantFeedbackDependencies:
    extract_bearer_token: Callable[[str | None], str | None]
    require_api_key: Callable[[str | None], None]
    resolve_note_path: Callable[[str], Path | None]
    update_note: Callable[..., dict[str, str]]
    sanitizer: Callable[[str], str]
    rebuild_revit_qa_moc: Callable[[], Any]
    refresh_knowledge: Callable[[], Awaitable[Any]]
    launch_background_task: Callable[[Awaitable[Any]], Any]
    metrics: RevitAssistantMetrics
    save_metrics_snapshot: Callable[[], None]
    now: Callable[[], dt.datetime]


async def handle_revit_assistant_chat(
    *,
    request: Any,
    api_key: str | None,
    authorization: str | None,
    deps: RevitAssistantChatDependencies,
) -> dict[str, Any]:
    deps.require_api_key(api_key or deps.extract_bearer_token(authorization))
    if not request.message.strip():
        return {"status": "rejected", "reason": "message is empty"}

    try:
        query_with_context = deps.build_context_prompt(request.message, request.revit_context)
        agent = deps.infer_agent(query_with_context)
        matches = deps.prioritize_matches(deps.search_local_knowledge(query_with_context, limit=5), agent)
        top_score = matches[0]["score"] if matches else 0
    except Exception as exc:
        deps.metrics.record_chat_error("knowledge_lookup")
        deps.save_metrics_snapshot()
        return build_revit_error_response(
            stage="knowledge_lookup",
            exc=exc,
            sanitizer=deps.sanitizer,
        )

    try:
        answer_payload = await compose_revit_assistant_answer(
            query=query_with_context,
            question=request.message,
            agent=agent,
            matches=matches,
            top_score=top_score,
            knowledge_agents=deps.knowledge_agents,
            build_local_answer=deps.build_local_answer,
            search_web=deps.search_web,
            build_context=deps.build_context,
            synthesize=deps.synthesize,
            enforce_answer=deps.enforce_answer,
            infer_agent=deps.infer_agent,
            sanitizer=deps.sanitizer,
        )
    except Exception as exc:
        deps.metrics.record_chat_error("answer_generation")
        deps.save_metrics_snapshot()
        return build_revit_error_response(
            stage="answer_generation",
            exc=exc,
            sanitizer=deps.sanitizer,
            agent=agent,
        )

    answer = answer_payload["answer"]
    source_tag = answer_payload["source_tag"]
    search_result = answer_payload["search_result"]
    try:
        persist_revit_knowledge_side_effects(
            knowledge_candidate=answer_payload["knowledge_candidate"],
            search_result=search_result,
            query=query_with_context,
            agent=agent,
            top_score=top_score,
            append_knowledge_update=deps.append_knowledge_update,
            knowledge_update_factory=deps.knowledge_update_factory,
            append_gap_log=deps.append_gap_log,
        )
    except Exception as exc:
        deps.metrics.record_chat_error("knowledge_persistence")
        deps.save_metrics_snapshot()
        return build_revit_error_response(
            stage="knowledge_persistence",
            exc=exc,
            sanitizer=deps.sanitizer,
            agent=agent,
        )

    answer = deps.enforce_answer(answer, request.message.strip() or "LUAChat 질문")
    answer = f"[{source_tag}]\n\n{answer}"

    try:
        payload = await finalize_revit_assistant_chat(
            request=request,
            answer=answer,
            agent=agent,
            matches=matches,
            search_result=search_result,
            source_tag=source_tag,
            top_score=top_score,
            project_root=deps.project_root,
            agent_states=deps.agent_states,
            ensure_agent_state=deps.ensure_agent_state,
            save_note=deps.save_note,
            send_state=deps.send_state,
            refresh_knowledge=deps.refresh_knowledge,
            launch_background_task=deps.launch_background_task,
            fallback_note_dir=deps.fallback_note_dir,
        )
        deps.metrics.record_chat_success(search_result=search_result)
        deps.save_metrics_snapshot()
        return payload
    except Exception as exc:
        deps.metrics.record_chat_error("note_persistence")
        deps.save_metrics_snapshot()
        return build_revit_partial_chat_response(
            agent=agent,
            answer=answer,
            matches=matches,
            search_result=search_result,
            project_root=deps.project_root,
            warning_stage="note_persistence",
            warning=exc,
            sanitizer=deps.sanitizer,
        )


async def handle_revit_assistant_feedback(
    *,
    request: Any,
    api_key: str | None,
    authorization: str | None,
    deps: RevitAssistantFeedbackDependencies,
) -> dict[str, str]:
    deps.require_api_key(api_key or deps.extract_bearer_token(authorization))
    payload = deps.update_note(
        note_path=deps.resolve_note_path(request.note_path),
        note_path_label=request.note_path,
        user_id=request.user_id,
        feedback=request.feedback,
        is_good=request.is_good,
        now=deps.now(),
        sanitizer=deps.sanitizer,
        rebuild_revit_qa_moc=deps.rebuild_revit_qa_moc,
        refresh_knowledge=deps.refresh_knowledge,
        launch_background_task=deps.launch_background_task,
    )
    deps.metrics.record_feedback(payload.get("status", ""))
    deps.save_metrics_snapshot()
    return payload
