from pathlib import Path

import pytest
from fastapi import HTTPException

from backend import revit_assistant_security as security


def test_revit_feedback_note_path_rejects_empty_absolute_and_traversal():
    project_root = Path("/repo")
    allowed_root = project_root / "obsidian_vaults/lua_bim_lab_global_map/NAS_Knowledge/Revit_Assistant_QA"

    assert security.resolve_revit_feedback_note_path("", project_root=project_root, allowed_root=allowed_root) is None
    assert security.resolve_revit_feedback_note_path("/tmp/outside.md", project_root=project_root, allowed_root=allowed_root) is None
    assert (
        security.resolve_revit_feedback_note_path(
            "obsidian_vaults/model_quality_auditor/../outside.md",
            project_root=project_root,
            allowed_root=allowed_root,
        )
        is None
    )


def test_revit_feedback_note_path_allows_revit_qa_notes():
    note = "obsidian_vaults/lua_bim_lab_global_map/NAS_Knowledge/Revit_Assistant_QA/sample.md"
    project_root = Path("/repo")
    allowed_root = project_root / "obsidian_vaults/lua_bim_lab_global_map/NAS_Knowledge/Revit_Assistant_QA"

    resolved = security.resolve_revit_feedback_note_path(note, project_root=project_root, allowed_root=allowed_root)

    assert resolved == (project_root / note).resolve()


def test_revit_api_key_accepts_configured_token(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setenv("LUA_CHAT_TOKEN", "primary-token")
    monkeypatch.setenv("REVIT_ASSISTANT_API_KEYS", "secondary-token, third-token")

    security.require_revit_assistant_api_key("secondary-token")


def test_revit_api_key_rejects_wrong_token(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setenv("LUA_CHAT_TOKEN", "primary-token")
    monkeypatch.setenv("REVIT_ASSISTANT_API_KEYS", "")

    with pytest.raises(HTTPException):
        security.require_revit_assistant_api_key("wrong-token")


def test_bearer_token_extraction_is_strict():
    assert security.extract_bearer_token("Bearer abc123") == "abc123"
    assert security.extract_bearer_token("bearer abc123") == "abc123"
    assert security.extract_bearer_token("Token abc123") is None
    assert security.extract_bearer_token("Bearer") is None
