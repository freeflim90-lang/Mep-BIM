from __future__ import annotations

from fastapi import FastAPI
from fastapi.testclient import TestClient

from backend.routers.operations_status import (
    build_ai_model_routing_payload,
    build_root_health_payload,
    create_operations_status_router,
)
from backend.visitor_counter import VisitorCounter


def test_build_root_health_payload_exposes_operational_flags():
    payload = build_root_health_payload(
        agents=["CEO", "COO"],
        telegram_enabled=True,
        telegram_chat_configured=False,
        github_configured=True,
        local_coder_enabled=True,
    )

    assert payload["status"] == "running"
    assert payload["service"] == "LUA BIM LABS integrated backend"
    assert payload["agents"] == ["CEO", "COO"]
    assert payload["telegram_enabled"] is True
    assert payload["telegram_chat_configured"] is False
    assert payload["github_configured"] is True
    assert payload["local_coder_enabled"] is True


def test_build_ai_model_routing_payload_preserves_budget_and_agent_models():
    payload = build_ai_model_routing_payload(
        routing={"DeepSeek": {"enabled": True}},
        agent_models={"CEO": "deepseek"},
        paid_ai_enabled=True,
        deepseek_api_configured=False,
        monthly_budget_remaining_usd=42.5,
    )

    assert payload == {
        "status": "ok",
        "routing": {"DeepSeek": {"enabled": True}},
        "agent_models": {"CEO": "deepseek"},
        "paid_ai_enabled": True,
        "deepseek_api_configured": False,
        "monthly_budget_remaining_usd": 42.5,
    }


def test_operations_status_router_serves_health_visitor_and_model_routes(tmp_path):
    app = FastAPI()
    counter = VisitorCounter(tmp_path / "visitor_count.json")
    app.include_router(create_operations_status_router(
        frontend_dir=tmp_path,
        agents=["CEO"],
        telegram_enabled=lambda: False,
        telegram_chat_configured=lambda: True,
        github_configured=lambda: True,
        local_coder_enabled=lambda: False,
        visitor_counter=counter,
        model_routing_status=lambda: {"mode": "local-first"},
        agent_model_map=lambda routing: {"CEO": routing["mode"]},
        paid_ai_enabled=lambda: False,
        deepseek_api_configured=lambda: False,
        deepseek_budget_remaining=lambda: 10.0,
    ))
    client = TestClient(app)

    health = client.get("/")
    first_visit = client.post("/api/visitor-count", headers={"x-forwarded-for": "10.0.0.1, 10.0.0.2"})
    duplicate_visit = client.post("/api/visitor-count", headers={"x-forwarded-for": "10.0.0.1"})
    current_count = client.get("/api/visitor-count")
    routing = client.get("/api/ai/model-routing")

    assert health.status_code == 200
    assert health.json()["agents"] == ["CEO"]
    assert first_visit.json() == {"total": 1}
    assert duplicate_visit.json() == {"total": 1}
    assert current_count.json() == {"total": 1}
    assert routing.json()["agent_models"] == {"CEO": "local-first"}


def test_operations_status_routes_are_registered_in_integrated_app():
    import backend.server_total as server

    paths = {route.path for route in server.app.routes}

    assert "/" in paths
    assert "/dashboard" in paths
    assert "/api/visitor-count" in paths
    assert "/api/ai/model-routing" in paths
