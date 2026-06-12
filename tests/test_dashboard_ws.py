import json

from fastapi import WebSocketDisconnect

from backend.dashboard_ws import (
    ConnectionManager,
    build_decision_log_payload,
    build_state_update_payload,
    dashboard_websocket_session,
)


class FakeWebSocket:
    def __init__(self, messages=None, *, fail_send=False):
        self.messages = list(messages or [])
        self.fail_send = fail_send
        self.accepted = False
        self.sent = []

    async def accept(self):
        self.accepted = True

    async def send_text(self, message):
        if self.fail_send:
            raise RuntimeError("send failed")
        self.sent.append(message)

    async def receive_text(self):
        if self.messages:
            item = self.messages.pop(0)
            if isinstance(item, BaseException):
                raise item
            return item
        raise WebSocketDisconnect()


def test_build_state_update_payload_deep_copies_and_counts_tokens():
    states = {
        "CEO": {"status": "Idle", "tokens": 2, "message": "ready"},
        "PM": {"status": "Active", "tokens": "3", "message": "work"},
    }

    payload = build_state_update_payload(agent_states=states, current_active_agent="CEO")
    states["CEO"]["tokens"] = 999

    assert payload["type"] == "STATE_UPDATE"
    assert payload["current"] == "CEO"
    assert payload["total_tokens"] == 5
    assert payload["data"]["CEO"]["tokens"] == 2
    assert build_decision_log_payload(tag="route", message="ok") == {
        "type": "DECISION_LOG",
        "tag": "route",
        "message": "ok",
    }


def test_connection_manager_broadcast_removes_stale_connections():
    import asyncio

    manager = ConnectionManager()
    good = FakeWebSocket()
    bad = FakeWebSocket(fail_send=True)

    asyncio.run(manager.connect(good))
    asyncio.run(manager.connect(bad))
    asyncio.run(manager.broadcast("hello"))

    assert good.sent == ["hello"]
    assert good in manager.active_connections
    assert bad not in manager.active_connections


def test_dashboard_websocket_session_sends_state_and_pong_then_disconnects():
    import asyncio

    manager = ConnectionManager()
    websocket = FakeWebSocket([
        "not-json",
        json.dumps({"type": "PING"}),
        WebSocketDisconnect(),
    ])
    sent_state = []

    async def send_state():
        sent_state.append("state")

    asyncio.run(dashboard_websocket_session(websocket=websocket, manager=manager, send_state=send_state))

    assert websocket.accepted is True
    assert sent_state == ["state"]
    assert websocket.sent == [json.dumps({"type": "PONG"}, ensure_ascii=False)]
    assert websocket not in manager.active_connections


def test_integrated_app_registers_dashboard_websocket_routes():
    import backend.server_total as server

    paths = {route.path for route in server.app.routes}

    assert "/ws/office" in paths
    assert "/ws/state" in paths
