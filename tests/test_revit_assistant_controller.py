import datetime as dt
from pathlib import Path
from types import SimpleNamespace

from backend.revit_assistant_controller import (
    RevitAssistantChatDependencies,
    RevitAssistantFeedbackDependencies,
    handle_revit_assistant_chat,
    handle_revit_assistant_feedback,
)
from backend.revit_assistant_service import RevitAssistantMetrics


def test_handle_revit_assistant_chat_runs_success_path(tmp_path: Path):
    import asyncio

    metrics = RevitAssistantMetrics()
    snapshots = []
    sent = []
    states = {}

    async def send_state():
        sent.append("sent")

    async def refresh():
        return None

    def launch(coro):
        coro.close()

    payload = asyncio.run(handle_revit_assistant_chat(
        request=SimpleNamespace(message="로컬 답변 테스트", revit_context={}),
        api_key="token",
        authorization=None,
        deps=RevitAssistantChatDependencies(
            extract_bearer_token=lambda value: value,
            require_api_key=lambda value: None if value == "token" else (_ for _ in ()).throw(AssertionError("bad token")),
            build_context_prompt=lambda message, context: message,
            infer_agent=lambda query: "Revit_Addin",
            search_local_knowledge=lambda query, limit=5: [{"path": tmp_path / "kb.md", "score": 90}],
            prioritize_matches=lambda matches, agent: matches,
            knowledge_agents={"Revit_Addin"},
            build_local_answer=lambda query, matches, agent: "로컬 지식 기반 답변",
            search_web=lambda agent, query: (_ for _ in ()).throw(AssertionError("search skipped")),
            build_context=lambda query, search, matches: "context",
            synthesize=lambda query, context: (_ for _ in ()).throw(AssertionError("synthesis skipped")),
            enforce_answer=lambda text, fallback: text,
            sanitizer=lambda value: value,
            append_knowledge_update=lambda update: None,
            knowledge_update_factory=lambda **kwargs: kwargs,
            append_gap_log=lambda **kwargs: None,
            metrics=metrics,
            save_metrics_snapshot=lambda: snapshots.append(metrics.snapshot()),
            project_root=tmp_path,
            agent_states=states,
            ensure_agent_state=lambda agent: states.setdefault(agent, {"status": "Idle", "tokens": 0, "message": ""}),
            save_note=lambda **kwargs: tmp_path / "qa.md",
            send_state=send_state,
            refresh_knowledge=refresh,
            launch_background_task=launch,
        ),
    ))

    assert payload["status"] == "ok"
    assert payload["agent"] == "Revit_Addin"
    assert "로컬 지식 기반 답변" in payload["answer"]
    assert metrics.snapshot()["chat_local"] == 1
    assert snapshots[-1]["chat_success"] == 1
    assert sent == ["sent", "sent"]


def test_handle_revit_assistant_feedback_records_metrics(tmp_path: Path):
    import asyncio

    metrics = RevitAssistantMetrics()
    snapshots = []
    note_path = tmp_path / "qa.md"

    payload = asyncio.run(handle_revit_assistant_feedback(
        request=SimpleNamespace(note_path="obsidian/qa.md", user_id="tester", feedback="ok", is_good=True),
        api_key=None,
        authorization="Bearer token",
        deps=RevitAssistantFeedbackDependencies(
            extract_bearer_token=lambda value: value.replace("Bearer ", "") if value else None,
            require_api_key=lambda value: None if value == "token" else (_ for _ in ()).throw(AssertionError("bad token")),
            resolve_note_path=lambda label: note_path,
            update_note=lambda **kwargs: {"status": "updated", "note_path": kwargs["note_path_label"]},
            sanitizer=lambda value: value,
            rebuild_revit_qa_moc=lambda: None,
            refresh_knowledge=lambda: (_ for _ in ()).throw(AssertionError("unused by stub")),
            launch_background_task=lambda coro: None,
            metrics=metrics,
            save_metrics_snapshot=lambda: snapshots.append(metrics.snapshot()),
            now=lambda: dt.datetime(2026, 6, 12, 12, 0, 0),
        ),
    ))

    assert payload == {"status": "updated", "note_path": "obsidian/qa.md"}
    assert metrics.snapshot()["feedback_updated"] == 1
    assert snapshots[-1]["feedback_total"] == 1
