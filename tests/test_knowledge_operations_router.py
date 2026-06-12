from pathlib import Path

from fastapi import FastAPI
from fastapi.testclient import TestClient

from backend.routers.knowledge_operations import create_knowledge_operations_router, parse_knowledge_stats_from_log


def test_parse_knowledge_stats_from_log_uses_latest_valid_row(tmp_path: Path):
    log = tmp_path / "hourly_ax_signal_monitor.log"
    log.write_text(
        "old source_docs=3 nodes=4 edges=5\n"
        "noise\n"
        "new source_docs=8 nodes=13 edges=21\n",
        encoding="utf-8",
    )

    assert parse_knowledge_stats_from_log(log) == {"source_docs": 8, "nodes": 13, "edges": 21}
    assert parse_knowledge_stats_from_log(tmp_path / "missing.log") == {"source_docs": 0, "nodes": 0, "edges": 0}


def make_client(tmp_path: Path):
    states = {}
    sent = []
    updates = []
    ensured = []

    def ensure_kb():
        ensured.append("kb")

    def ensure_agent(agent):
        states.setdefault(agent, {"status": "Idle", "tokens": 0, "message": ""})

    async def send_state():
        sent.append("sent")

    async def submit_candidate(update, result):
        return {"id": "K-test"} if "needs-review" in update.tags else None

    def append_update(update):
        updates.append(update)
        if update.agent == "Bad":
            raise ValueError("unsupported")
        return {"agent": update.agent, "path": str(tmp_path / "kb.md"), "updated_at": "now", "skipped": False}

    app = FastAPI()
    app.include_router(create_knowledge_operations_router(
        project_root=tmp_path,
        ensure_knowledge_base=ensure_kb,
        knowledge_agents=["건축", "Revit_Addin"],
        knowledge_dir=str(tmp_path / "knowledge_base"),
        append_knowledge_update=append_update,
        submit_knowledge_approval_candidate=submit_candidate,
        ensure_agent_state=ensure_agent,
        agent_states=states,
        send_state_to_dashboard=send_state,
        get_persistent_gaps=lambda min_count: [{"query": "gap", "count": min_count, "agent": "건축"}],
    ))
    return TestClient(app), states, sent, updates, ensured


def test_knowledge_operations_router_lists_agents_and_updates_knowledge(tmp_path: Path):
    client, states, sent, updates, ensured = make_client(tmp_path)

    agents = client.get("/api/knowledge-agents")
    updated = client.post(
        "/api/knowledge-update",
        json={
            "agent": "건축",
            "title": "반복 질문",
            "content": "검토할 지식 내용",
            "source": "telegram-auto",
            "tags": "needs-review",
        },
    )

    assert agents.json() == {"agents": ["건축", "Revit_Addin"], "directory": str(tmp_path / "knowledge_base")}
    assert ensured == ["kb"]
    assert updated.json()["status"] == "updated"
    assert updated.json()["approval_candidate_id"] == "K-test"
    assert updates[0].agent == "건축"
    assert states["건축"]["tokens"] == 1
    assert sent == ["sent"]


def test_knowledge_operations_router_rejects_invalid_update_and_reports_gaps(tmp_path: Path):
    client, _, _, _, _ = make_client(tmp_path)

    rejected = client.post(
        "/api/knowledge-update",
        json={"agent": "Bad", "title": "x", "content": "body", "source": "manual", "tags": ""},
    )
    gaps = client.get("/api/knowledge-gap/persistent", params={"min_count": 5})

    assert rejected.json() == {"status": "rejected", "reason": "unsupported"}
    assert gaps.json() == {
        "status": "ok",
        "min_count": 5,
        "total": 1,
        "gaps": [{"query": "gap", "count": 5, "agent": "건축"}],
    }


def test_knowledge_operations_router_stats_and_integrated_registration(tmp_path: Path):
    client, _, _, _, _ = make_client(tmp_path)
    log_dir = tmp_path / "logs"
    log_dir.mkdir()
    (log_dir / "hourly_ax_signal_monitor.log").write_text("source_docs=2 nodes=3 edges=4\n", encoding="utf-8")

    stats = client.get("/api/knowledge-stats")

    assert stats.json() == {"status": "ok", "source_docs": 2, "nodes": 3, "edges": 4}

    import backend.server_total as server

    paths = {route.path for route in server.app.routes}
    assert "/api/knowledge-update" in paths
    assert "/api/knowledge-gap/persistent" in paths
