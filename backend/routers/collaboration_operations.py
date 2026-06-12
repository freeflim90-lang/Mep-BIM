from __future__ import annotations

from typing import Any, Callable

from fastapi import APIRouter

from backend.models import RoutePreviewRequest


def public_workflow_row(workflow: dict[str, Any]) -> dict[str, Any]:
    return {
        "id": workflow["id"],
        "name": workflow["name"],
        "primary": workflow["primary"],
        "participants": workflow["participants"],
        "steps": workflow["steps"],
        "local_only": workflow["local_only"],
    }


def create_collaboration_operations_router(
    *,
    collaboration: Any,
    active_collaboration_workflows: Callable[[], list[dict[str, Any]]],
    preview_collaboration_route: Callable[[str], dict[str, Any]],
    ensure_agent_state: Callable[[str], None],
    agent_states: dict[str, dict[str, Any]],
) -> APIRouter:
    router = APIRouter(tags=["collaboration-operations"])

    @router.get("/api/collaboration-workflows")
    async def list_collaboration_workflows():
        return {"workflows": [public_workflow_row(workflow) for workflow in active_collaboration_workflows()]}

    @router.get("/api/role-boundaries")
    async def list_role_boundaries():
        return {"roles": collaboration.ROLE_BOUNDARIES}

    @router.get("/api/collaboration-audit")
    async def collaboration_audit():
        workflows = active_collaboration_workflows()
        return {
            "workflow_count": len(workflows),
            "issues": collaboration.audit_collaboration_workflows(workflows),
        }

    @router.get("/api/daily-idea-report")
    async def daily_idea_report():
        report = collaboration.build_daily_idea_report(limit=3)
        for participant in report["participants"]:
            ensure_agent_state(participant)
            agent_states[participant]["status"] = "Idle"
        ensure_agent_state("아이디어발굴")
        agent_states["아이디어발굴"]["message"] = "최고지배자 일일 3대 아이디어 보고 준비 완료. 유료 API 호출 없이 로컬 산식으로 산출."
        return {
            "status": "ok",
            **report,
        }

    @router.post("/api/route-preview")
    async def route_preview(preview: RoutePreviewRequest):
        if not preview.request.strip():
            return {"status": "rejected", "reason": "request is empty"}
        return {
            "status": "ok",
            **preview_collaboration_route(preview.request),
        }

    return router
