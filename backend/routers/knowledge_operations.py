from __future__ import annotations

import re
from pathlib import Path
from typing import Any, Awaitable, Callable

from fastapi import APIRouter

from backend.models import KnowledgeUpdateRequest


def parse_knowledge_stats_from_log(log_path: Path) -> dict[str, int]:
    nodes, edges, source_docs = 0, 0, 0
    try:
        lines = log_path.read_text(encoding="utf-8", errors="ignore").splitlines()
    except OSError:
        return {"nodes": nodes, "edges": edges, "source_docs": source_docs}

    for line in reversed(lines):
        match = re.search(r"source_docs=(\d+).*nodes=(\d+).*edges=(\d+)", line)
        if match:
            source_docs, nodes, edges = int(match.group(1)), int(match.group(2)), int(match.group(3))
            break
    return {"nodes": nodes, "edges": edges, "source_docs": source_docs}


def create_knowledge_operations_router(
    *,
    project_root: Path,
    ensure_knowledge_base: Callable[[], None],
    knowledge_agents: list[str],
    knowledge_dir: str,
    append_knowledge_update: Callable[[KnowledgeUpdateRequest], dict[str, Any]],
    submit_knowledge_approval_candidate: Callable[[KnowledgeUpdateRequest, dict[str, Any]], Awaitable[dict[str, Any] | None]],
    ensure_agent_state: Callable[[str], None],
    agent_states: dict[str, dict[str, Any]],
    send_state_to_dashboard: Callable[[], Awaitable[Any]],
    get_persistent_gaps: Callable[[int], list[dict[str, Any]]],
) -> APIRouter:
    router = APIRouter(tags=["knowledge-operations"])

    @router.get("/api/knowledge-agents")
    async def list_knowledge_agents():
        ensure_knowledge_base()
        return {
            "agents": knowledge_agents,
            "directory": knowledge_dir,
        }

    @router.post("/api/knowledge-update")
    async def create_knowledge_update(update: KnowledgeUpdateRequest):
        try:
            result = append_knowledge_update(update)
        except ValueError as exc:
            return {"status": "rejected", "reason": str(exc)}
        approval_candidate = await submit_knowledge_approval_candidate(update, result)
        ensure_agent_state(update.agent)
        agent_states[update.agent]["message"] = f"지식 업데이트 반영: {update.title[:60]}"
        agent_states[update.agent]["tokens"] += 1
        await send_state_to_dashboard()
        return {
            "status": "updated",
            "approval_candidate_id": approval_candidate["id"] if approval_candidate else "",
            **result,
        }

    @router.get("/api/knowledge-stats")
    async def knowledge_stats():
        return {
            "status": "ok",
            **parse_knowledge_stats_from_log(project_root / "logs" / "hourly_ax_signal_monitor.log"),
        }

    @router.get("/api/knowledge-gap/persistent")
    async def persistent_knowledge_gaps(min_count: int = 3):
        gaps = get_persistent_gaps(min_count=min_count)
        return {
            "status": "ok",
            "min_count": min_count,
            "total": len(gaps),
            "gaps": gaps,
        }

    return router
