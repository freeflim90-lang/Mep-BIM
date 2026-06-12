from fastapi import FastAPI
from fastapi.testclient import TestClient

from backend.routers.collaboration_operations import create_collaboration_operations_router, public_workflow_row


class FakeCollaboration:
    ROLE_BOUNDARIES = {"아이디어발굴": {"owns": ["idea"], "handoff": {}}}

    @staticmethod
    def audit_collaboration_workflows(workflows):
        return [{"workflow": workflows[0]["id"], "issue": "sample"}]

    @staticmethod
    def build_daily_idea_report(limit=3):
        return {
            "participants": ["아이디어발굴", "전략기획"],
            "ideas": [{"title": "A"}, {"title": "B"}][:limit],
        }


def sample_workflows():
    return [
        {
            "id": "support_general",
            "name": "Support",
            "primary": "고객지원 CS",
            "participants": ["고객지원 CS"],
            "steps": ["classify"],
            "local_only": True,
            "keywords": ["support"],
        }
    ]


def make_client():
    states = {}

    def ensure(agent):
        states.setdefault(agent, {"status": "Active", "tokens": 0, "message": ""})

    app = FastAPI()
    app.include_router(create_collaboration_operations_router(
        collaboration=FakeCollaboration(),
        active_collaboration_workflows=sample_workflows,
        preview_collaboration_route=lambda text: {"workflow_id": "support_general", "request": text},
        ensure_agent_state=ensure,
        agent_states=states,
    ))
    return TestClient(app), states


def test_public_workflow_row_hides_keywords():
    row = public_workflow_row(sample_workflows()[0])

    assert row == {
        "id": "support_general",
        "name": "Support",
        "primary": "고객지원 CS",
        "participants": ["고객지원 CS"],
        "steps": ["classify"],
        "local_only": True,
    }


def test_collaboration_operations_router_lists_audits_and_reports():
    client, states = make_client()

    workflows = client.get("/api/collaboration-workflows")
    roles = client.get("/api/role-boundaries")
    audit = client.get("/api/collaboration-audit")
    report = client.get("/api/daily-idea-report")

    assert workflows.json()["workflows"][0]["id"] == "support_general"
    assert "keywords" not in workflows.json()["workflows"][0]
    assert roles.json()["roles"]["아이디어발굴"]["owns"] == ["idea"]
    assert audit.json() == {"workflow_count": 1, "issues": [{"workflow": "support_general", "issue": "sample"}]}
    assert report.json()["status"] == "ok"
    assert states["아이디어발굴"]["status"] == "Idle"
    assert states["전략기획"]["status"] == "Idle"
    assert states["아이디어발굴"]["message"].startswith("최고지배자 일일 3대 아이디어")


def test_collaboration_operations_router_previews_routes_and_rejects_empty():
    client, _ = make_client()

    rejected = client.post("/api/route-preview", json={"request": "   "})
    preview = client.post("/api/route-preview", json={"request": "고객지원 문의"})

    assert rejected.json() == {"status": "rejected", "reason": "request is empty"}
    assert preview.json() == {"status": "ok", "workflow_id": "support_general", "request": "고객지원 문의"}


def test_collaboration_operations_router_is_registered_in_integrated_app():
    import backend.server_total as server

    paths = {route.path for route in server.app.routes}

    assert "/api/collaboration-workflows" in paths
    assert "/api/route-preview" in paths
