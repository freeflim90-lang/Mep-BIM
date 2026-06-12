from types import SimpleNamespace

from fastapi import FastAPI
from fastapi.testclient import TestClient

from backend.routers.development_operations import build_local_coder_prompt, create_development_operations_router


class FakeGitHub:
    class GitHubIntegrationError(RuntimeError):
        pass

    def __init__(self):
        self.fail = False

    def is_configured(self):
        return True

    async def check_connection(self):
        if self.fail:
            raise self.GitHubIntegrationError("github down")
        return {"status": "ok", "configured": True}

    async def list_repositories(self, limit=20):
        return {"configured": True, "limit": limit, "repositories": [{"full_name": "lua/repo"}]}


class FakeLocalCoder:
    async def status(self):
        return {
            "enabled": True,
            "provider": "ollama",
            "model": "qwen2.5-coder:7b",
            "reachable": True,
            "model_available": True,
        }

    async def generate(self, prompt, system="", num_predict=0, timeout=0):
        return {
            "ok": True,
            "response": "Plan\nDraft\nVerification\nAPI 필요성 판단",
            "prompt": prompt,
            "system": system,
            "num_predict": num_predict,
            "timeout": timeout,
        }


class FakeQwenDrafts:
    def load_queue(self):
        return {
            "product": "Model Quality Auditor",
            "selected_item": "QA MVP",
            "tasks": [{"id": "T1"}, {"id": "T2"}],
        }

    def load_state(self):
        return {"completed": ["T1"], "in_progress": None, "last_report": {"task_id": "T1"}}

    async def run_next(self, max_tasks=1, send_reports=True, advance_on_blocked=False):
        return {
            "status": "ok",
            "runs": [{"task_id": "T2", "ok": True, "next_task": None}],
            "max_tasks": max_tasks,
            "send_reports": send_reports,
            "advance_on_blocked": advance_on_blocked,
        }


class FakeCollaboration:
    @staticmethod
    def workflow_by_id(workflows, workflow_id):
        return next((workflow for workflow in workflows if workflow["id"] == workflow_id), None)


def make_client():
    states = {}
    sent = []

    def ensure(agent):
        states.setdefault(agent, {"status": "Idle", "tokens": 0, "message": ""})

    async def send_state():
        sent.append("sent")

    app = FastAPI()
    app.include_router(create_development_operations_router(
        github_integration=FakeGitHub(),
        local_coder=FakeLocalCoder(),
        qwen_product_drafts=FakeQwenDrafts(),
        collaboration=FakeCollaboration(),
        active_collaboration_workflows=lambda: [
            {"id": "excel_qwen_automation", "name": "Excel Automation"},
            {"id": "local_qwen_development", "name": "Local Development"},
        ],
        agent_states=states,
        ensure_agent_state=ensure,
        send_state_to_dashboard=send_state,
    ))
    return TestClient(app), states, sent


def test_development_operations_router_exposes_github_and_local_coder_status():
    client, states, _ = make_client()

    github = client.get("/api/github/status")
    local_status = client.get("/api/local-coder/status")

    assert github.json()["status"] == "ok"
    assert states["인프라_DevOps (Obsidian)"]["message"]
    assert local_status.json()["status"] == "ok"
    assert states["Qwen_Coder_8B"]["message"].startswith("로컬 코더 상태 확인")


def test_development_operations_router_generates_local_coder_draft():
    client, _, _ = make_client()

    response = client.post(
        "/api/local-coder/draft",
        json={"request": "CSV 보고서 자동화", "workflow": "excel_qwen_automation"},
    )

    payload = response.json()
    assert payload["status"] == "ok"
    assert payload["workflow_id"] == "excel_qwen_automation"
    assert "pandas를 사용하거나 언급하지 마세요" in payload["prompt"]
    assert payload["num_predict"] == 320
    assert payload["timeout"] == 30


def test_development_operations_router_reports_and_runs_qwen_queue():
    client, states, sent = make_client()

    status = client.get("/api/qwen-product-drafts/status")
    run = client.post(
        "/api/qwen-product-drafts/next",
        json={"max_tasks": 9, "send_telegram": False, "advance_on_blocked": True},
    )

    assert status.json()["remaining"] == ["T2"]
    payload = run.json()
    assert payload["max_tasks"] == 3
    assert payload["send_reports"] is False
    assert payload["advance_on_blocked"] is True
    assert states["Qwen_Coder_8B"]["status"] == "Idle"
    assert sent == ["sent"]


def test_development_operations_router_is_registered_in_integrated_app():
    import backend.server_total as server

    client = TestClient(server.app)

    response = client.get("/api/local-coder/status")

    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_build_local_coder_prompt_keeps_excel_guardrails():
    prompt, system = build_local_coder_prompt(
        request="xlsx 정리",
        workflow={"id": "excel_qwen_automation", "name": "Excel Automation"},
    )

    assert "Python 표준 csv 라이브러리 + openpyxl" in prompt
    assert "Lua 언어는 절대 제안하지 마세요" in prompt
    assert "Plan, Draft, Verification, API 필요성 판단" in system
