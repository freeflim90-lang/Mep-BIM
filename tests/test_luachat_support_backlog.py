from pathlib import Path

from scripts import luachat_support_backlog as backlog


def test_luachat_support_backlog_prioritizes_note_persistence_warning(tmp_path: Path):
    snapshot = {
        "service": "luachat",
        "days": {
            "2026-06-12": {
                "metrics": {
                    "chat_total": 10,
                    "chat_success": 8,
                    "chat_local": 3,
                    "chat_search_assisted": 5,
                    "feedback_total": 4,
                    "feedback_updated": 2,
                    "error_total": 1,
                    "error_stages": {"note_persistence": 1},
                }
            }
        },
    }

    result = backlog.build_support_backlog(snapshot)
    titles = [item.title for item in result["items"]]

    assert titles[0] == "Restore Revit Assistant QA note archiving reliability"
    assert any("reviewed FAQ" in item.title for item in result["items"])
    assert any("feedback update loop" in item.title for item in result["items"])

    markdown = tmp_path / "backlog.md"
    backlog.write_markdown(result, markdown)
    text = markdown.read_text(encoding="utf-8")

    assert "note_persistence" in text
    assert "support_snippet" in text
    assert "knowledge_base_candidate" in text


def test_luachat_support_backlog_handles_empty_metrics():
    result = backlog.build_support_backlog({"service": "luachat", "days": {}})

    assert len(result["items"]) == 1
    item = result["items"][0]
    assert item.title == "Collect enough live LUAChat usage before publishing new FAQ items"
    assert "monitoring live usage" in item.support_snippet
