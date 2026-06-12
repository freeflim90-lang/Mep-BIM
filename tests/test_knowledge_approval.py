import datetime as dt

from backend.knowledge_approval import (
    append_knowledge_approval_candidate,
    build_knowledge_approval_candidate,
    find_knowledge_approval_candidate,
    knowledge_approval_message,
    knowledge_approval_required,
    load_knowledge_approval_registry,
    save_knowledge_approval_registry,
)
from backend.models import KnowledgeUpdateRequest


def make_update(**overrides):
    payload = {
        "agent": "건축",
        "title": "반복 질문",
        "content": "검토가 필요한 자동 수집 지식입니다.",
        "source": "telegram-auto",
        "tags": "needs-review",
    }
    payload.update(overrides)
    return KnowledgeUpdateRequest(**payload)


def test_knowledge_approval_required_skips_duplicates_and_accepts_review_sources():
    assert knowledge_approval_required(make_update(), {"skipped": False}) is True
    assert knowledge_approval_required(make_update(tags="manual-knowledge", source="manual"), {"skipped": False}) is False
    assert knowledge_approval_required(make_update(), {"skipped": True}) is False


def test_build_knowledge_approval_candidate_uses_relative_paths(tmp_path):
    result_path = tmp_path / "data" / "knowledge_base" / "qa.md"
    registry = {"items": [{"id": "existing"}]}

    item = build_knowledge_approval_candidate(
        update=make_update(),
        result={"path": str(result_path)},
        registry=registry,
        assessment={"reasons": ["ok"], "top_score": 42},
        now=dt.datetime(2026, 6, 12, 10, 0, 0),
        project_root=tmp_path,
    )

    assert item["id"] == "K20260612100000-002"
    assert item["qa_path"] == "data/knowledge_base/qa.md"
    assert item["assessment"]["top_score"] == 42
    assert item["status"] == "pending_owner_approval"


def test_append_find_and_save_knowledge_approval_candidate(tmp_path):
    registry_path = tmp_path / "registry.json"

    item = append_knowledge_approval_candidate(
        update=make_update(),
        result={"path": str(tmp_path / "qa.md")},
        assessment={"reasons": ["needs owner"]},
        registry_path=registry_path,
        project_root=tmp_path,
    )
    skipped = append_knowledge_approval_candidate(
        update=make_update(source="manual", tags="manual-knowledge"),
        result={"path": str(tmp_path / "manual.md")},
        registry_path=registry_path,
        project_root=tmp_path,
    )
    registry, found = find_knowledge_approval_candidate(item["id"], registry_path)

    assert skipped is None
    assert found["id"] == item["id"]
    assert registry["items"][0]["qa_path"] == "qa.md"
    assert load_knowledge_approval_registry(registry_path)["items"][0]["id"] == item["id"]

    registry["items"][0]["status"] = "approved_promoted"
    save_knowledge_approval_registry(registry, registry_path)
    assert load_knowledge_approval_registry(registry_path)["items"][0]["status"] == "approved_promoted"


def test_knowledge_approval_message_sanitizes_preview():
    message = knowledge_approval_message({
        "id": "K1",
        "agent": "건축",
        "title": "검토",
        "source": "telegram-auto",
        "content": "secret sk-1234567890123456789012345",
        "qa_path": "qa.md",
        "assessment": {"reasons": ["자동 수집"], "top_score": 10},
    })

    assert "후보 ID: K1" in message
    assert "자동 수집" in message
    assert "sk-1234567890123456789012345" not in message
    assert "sk-[LONG_ID_MASKED]" in message
