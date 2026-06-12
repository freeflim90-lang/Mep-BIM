from __future__ import annotations

import copy
import json
from typing import Any, Awaitable, Callable

from fastapi import WebSocket, WebSocketDisconnect


class ConnectionManager:
    def __init__(self) -> None:
        self.active_connections: set[WebSocket] = set()

    async def connect(self, websocket: WebSocket) -> None:
        await websocket.accept()
        self.active_connections.add(websocket)
        print(f"📡 [웹소켓] 대시보드 클라이언트 연결 성공. (총 연결수: {len(self.active_connections)})")

    def disconnect(self, websocket: WebSocket) -> None:
        self.active_connections.discard(websocket)
        print(f"⚠️ [웹소켓] 대시보드 세션 종료. (남은 연결수: {len(self.active_connections)})")

    async def broadcast(self, message: str) -> None:
        stale_connections = []
        for connection in list(self.active_connections):
            try:
                await connection.send_text(message)
            except Exception:
                stale_connections.append(connection)
        for connection in stale_connections:
            self.disconnect(connection)


def build_state_update_payload(*, agent_states: dict[str, dict[str, Any]], current_active_agent: str) -> dict[str, Any]:
    return {
        "type": "STATE_UPDATE",
        "data": copy.deepcopy(agent_states),
        "current": current_active_agent,
        "total_tokens": sum(int(agent.get("tokens", 0)) for agent in agent_states.values()),
    }


def build_decision_log_payload(*, tag: str, message: str) -> dict[str, str]:
    return {
        "type": "DECISION_LOG",
        "tag": tag,
        "message": message,
    }


async def broadcast_json(manager: ConnectionManager, payload: dict[str, Any]) -> None:
    await manager.broadcast(json.dumps(payload, ensure_ascii=False))


async def dashboard_websocket_session(
    *,
    websocket: WebSocket,
    manager: ConnectionManager,
    send_state: Callable[[], Awaitable[Any]],
) -> None:
    await manager.connect(websocket)
    try:
        await send_state()
        while True:
            raw_message = await websocket.receive_text()
            if not raw_message:
                continue
            try:
                command = json.loads(raw_message)
            except json.JSONDecodeError:
                continue
            if command.get("type") == "PING":
                await websocket.send_text(json.dumps({"type": "PONG"}, ensure_ascii=False))
    except WebSocketDisconnect:
        manager.disconnect(websocket)
    except Exception as exc:
        print(f"⚠️ [웹소켓] 예외 종료: {exc}")
        manager.disconnect(websocket)
