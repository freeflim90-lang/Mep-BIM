import datetime as dt
from pathlib import Path

from backend.revit_assistant_service import (
    RevitAssistantMetrics,
    apply_revit_feedback_to_text,
    build_revit_chat_response,
    build_revit_error_response,
    build_revit_partial_chat_response,
    build_search_assisted_knowledge_candidate,
    compose_revit_assistant_answer,
    fallback_revit_note_title,
    finalize_revit_assistant_chat,
    luachat_health_payload,
    mark_revit_assistant_idle,
    mark_revit_assistant_processing,
    persist_revit_knowledge_side_effects,
    resolve_knowledge_candidate_agent,
    serialize_revit_sources,
    source_tag_for_revit_answer,
    update_revit_feedback_note,
    write_revit_qa_fallback_note,
    write_luachat_metrics_daily_snapshot,
)


def test_serialize_revit_sources_prefers_relative_project_paths(tmp_path: Path):
    project_root = tmp_path
    inside = project_root / "data" / "knowledge_base" / "Revit_Addin.md"
    outside = Path("/tmp/outside.md")

    rows = serialize_revit_sources(
        [
            {"path": inside, "score": 90},
            {"path": outside, "score": 42},
            {"path": "plain.md"},
        ],
        project_root=project_root,
    )

    assert rows == [
        {"path": "data/knowledge_base/Revit_Addin.md", "score": 90},
        {"path": "/tmp/outside.md", "score": 42},
        {"path": "plain.md", "score": 0},
    ]


def test_build_revit_chat_response_uses_serialized_sources_and_needs_more(tmp_path: Path):
    note_path = tmp_path / "obsidian_vaults" / "qa.md"

    payload = build_revit_chat_response(
        agent="Revit_Addin",
        answer="answer",
        matches=[{"path": tmp_path / "data" / "a.md", "score": 50}],
        search_result="",
        note_path=note_path,
        project_root=tmp_path,
    )

    assert payload["status"] == "ok"
    assert payload["brand"] == "LUA BIM LABS"
    assert payload["agent"] == "Revit_Addin"
    assert payload["sources"] == [{"path": "data/a.md", "score": 50}]
    assert payload["note_path"] == "obsidian_vaults/qa.md"
    assert payload["needs_more"] is False

    empty_payload = build_revit_chat_response(
        agent="Revit_Addin",
        answer="answer",
        matches=[],
        search_result="",
        note_path=note_path,
        project_root=tmp_path,
    )
    assert empty_payload["needs_more"] is True


def test_build_revit_error_response_sanitizes_reason_and_preserves_contract():
    payload = build_revit_error_response(
        stage="answer_generation",
        exc=RuntimeError("bad <secret>"),
        sanitizer=lambda value: value.replace("<", "[").replace(">", "]"),
        agent="Revit_Addin",
    )

    assert payload == {
        "status": "error",
        "brand": "LUA BIM LABS",
        "agent": "Revit_Addin",
        "stage": "answer_generation",
        "reason": "bad [secret]",
        "answer": "",
        "sources": [],
        "needs_more": True,
    }


def test_build_revit_partial_chat_response_preserves_answer_and_warning(tmp_path: Path):
    payload = build_revit_partial_chat_response(
        agent="Revit_Addin",
        answer="[source]\n\nanswer",
        matches=[{"path": tmp_path / "kb.md", "score": 80}],
        search_result="",
        project_root=tmp_path,
        warning_stage="note_persistence",
        warning=OSError("vault <offline>"),
        sanitizer=lambda value: value.replace("<", "[").replace(">", "]"),
    )

    assert payload["status"] == "partial"
    assert payload["answer"] == "[source]\n\nanswer"
    assert payload["sources"] == [{"path": "kb.md", "score": 80}]
    assert payload["note_path"] is None
    assert payload["warning_stage"] == "note_persistence"
    assert payload["warning"] == "vault [offline]"


def test_luachat_health_payload_is_stable_contract(tmp_path: Path):
    payload = luachat_health_payload(
        obsidian_vault=tmp_path / "obsidian_vaults" / "lua_bim_lab_global_map",
        project_root=tmp_path,
        token_required=True,
        search_providers={"duckduckgo": True},
        metrics={"chat_total": 1},
    )

    assert payload["status"] == "ok"
    assert payload["chat_endpoint"] == "/api/luachat"
    assert payload["feedback_endpoint"] == "/api/luachat/feedback"
    assert payload["obsidian_vault"] == "obsidian_vaults/lua_bim_lab_global_map"
    assert payload["token_required"] is True
    assert payload["search_providers"] == {"duckduckgo": True}
    assert payload["metrics"] == {"chat_total": 1}
    assert "metrics_snapshot_path" not in payload


def test_revit_assistant_metrics_tracks_success_feedback_and_error_stages():
    metrics = RevitAssistantMetrics()

    metrics.record_chat_success(search_result="")
    metrics.record_chat_success(search_result="web")
    metrics.record_chat_error("answer_generation")
    metrics.record_chat_error("answer_generation")
    metrics.record_feedback("ignored")
    metrics.record_feedback("updated")

    assert metrics.snapshot() == {
        "chat_total": 4,
        "chat_success": 2,
        "chat_local": 1,
        "chat_search_assisted": 1,
        "feedback_total": 2,
        "feedback_updated": 1,
        "error_total": 2,
        "error_stages": {"answer_generation": 2},
    }


def test_write_luachat_metrics_daily_snapshot_upserts_current_day(tmp_path: Path):
    path = tmp_path / "runtime" / "luachat_metrics_daily.json"

    first = write_luachat_metrics_daily_snapshot(
        path=path,
        metrics={"chat_total": 1},
        now=dt.datetime(2026, 6, 12, 9, 0, 0),
    )
    second = write_luachat_metrics_daily_snapshot(
        path=path,
        metrics={"chat_total": 2},
        now=dt.datetime(2026, 6, 12, 10, 0, 0),
    )

    assert first["date"] == "2026-06-12"
    assert second["metrics"] == {"chat_total": 2}
    text = path.read_text(encoding="utf-8")
    assert '"latest_date": "2026-06-12"' in text
    assert '"chat_total": 2' in text


def test_mark_revit_assistant_processing_and_idle_updates_agent_states():
    states: dict[str, dict] = {}

    def ensure(agent: str) -> None:
        states.setdefault(agent, {"status": "Idle", "tokens": 0, "message": ""})

    mark_revit_assistant_processing(
        agent_states=states,
        agent="Revit_Addin",
        message="A" * 80,
        ensure_agent_state=ensure,
    )

    assert states["Revit_Addin"]["status"] == "Active"
    assert states["Revit_Addin"]["tokens"] == 1
    assert len(states["Revit_Addin"]["message"]) < 90
    assert states["지식업데이트"]["message"] == "Revit Assistant Q&A를 Obsidian 지식 루프에 기록했습니다."

    mark_revit_assistant_idle(
        agent_states=states,
        agent="Revit_Addin",
        ensure_agent_state=ensure,
    )
    assert states["Revit_Addin"]["status"] == "Idle"


def test_finalize_revit_assistant_chat_saves_updates_state_and_returns_payload(tmp_path: Path):
    import asyncio
    from types import SimpleNamespace

    states: dict[str, dict] = {}
    sent = []
    launched = []

    def ensure(agent: str) -> None:
        states.setdefault(agent, {"status": "Idle", "tokens": 0, "message": ""})

    def save_note(**kwargs):
        assert kwargs["agent"] == "Revit_Addin"
        return tmp_path / "obsidian" / "qa.md"

    async def send_state():
        sent.append("sent")

    async def refresh():
        launched.append("refresh-ran")

    def launch(coro):
        coro.close()
        launched.append("scheduled")

    payload = asyncio.run(finalize_revit_assistant_chat(
        request=SimpleNamespace(message="뷰 템플릿 복사 기준 알려줘"),
        answer="[source]\n\nanswer",
        agent="Revit_Addin",
        matches=[{"path": tmp_path / "kb.md", "score": 77}],
        search_result="",
        source_tag="📚 지식 베이스 (score 77)",
        top_score=77,
        project_root=tmp_path,
        agent_states=states,
        ensure_agent_state=ensure,
        save_note=save_note,
        send_state=send_state,
        refresh_knowledge=refresh,
        launch_background_task=launch,
    ))

    assert sent == ["sent", "sent"]
    assert launched == ["scheduled"]
    assert states["Revit_Addin"]["status"] == "Idle"
    assert states["Revit_Addin"]["tokens"] == 1
    assert payload["note_path"] == "obsidian/qa.md"
    assert payload["note_archive_mode"] == "obsidian"
    assert payload["sources"] == [{"path": "kb.md", "score": 77}]


def test_finalize_revit_assistant_chat_uses_runtime_fallback_when_obsidian_save_fails(tmp_path: Path):
    import asyncio
    from types import SimpleNamespace

    states: dict[str, dict] = {}
    sent = []
    fallback_dir = tmp_path / "runtime" / "revit_assistant_qa_fallback"

    def ensure(agent: str) -> None:
        states.setdefault(agent, {"status": "Idle", "tokens": 0, "message": ""})

    def fail_save(**kwargs):
        raise OSError("obsidian unavailable")

    async def send_state():
        sent.append("sent")

    async def refresh():
        return None

    def launch(coro):
        coro.close()

    payload = asyncio.run(finalize_revit_assistant_chat(
        request=SimpleNamespace(
            message="덕트 사이즈 검토",
            user_id="tester",
            client_version="test-client",
            revit_context="duct context",
        ),
        answer="[source]\n\nfallback answer",
        agent="Revit_Addin",
        matches=[],
        search_result="",
        source_tag="📚 지식 베이스 (score 77)",
        top_score=77,
        project_root=tmp_path,
        agent_states=states,
        ensure_agent_state=ensure,
        save_note=fail_save,
        send_state=send_state,
        refresh_knowledge=refresh,
        launch_background_task=launch,
        fallback_note_dir=fallback_dir,
    ))

    fallback_path = tmp_path / payload["note_path"]
    assert payload["status"] == "ok"
    assert payload["note_archive_mode"] == "fallback"
    assert fallback_path.exists()
    assert "obsidian unavailable" in fallback_path.read_text(encoding="utf-8")
    assert sent == ["sent", "sent"]


def test_write_revit_qa_fallback_note_sanitizes_title_and_preserves_context(tmp_path: Path):
    from types import SimpleNamespace

    now = dt.datetime(2026, 6, 12, 12, 30, 0)
    title = fallback_revit_note_title("덕트? 사이즈/검토", now=now)
    path = write_revit_qa_fallback_note(
        fallback_dir=tmp_path,
        request=SimpleNamespace(
            message="덕트? 사이즈/검토",
            user_id="tester",
            client_version="1.0",
            revit_context="context",
        ),
        answer="answer",
        agent="Revit_Addin",
        search_result="search",
        source_tag="source",
        top_score=10,
        primary_error=OSError("primary failed"),
        now=now,
    )

    assert title == "QA-FALLBACK-20260612-123000-덕트_사이즈_검토.md"
    assert path.name == title
    text = path.read_text(encoding="utf-8")
    assert "fallback-archive-needs-obsidian-replay" in text
    assert "primary failed" in text
    assert "context" in text


def test_apply_revit_feedback_to_text_updates_status_and_appends_block():
    text = "status: answered-pending-feedback\n# Note\n"

    updated = apply_revit_feedback_to_text(
        text,
        user_id="tester",
        feedback="needs <review>",
        is_good=False,
        now=dt.datetime(2026, 6, 12, 9, 30, 0),
        sanitizer=lambda value: value.replace("<", "[").replace(">", "]"),
    )

    assert updated.startswith("status: knowledge-gap-needs-review")
    assert "2026-06-12 09:30:00" in updated
    assert "- User: tester" in updated
    assert "- Result: needs-review" in updated
    assert "needs [review]" in updated


def test_update_revit_feedback_note_writes_file_and_schedules_refresh(tmp_path: Path):
    note_path = tmp_path / "qa.md"
    note_path.write_text("status: answered-pending-feedback\n# QA\n", encoding="utf-8")
    rebuilt = []
    launched = []

    async def refresh():
        launched.append("refresh-ran")

    def launch(coro):
        coro.close()
        launched.append("scheduled")

    result = update_revit_feedback_note(
        note_path=note_path,
        note_path_label="obsidian/qa.md",
        user_id="tester",
        feedback="좋아요",
        is_good=True,
        now=dt.datetime(2026, 6, 12, 10, 0, 0),
        sanitizer=lambda value: value,
        rebuild_revit_qa_moc=lambda: rebuilt.append("rebuilt"),
        refresh_knowledge=refresh,
        launch_background_task=launch,
    )

    assert result == {"status": "updated", "note_path": "obsidian/qa.md"}
    assert rebuilt == ["rebuilt"]
    assert launched == ["scheduled"]
    assert "status: answered-good" in note_path.read_text(encoding="utf-8")


def test_source_tag_for_revit_answer_covers_local_web_and_empty_cases():
    assert source_tag_for_revit_answer(matches=[{"score": 80}], top_score=80, search_result="") == "📚 지식 베이스 (score 80)"
    assert source_tag_for_revit_answer(matches=[{"score": 15}], top_score=15, search_result="web") == "📚 지식 베이스 (score 15) + 🔍 웹 검색 보강"
    assert source_tag_for_revit_answer(matches=[{"score": 15}], top_score=15, search_result="") == "📚 지식 베이스 (score 15)"
    assert source_tag_for_revit_answer(matches=[], top_score=0, search_result="web") == "🔍 웹 검색"
    assert source_tag_for_revit_answer(matches=[], top_score=0, search_result="") == "❓ 지식 없음 — 지식 베이스 보강 필요"


def test_resolve_knowledge_candidate_agent_avoids_operational_agents():
    agents = {"건축", "Revit_Addin", "지식업데이트", "지식큐레이터"}

    assert resolve_knowledge_candidate_agent(
        agent="Revit_Addin",
        query="query",
        knowledge_agents=agents,
        infer_agent=lambda query: "건축",
    ) == "Revit_Addin"
    assert resolve_knowledge_candidate_agent(
        agent="지식업데이트",
        query="query",
        knowledge_agents=agents,
        infer_agent=lambda query: "지식큐레이터",
    ) == "건축"


def test_build_search_assisted_knowledge_candidate_requires_useful_search_and_answer():
    agents = {"건축", "Revit_Addin"}

    candidate = build_search_assisted_knowledge_candidate(
        agent="Revit_Addin",
        query="query",
        question="뷰 템플릿 복사 기준 알려줘",
        answer="충분히 긴 검색 보강 답변입니다. 지식 후보로 저장할 수 있습니다.",
        search_result="search evidence",
        knowledge_agents=agents,
        infer_agent=lambda query: "건축",
        sanitizer=lambda value: value.replace("<", "[").replace(">", "]"),
    )

    assert candidate is not None
    assert candidate["agent"] == "Revit_Addin"
    assert candidate["source"] == "search-assisted-qa"
    assert "needs-review" in candidate["tags"]
    assert "뷰 템플릿 복사 기준" in candidate["content"]
    assert "search evidence" in candidate["content"]

    assert build_search_assisted_knowledge_candidate(
        agent="Revit_Addin",
        query="query",
        question="q",
        answer="short",
        search_result="search evidence",
        knowledge_agents=agents,
        infer_agent=lambda query: "건축",
        sanitizer=lambda value: value,
    ) is None


def test_persist_revit_knowledge_side_effects_records_candidate_and_gap_log():
    updates = []
    gap_logs = []

    def update_factory(**kwargs):
        return {"model": kwargs}

    persist_revit_knowledge_side_effects(
        knowledge_candidate={
            "agent": "Revit_Addin",
            "title": "Q: question",
            "source": "search-assisted-qa",
            "tags": "qa",
            "content": "candidate content",
        },
        search_result="search evidence",
        query="context query",
        agent="Revit_Addin",
        top_score=12,
        append_knowledge_update=updates.append,
        knowledge_update_factory=update_factory,
        append_gap_log=lambda **kwargs: gap_logs.append(kwargs),
    )

    assert updates == [
        {
            "model": {
                "agent": "Revit_Addin",
                "title": "Q: question",
                "source": "search-assisted-qa",
                "tags": "qa",
                "content": "candidate content",
            }
        }
    ]
    assert gap_logs == [
        {
            "query": "context query",
            "agent": "Revit_Addin",
            "assessment": {"reasons": [], "top_score": 12, "top_path": ""},
            "search_result": "search evidence",
        }
    ]


def test_persist_revit_knowledge_side_effects_skips_empty_payloads():
    updates = []
    gap_logs = []

    persist_revit_knowledge_side_effects(
        knowledge_candidate=None,
        search_result="",
        query="context query",
        agent="Revit_Addin",
        top_score=0,
        append_knowledge_update=updates.append,
        knowledge_update_factory=lambda **kwargs: kwargs,
        append_gap_log=lambda **kwargs: gap_logs.append(kwargs),
    )

    assert updates == []
    assert gap_logs == []


def test_compose_revit_assistant_answer_uses_local_answer_when_score_is_high():
    async def fail_search(agent: str, query: str) -> str:
        raise AssertionError("search should be skipped for strong local matches")

    async def synthesize(query: str, context: str) -> str:
        raise AssertionError("synthesis should be skipped for strong local matches")

    import asyncio

    result = asyncio.run(compose_revit_assistant_answer(
        query="query",
        question="question",
        agent="Revit_Addin",
        matches=[{"score": 80}],
        top_score=80,
        knowledge_agents={"Revit_Addin"},
        build_local_answer=lambda query, matches, agent: "local answer",
        search_web=fail_search,
        build_context=lambda query, search, matches: "context",
        synthesize=synthesize,
        enforce_answer=lambda answer, fallback: answer,
        infer_agent=lambda query: "Revit_Addin",
        sanitizer=lambda value: value,
    ))

    assert result["answer"] == "local answer"
    assert result["source_tag"] == "📚 지식 베이스 (score 80)"
    assert result["search_result"] == ""
    assert result["knowledge_candidate"] is None


def test_compose_revit_assistant_answer_uses_search_and_candidate_when_local_is_weak():
    async def search(agent: str, query: str) -> str:
        return "search evidence"

    async def synthesize(query: str, context: str) -> str:
        return "검색으로 보강한 충분히 긴 답변입니다. 후보 지식으로 저장됩니다."

    import asyncio

    result = asyncio.run(compose_revit_assistant_answer(
        query="query",
        question="question",
        agent="Revit_Addin",
        matches=[{"score": 12}],
        top_score=12,
        knowledge_agents={"Revit_Addin", "건축"},
        build_local_answer=lambda query, matches, agent: "local",
        search_web=search,
        build_context=lambda query, search, matches: f"context {search}",
        synthesize=synthesize,
        enforce_answer=lambda answer, fallback: answer,
        infer_agent=lambda query: "건축",
        sanitizer=lambda value: value,
    ))

    assert result["search_result"] == "search evidence"
    assert result["source_tag"] == "📚 지식 베이스 (score 12) + 🔍 웹 검색 보강"
    assert result["knowledge_candidate"]["agent"] == "Revit_Addin"
