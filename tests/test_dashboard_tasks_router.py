from fastapi import FastAPI
from fastapi.testclient import TestClient

from backend.models import AddinTaskRequest
from backend.routers.dashboard_tasks import build_addin_task_prompt, create_dashboard_tasks_router


def make_client():
    scheduled = []
    received = []

    async def run_task(task):
        received.append(task)

    def launch(coro):
        coro.close()
        scheduled.append("scheduled")

    app = FastAPI()
    app.include_router(create_dashboard_tasks_router(
        run_addin_task=run_task,
        launch_background_task=launch,
    ))
    return TestClient(app), scheduled, received


def test_build_addin_task_prompt_preserves_dashboard_context():
    prompt = build_addin_task_prompt(
        AddinTaskRequest(
            target="Revit",
            discipline="MEP",
            priority="high",
            title="View Template Copier",
            request="dry-run 먼저 구현",
        )
    )

    assert "[Revit Add-in 개발 요청]" in prompt
    assert "공정: MEP" in prompt
    assert "우선순위: high" in prompt
    assert "요청 내용:\ndry-run 먼저 구현" in prompt


def test_dashboard_tasks_router_rejects_empty_and_schedules_valid_task():
    client, scheduled, received = make_client()

    rejected = client.post("/api/addin-task", json={"request": "   "})
    accepted = client.post(
        "/api/addin-task",
        json={
            "target": "Revit",
            "discipline": "MEP",
            "priority": "high",
            "title": "Template Copier",
            "request": "구현 요청",
        },
    )

    assert rejected.json() == {"status": "rejected", "reason": "request is empty"}
    assert accepted.json() == {"status": "accepted", "target": "Revit", "title": "Template Copier"}
    assert scheduled == ["scheduled"]
    assert received == []


def test_dashboard_tasks_router_is_registered_in_integrated_app():
    import backend.server_total as server

    paths = {route.path for route in server.app.routes}

    assert "/api/addin-task" in paths
