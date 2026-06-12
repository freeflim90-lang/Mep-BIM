from __future__ import annotations

import asyncio
from pathlib import Path
from typing import Any, Callable

from fastapi import APIRouter, Request
from fastapi.responses import FileResponse

from backend.visitor_counter import VisitorCounter, client_ip_from_headers

VisitorCounterProvider = VisitorCounter | Callable[[], VisitorCounter]


def _resolve_visitor_counter(provider: VisitorCounterProvider) -> VisitorCounter:
    return provider() if callable(provider) else provider


def build_root_health_payload(
    *,
    agents: list[str],
    telegram_enabled: bool,
    telegram_chat_configured: bool,
    github_configured: bool,
    local_coder_enabled: bool,
) -> dict[str, Any]:
    return {
        "status": "running",
        "service": "LUA BIM LABS integrated backend",
        "agents": agents,
        "telegram_enabled": telegram_enabled,
        "telegram_chat_configured": telegram_chat_configured,
        "github_configured": github_configured,
        "local_coder_enabled": local_coder_enabled,
    }


def build_ai_model_routing_payload(
    *,
    routing: dict[str, Any],
    agent_models: dict[str, Any],
    paid_ai_enabled: bool,
    deepseek_api_configured: bool,
    monthly_budget_remaining_usd: float,
) -> dict[str, Any]:
    return {
        "status": "ok",
        "routing": routing,
        "agent_models": agent_models,
        "paid_ai_enabled": paid_ai_enabled,
        "deepseek_api_configured": deepseek_api_configured,
        "monthly_budget_remaining_usd": monthly_budget_remaining_usd,
    }


def create_operations_status_router(
    *,
    frontend_dir: Path,
    agents: list[str],
    telegram_enabled: Callable[[], bool],
    telegram_chat_configured: Callable[[], bool],
    github_configured: Callable[[], bool],
    local_coder_enabled: Callable[[], bool],
    visitor_counter: VisitorCounterProvider,
    model_routing_status: Callable[[], dict[str, Any]],
    agent_model_map: Callable[[dict[str, Any]], dict[str, Any]],
    paid_ai_enabled: Callable[[], bool],
    deepseek_api_configured: Callable[[], bool],
    deepseek_budget_remaining: Callable[[], float],
) -> APIRouter:
    router = APIRouter(tags=["operations-status"])
    visitor_lock = asyncio.Lock()

    @router.get("/")
    async def health_check():
        return build_root_health_payload(
            agents=agents,
            telegram_enabled=telegram_enabled(),
            telegram_chat_configured=telegram_chat_configured(),
            github_configured=github_configured(),
            local_coder_enabled=local_coder_enabled(),
        )

    @router.get("/dashboard")
    async def dashboard():
        return FileResponse(frontend_dir / "index.html")

    @router.post("/api/visitor-count")
    async def record_visitor(request: Request):
        raw_ip = client_ip_from_headers(
            request.headers,
            fallback=request.client.host if request.client else "unknown",
        )
        async with visitor_lock:
            total = _resolve_visitor_counter(visitor_counter).record(raw_ip)
        return {"total": total}

    @router.get("/api/visitor-count")
    async def get_visitor_count():
        return {"total": _resolve_visitor_counter(visitor_counter).total()}

    @router.get("/api/ai/model-routing")
    async def ai_model_routing():
        routing = model_routing_status()
        return build_ai_model_routing_payload(
            routing=routing,
            agent_models=agent_model_map(routing),
            paid_ai_enabled=paid_ai_enabled(),
            deepseek_api_configured=deepseek_api_configured(),
            monthly_budget_remaining_usd=deepseek_budget_remaining(),
        )

    return router
