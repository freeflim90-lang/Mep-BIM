from pathlib import Path

from scripts import luachat_metrics_report as report


def test_luachat_metrics_report_prioritizes_search_assisted_and_errors():
    snapshot = {
        "service": "luachat",
        "days": {
            "2026-06-12": {
                "updated_at": "2026-06-12T10:00:00",
                "metrics": {
                    "chat_total": 10,
                    "chat_success": 7,
                    "chat_local": 2,
                    "chat_search_assisted": 5,
                    "feedback_total": 2,
                    "feedback_updated": 1,
                    "error_total": 3,
                    "error_stages": {"answer_generation": 2, "note_persistence": 1},
                },
            }
        },
    }

    result = report.build_report(snapshot)

    assert result["totals"]["chat_total"] == 10
    assert result["totals"]["search_assist_rate"] == 50.0
    assert result["totals"]["error_stages"] == {"answer_generation": 2, "note_persistence": 1}
    assert any("reviewed FAQ" in item for item in result["recommendations"])
    assert any("answer_generation" in item for item in result["recommendations"])


def test_luachat_metrics_report_markdown_handles_empty_snapshot(tmp_path: Path):
    result = report.build_report({"service": "luachat", "days": {}})
    out = tmp_path / "report.md"

    report.write_markdown(result, out)

    text = out.read_text(encoding="utf-8")
    assert "LUAChat Operational Metrics Review" in text
    assert "No daily metrics snapshots found" in text

