from __future__ import annotations

from typing import Awaitable, Callable

from fastapi import APIRouter

from backend.models import AddinTaskRequest


def build_addin_task_prompt(task: AddinTaskRequest) -> str:
    return (
        f"[{task.target} Add-in 개발 요청]\n"
        f"공정: {task.discipline}\n"
        f"우선순위: {task.priority}\n"
        f"제목: {task.title}\n"
        f"요청 내용:\n{task.request}"
    )


def create_dashboard_tasks_router(
    *,
    run_addin_task: Callable[[AddinTaskRequest], Awaitable[None]],
    launch_background_task: Callable[[Awaitable[None]], object],
) -> APIRouter:
    router = APIRouter(tags=["dashboard-tasks"])

    @router.post("/api/addin-task")
    async def create_addin_task(task: AddinTaskRequest):
        if not task.request.strip():
            return {"status": "rejected", "reason": "request is empty"}
        launch_background_task(run_addin_task(task))
        return {
            "status": "accepted",
            "target": task.target,
            "title": task.title,
        }

    return router
