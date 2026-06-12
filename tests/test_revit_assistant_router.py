from fastapi import FastAPI
from fastapi.testclient import TestClient

from backend.routers.revit_assistant import create_revit_assistant_router


async def chat_handler():
    return {"handler": "chat"}


async def feedback_handler():
    return {"handler": "feedback"}


async def health_handler():
    return {"handler": "health"}


def test_revit_assistant_router_registers_public_contract_paths():
    app = FastAPI()
    app.include_router(create_revit_assistant_router(
        chat_handler=chat_handler,
        feedback_handler=feedback_handler,
        health_handler=health_handler,
    ))
    client = TestClient(app)

    assert client.post("/api/luachat").json() == {"handler": "chat"}
    assert client.post("/api/revit-assistant/chat").json() == {"handler": "chat"}
    assert client.post("/api/luachat/feedback").json() == {"handler": "feedback"}
    assert client.post("/api/revit-assistant/feedback").json() == {"handler": "feedback"}
    assert client.get("/api/luachat/health").json() == {"handler": "health"}
