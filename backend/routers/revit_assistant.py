from __future__ import annotations

from collections.abc import Callable

from fastapi import APIRouter


def create_revit_assistant_router(
    *,
    chat_handler: Callable,
    feedback_handler: Callable,
    health_handler: Callable,
) -> APIRouter:
    router = APIRouter(tags=["revit-assistant"])
    router.add_api_route("/api/revit-assistant/chat", chat_handler, methods=["POST"])
    router.add_api_route("/api/luachat", chat_handler, methods=["POST"])
    router.add_api_route("/api/revit-assistant/feedback", feedback_handler, methods=["POST"])
    router.add_api_route("/api/luachat/feedback", feedback_handler, methods=["POST"])
    router.add_api_route("/api/luachat/health", health_handler, methods=["GET"])
    return router
