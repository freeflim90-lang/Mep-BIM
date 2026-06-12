from fastapi.testclient import TestClient

import backend.server_total as server


def test_luachat_health_reports_operational_contract(monkeypatch):
    monkeypatch.setenv("LUA_CHAT_TOKEN", "test-token")
    metrics = server.RevitAssistantMetrics()
    metrics.record_chat_success(search_result="web")
    monkeypatch.setattr(server, "revit_assistant_metrics", metrics)
    client = TestClient(server.app)

    response = client.get("/api/luachat/health")

    assert response.status_code == 200
    payload = response.json()
    assert payload["status"] == "ok"
    assert payload["chat_endpoint"] == "/api/luachat"
    assert payload["feedback_endpoint"] == "/api/luachat/feedback"
    assert payload["token_required"] is True
    assert payload["metrics"]["chat_total"] == 1
    assert payload["metrics"]["chat_search_assisted"] == 1
    assert payload["metrics_snapshot_path"] == "runtime/luachat_metrics_daily.json"


def test_luachat_feedback_rejects_wrong_token(monkeypatch):
    monkeypatch.setenv("LUA_CHAT_TOKEN", "test-token")
    monkeypatch.setenv("REVIT_ASSISTANT_API_KEYS", "")
    client = TestClient(server.app)

    response = client.post(
        "/api/luachat/feedback",
        headers={"Authorization": "Bearer wrong-token"},
        json={
            "user_id": "tester",
            "message": "question",
            "answer": "answer",
            "is_good": True,
            "note_path": "obsidian_vaults/lua_bim_lab_global_map/NAS_Knowledge/Revit_Assistant_QA/sample.md",
            "feedback": "ok",
        },
    )

    assert response.status_code == 401


def test_luachat_feedback_ignores_path_outside_revit_qa(monkeypatch):
    monkeypatch.setenv("LUA_CHAT_TOKEN", "test-token")
    monkeypatch.setenv("REVIT_ASSISTANT_API_KEYS", "")
    client = TestClient(server.app)

    response = client.post(
        "/api/luachat/feedback",
        headers={"Authorization": "Bearer test-token"},
        json={
            "user_id": "tester",
            "message": "question",
            "answer": "answer",
            "is_good": False,
            "note_path": "../README.md",
            "feedback": "needs work",
        },
    )

    assert response.status_code == 200
    assert response.json() == {"status": "ignored", "reason": "note_path not found"}


def test_luachat_feedback_updates_revit_qa_note(monkeypatch, tmp_path):
    monkeypatch.setenv("LUA_CHAT_TOKEN", "test-token")
    monkeypatch.setenv("REVIT_ASSISTANT_API_KEYS", "")
    project_root = tmp_path
    qa_dir = project_root / "obsidian_vaults" / "lua_bim_lab_global_map" / "NAS_Knowledge" / "Revit_Assistant_QA"
    qa_dir.mkdir(parents=True)
    note_path = qa_dir / "sample.md"
    note_path.write_text("status: answered-pending-feedback\n# Sample\n", encoding="utf-8")
    relative_note = "obsidian_vaults/lua_bim_lab_global_map/NAS_Knowledge/Revit_Assistant_QA/sample.md"
    rebuilt = []
    launched = []

    async def noop_refresh():
        return None

    def launch(coro):
        coro.close()
        launched.append("scheduled")

    monkeypatch.setattr(server, "PROJECT_ROOT", project_root)
    monkeypatch.setattr(server, "REVIT_QA_OBSIDIAN_DIR", qa_dir)
    monkeypatch.setattr(server, "rebuild_revit_qa_moc", lambda: rebuilt.append("rebuilt"))
    monkeypatch.setattr(server, "refresh_obsidian_after_knowledge_update", noop_refresh)
    monkeypatch.setattr(server, "launch_background_task", launch)
    metrics = server.RevitAssistantMetrics()
    monkeypatch.setattr(server, "revit_assistant_metrics", metrics)

    client = TestClient(server.app)
    response = client.post(
        "/api/luachat/feedback",
        headers={"Authorization": "Bearer test-token"},
        json={
            "user_id": "tester",
            "message": "question",
            "answer": "answer",
            "is_good": True,
            "note_path": relative_note,
            "feedback": "확인 완료",
        },
    )

    assert response.status_code == 200
    assert response.json() == {"status": "updated", "note_path": relative_note}
    assert rebuilt == ["rebuilt"]
    assert launched == ["scheduled"]
    updated = note_path.read_text(encoding="utf-8")
    assert "status: answered-good" in updated
    assert "- User: tester" in updated
    assert "확인 완료" in updated
    assert metrics.snapshot()["feedback_updated"] == 1


def test_luachat_chat_success_uses_local_knowledge(monkeypatch, tmp_path):
    monkeypatch.setenv("LUA_CHAT_TOKEN", "test-token")
    monkeypatch.setenv("REVIT_ASSISTANT_API_KEYS", "")
    monkeypatch.setattr(server, "build_revit_context_prompt", lambda message, context: f"{message}\n{context}".strip())
    monkeypatch.setattr(server, "infer_knowledge_agent_from_query", lambda query: "Revit_Addin")
    monkeypatch.setattr(
        server,
        "search_local_knowledge",
        lambda query, limit=5: [{"path": tmp_path / "revit.md", "score": 88, "preview": "local"}],
    )
    monkeypatch.setattr(server, "prioritize_agent_matches", lambda matches, agent: matches)
    monkeypatch.setattr(server, "build_revit_assistant_answer", lambda query, matches, agent: "로컬 지식 기반 답변")
    monkeypatch.setattr(server, "save_revit_qa_to_obsidian", lambda **kwargs: server.PROJECT_ROOT / "obsidian_vaults/lua_bim_lab_global_map/NAS_Knowledge/Revit_Assistant_QA/test.md")

    async def noop_send_state():
        return None

    async def noop_refresh():
        return None

    monkeypatch.setattr(server, "send_state_to_dashboard", noop_send_state)
    monkeypatch.setattr(server, "refresh_obsidian_after_knowledge_update", noop_refresh)
    monkeypatch.setattr(server, "launch_background_task", lambda coro: coro.close())
    metrics = server.RevitAssistantMetrics()
    monkeypatch.setattr(server, "revit_assistant_metrics", metrics)
    metrics_file = tmp_path / "runtime" / "luachat_metrics_daily.json"
    monkeypatch.setattr(server, "LUACHAT_METRICS_DAILY_FILE", metrics_file)

    client = TestClient(server.app)
    response = client.post(
        "/api/luachat",
        headers={"Authorization": "Bearer test-token"},
        json={
            "user_id": "tester",
            "message": "뷰 템플릿 복사 기준 알려줘",
            "revit_context": "Revit 2026",
        },
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["status"] == "ok"
    assert payload["agent"] == "Revit_Addin"
    assert payload["needs_more"] is False
    assert "로컬 지식 기반 답변" in payload["answer"]
    assert payload["sources"] == [{"path": str((tmp_path / "revit.md")), "score": 88}]
    assert metrics.snapshot()["chat_local"] == 1
    assert '"chat_local": 1' in metrics_file.read_text(encoding="utf-8")


def test_luachat_chat_search_assisted_answer_persists_candidate_and_gap_log(monkeypatch, tmp_path):
    monkeypatch.setenv("LUA_CHAT_TOKEN", "test-token")
    monkeypatch.setenv("REVIT_ASSISTANT_API_KEYS", "")
    monkeypatch.setattr(server, "build_revit_context_prompt", lambda message, context: f"{message}\n{context}".strip())
    monkeypatch.setattr(server, "infer_knowledge_agent_from_query", lambda query: "Revit_Addin")
    monkeypatch.setattr(
        server,
        "search_local_knowledge",
        lambda query, limit=5: [{"path": tmp_path / "weak.md", "score": 12, "preview": "weak local"}],
    )
    monkeypatch.setattr(server, "prioritize_agent_matches", lambda matches, agent: matches)
    monkeypatch.setattr(server, "build_combined_answer", lambda query, search, matches: f"context: {search}")

    async def search_web(agent: str, query: str) -> str:
        return "검색 근거: Revit 뷰 템플릿 복사는 대상 프로젝트 표준과 충돌 여부를 먼저 검토합니다."

    async def synthesize(query: str, context: str) -> str:
        return "검색으로 보강한 충분히 긴 한국어 답변입니다. 표준 템플릿 충돌을 먼저 확인하고 dry-run으로 검토합니다."

    async def noop_send_state():
        return None

    async def noop_refresh():
        return None

    updates = []
    gap_logs = []
    monkeypatch.setattr(server, "_search_web_for_knowledge", search_web)
    monkeypatch.setattr(server, "_synthesize_with_qwen", synthesize)
    metrics = server.RevitAssistantMetrics()
    monkeypatch.setattr(server, "revit_assistant_metrics", metrics)
    monkeypatch.setattr(server, "append_knowledge_update", lambda update: updates.append(update))
    monkeypatch.setattr(server, "append_auto_knowledge_gap_log", lambda **kwargs: gap_logs.append(kwargs))
    monkeypatch.setattr(
        server,
        "save_revit_qa_to_obsidian",
        lambda **kwargs: server.PROJECT_ROOT / "obsidian_vaults/lua_bim_lab_global_map/NAS_Knowledge/Revit_Assistant_QA/search.md",
    )
    monkeypatch.setattr(server, "send_state_to_dashboard", noop_send_state)
    monkeypatch.setattr(server, "refresh_obsidian_after_knowledge_update", noop_refresh)
    monkeypatch.setattr(server, "launch_background_task", lambda coro: coro.close())
    metrics = server.RevitAssistantMetrics()
    monkeypatch.setattr(server, "revit_assistant_metrics", metrics)

    client = TestClient(server.app)
    response = client.post(
        "/api/luachat",
        headers={"Authorization": "Bearer test-token"},
        json={
            "user_id": "tester",
            "message": "뷰 템플릿 복사 전에 어떤 기준으로 확인해야 해?",
            "revit_context": "Revit 2026",
        },
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["status"] == "ok"
    assert payload["agent"] == "Revit_Addin"
    assert payload["needs_more"] is False
    assert "웹 검색 보강" in payload["answer"]
    assert "검색으로 보강한 충분히 긴 한국어 답변" in payload["answer"]
    assert len(updates) == 1
    assert updates[0].agent == "Revit_Addin"
    assert updates[0].source == "search-assisted-qa"
    assert "needs-review" in updates[0].content
    assert len(gap_logs) == 1
    assert gap_logs[0]["agent"] == "Revit_Addin"
    assert gap_logs[0]["assessment"]["top_score"] == 12
    assert "검색 근거" in gap_logs[0]["search_result"]
    assert metrics.snapshot()["chat_search_assisted"] == 1


def test_luachat_chat_returns_error_when_search_fails(monkeypatch, tmp_path):
    monkeypatch.setenv("LUA_CHAT_TOKEN", "test-token")
    monkeypatch.setenv("REVIT_ASSISTANT_API_KEYS", "")
    monkeypatch.setattr(server, "build_revit_context_prompt", lambda message, context: message)
    monkeypatch.setattr(server, "infer_knowledge_agent_from_query", lambda query: "Revit_Addin")
    monkeypatch.setattr(
        server,
        "search_local_knowledge",
        lambda query, limit=5: [{"path": tmp_path / "weak.md", "score": 5}],
    )
    monkeypatch.setattr(server, "prioritize_agent_matches", lambda matches, agent: matches)

    async def search_web(agent: str, query: str) -> str:
        raise RuntimeError("search provider timeout")

    monkeypatch.setattr(server, "_search_web_for_knowledge", search_web)
    metrics = server.RevitAssistantMetrics()
    monkeypatch.setattr(server, "revit_assistant_metrics", metrics)

    client = TestClient(server.app)
    response = client.post(
        "/api/luachat",
        headers={"Authorization": "Bearer test-token"},
        json={"user_id": "tester", "message": "검색 실패 테스트"},
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["status"] == "error"
    assert payload["agent"] == "Revit_Addin"
    assert payload["stage"] == "answer_generation"
    assert "search provider timeout" in payload["reason"]
    assert payload["needs_more"] is True
    assert metrics.snapshot()["error_stages"] == {"answer_generation": 1}


def test_luachat_chat_returns_error_when_synthesis_fails(monkeypatch, tmp_path):
    monkeypatch.setenv("LUA_CHAT_TOKEN", "test-token")
    monkeypatch.setenv("REVIT_ASSISTANT_API_KEYS", "")
    monkeypatch.setattr(server, "build_revit_context_prompt", lambda message, context: message)
    monkeypatch.setattr(server, "infer_knowledge_agent_from_query", lambda query: "Revit_Addin")
    monkeypatch.setattr(
        server,
        "search_local_knowledge",
        lambda query, limit=5: [{"path": tmp_path / "weak.md", "score": 5}],
    )
    monkeypatch.setattr(server, "prioritize_agent_matches", lambda matches, agent: matches)
    monkeypatch.setattr(server, "build_combined_answer", lambda query, search, matches: search)

    async def search_web(agent: str, query: str) -> str:
        return "search evidence"

    async def synthesize(query: str, context: str) -> str:
        raise RuntimeError("synthesis unavailable")

    monkeypatch.setattr(server, "_search_web_for_knowledge", search_web)
    monkeypatch.setattr(server, "_synthesize_with_qwen", synthesize)
    metrics = server.RevitAssistantMetrics()
    monkeypatch.setattr(server, "revit_assistant_metrics", metrics)

    client = TestClient(server.app)
    response = client.post(
        "/api/luachat",
        headers={"Authorization": "Bearer test-token"},
        json={"user_id": "tester", "message": "합성 실패 테스트"},
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["status"] == "error"
    assert payload["stage"] == "answer_generation"
    assert "synthesis unavailable" in payload["reason"]
    assert metrics.snapshot()["error_stages"] == {"answer_generation": 1}


def test_luachat_chat_uses_fallback_archive_when_note_persistence_fails(monkeypatch, tmp_path):
    monkeypatch.setenv("LUA_CHAT_TOKEN", "test-token")
    monkeypatch.setenv("REVIT_ASSISTANT_API_KEYS", "")
    monkeypatch.setattr(server, "build_revit_context_prompt", lambda message, context: message)
    monkeypatch.setattr(server, "infer_knowledge_agent_from_query", lambda query: "Revit_Addin")
    monkeypatch.setattr(
        server,
        "search_local_knowledge",
        lambda query, limit=5: [{"path": tmp_path / "strong.md", "score": 88}],
    )
    monkeypatch.setattr(server, "prioritize_agent_matches", lambda matches, agent: matches)
    monkeypatch.setattr(server, "build_revit_assistant_answer", lambda query, matches, agent: "로컬 지식 기반 답변")

    def fail_save(**kwargs):
        raise OSError("obsidian vault unavailable")

    monkeypatch.setattr(server, "save_revit_qa_to_obsidian", fail_save)
    monkeypatch.setattr(server, "PROJECT_ROOT", tmp_path)
    metrics = server.RevitAssistantMetrics()
    monkeypatch.setattr(server, "revit_assistant_metrics", metrics)

    client = TestClient(server.app)
    response = client.post(
        "/api/luachat",
        headers={"Authorization": "Bearer test-token"},
        json={"user_id": "tester", "message": "노트 저장 실패 테스트"},
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["status"] == "ok"
    assert payload["agent"] == "Revit_Addin"
    assert "로컬 지식 기반 답변" in payload["answer"]
    assert payload["note_archive_mode"] == "fallback"
    fallback_note = tmp_path / payload["note_path"]
    assert fallback_note.exists()
    assert "obsidian vault unavailable" in fallback_note.read_text(encoding="utf-8")
    assert metrics.snapshot()["chat_success"] == 1
    assert metrics.snapshot()["error_stages"] == {}


def test_visitor_count_endpoint_records_once_per_forwarded_ip(monkeypatch, tmp_path):
    counter = server.VisitorCounter(tmp_path / "visitor_count.json")
    monkeypatch.setattr(server, "_visitor_counter", counter)
    client = TestClient(server.app)

    first = client.post("/api/visitor-count", headers={"x-forwarded-for": "10.0.0.1, 10.0.0.2"})
    second = client.post("/api/visitor-count", headers={"x-forwarded-for": "10.0.0.1, 10.0.0.3"})
    current = client.get("/api/visitor-count")

    assert first.json() == {"total": 1}
    assert second.json() == {"total": 1}
    assert current.json() == {"total": 1}
