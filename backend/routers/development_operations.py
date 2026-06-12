from __future__ import annotations

from typing import Any, Awaitable, Callable

from fastapi import APIRouter

from backend.models import LocalCoderDraftRequest, QwenProductDraftRunRequest


def build_local_coder_prompt(*, request: str, workflow: dict[str, Any]) -> tuple[str, str]:
    workflow_specific_rules = ""
    if workflow["id"] == "excel_qwen_automation":
        workflow_specific_rules = (
            "현재 요청은 엑셀 자동화입니다. pandas를 사용하거나 언급하지 마세요. "
            "CSV 처리는 Python 표준 csv 라이브러리로 수행하고, XLSX 생성과 필터 표는 openpyxl로만 작성하세요.\n"
        )
    prompt = (
        f"요청:\n{request}\n\n"
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
    )
    system = (
        "당신은 LUA BIM LABS의 로컬 Qwen 코더입니다. 모든 개발은 목적과 검증 plan을 먼저 세웁니다. "
        "엑셀 자동화 기본 구현은 Python 표준 csv 라이브러리와 openpyxl 조합이며 .NET Add-in 연계가 필요할 때만 C# OpenXML을 제안합니다. "
        "응답은 항상 Plan, Draft, Verification, API 필요성 판단 네 섹션을 모두 포함합니다. "
        "Lua 언어는 사용자가 명시적으로 요청한 경우에만 제안합니다."
    )
    return prompt, system


def create_development_operations_router(
    *,
    github_integration: Any,
    local_coder: Any,
    qwen_product_drafts: Any,
    collaboration: Any,
    active_collaboration_workflows: Callable[[], list[dict[str, Any]]],
    agent_states: dict[str, dict[str, Any]],
    ensure_agent_state: Callable[[str], None],
    send_state_to_dashboard: Callable[[], Awaitable[Any]],
) -> APIRouter:
    router = APIRouter(tags=["development-operations"])

    @router.get("/api/github/status")
    async def github_status():
        try:
            result = await github_integration.check_connection()
        except github_integration.GitHubIntegrationError as exc:
            return {
                "status": "error",
                "configured": github_integration.is_configured(),
                "reason": str(exc),
            }
        ensure_agent_state("인프라_DevOps (Obsidian)")
        agent_states["인프라_DevOps (Obsidian)"]["message"] = (
            "GitHub 연동 상태 확인 완료. 토큰은 환경변수에서만 읽고 응답에는 노출하지 않음."
        )
        return result

    @router.get("/api/github/repos")
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

    @router.get("/api/local-coder/status")
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

    @router.post("/api/local-coder/draft")
    async def local_coder_draft(draft: LocalCoderDraftRequest):
        if not draft.request.strip():
            return {"status": "rejected", "reason": "request is empty"}
        workflows = active_collaboration_workflows()
        workflow = (
            collaboration.workflow_by_id(workflows, draft.workflow)
            or collaboration.workflow_by_id(workflows, "local_qwen_development")
            or workflows[0]
        )
        prompt, system = build_local_coder_prompt(request=draft.request, workflow=workflow)
        result = await local_coder.generate(prompt, system=system, num_predict=320, timeout=30)
        return {
            "status": "ok" if result.get("ok") else "error",
            "workflow_id": workflow["id"],
            **result,
        }

    @router.get("/api/qwen-product-drafts/status")
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

    @router.post("/api/qwen-product-drafts/next")
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

    return router
