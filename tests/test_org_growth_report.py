from __future__ import annotations

import json

from scripts import org_growth_report


def _health_snapshot() -> dict:
    return {
        "summary": {
            "backend_lines": 1000,
            "script_lines": 6000,
            "test_lines": 200,
            "test_to_backend_ratio_percent": 20.0,
        },
        "risks": [
            {
                "severity": "high",
                "area": "large_modules",
                "finding": "4 code files are 500+ lines.",
                "action": "Extract helpers.",
            },
            {
                "severity": "medium",
                "area": "automation_surface",
                "finding": "Automation scripts are much larger than their tests.",
                "action": "Test scheduling-critical paths.",
            },
            {
                "severity": "medium",
                "area": "repository_boundary",
                "finding": "Data/knowledge/vendor material is larger than backend source.",
                "action": "Move runtime/vendor data behind explicit workflows.",
            },
        ],
    }


def _luachat_snapshot(error_total: int = 1) -> dict:
    metrics = {
        "chat_total": 3,
        "chat_success": 2,
        "chat_local": 2,
        "chat_search_assisted": 0,
        "feedback_total": 0,
        "feedback_updated": 0,
        "error_total": error_total,
        "error_stages": {"note_persistence": error_total} if error_total else {},
    }
    return {
        "service": "luachat",
        "latest_date": "2026-06-12",
        "days": {"2026-06-12": {"date": "2026-06-12", "metrics": metrics}},
    }


def test_build_growth_priorities_orders_reliability_before_maintainability():
    priorities = org_growth_report.build_growth_priorities(_health_snapshot(), _luachat_snapshot())

    assert priorities[0].priority == "P0"
    assert priorities[0].theme == "commercial_reliability"
    assert "note_persistence" in priorities[0].evidence
    assert [item.theme for item in priorities][1:4] == [
        "engineering_velocity",
        "automation_roi",
        "delivery_confidence",
    ]


def test_build_report_summarizes_operating_metrics():
    report = org_growth_report.build_report(_health_snapshot(), _luachat_snapshot(error_total=0))

    assert report["summary"]["backend_lines"] == 1000
    assert report["summary"]["luachat_chat_total"] == 3
    assert report["summary"]["luachat_error_total"] == 0
    assert all(item["theme"] != "commercial_reliability" for item in report["priorities"])


def test_write_markdown_and_json_payload_are_stable(tmp_path):
    report = org_growth_report.build_report(_health_snapshot(), _luachat_snapshot())
    markdown_path = tmp_path / "growth.md"
    json_path = tmp_path / "growth.json"

    org_growth_report.write_markdown(report, markdown_path)
    json_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")

    markdown = markdown_path.read_text(encoding="utf-8")
    payload = json.loads(json_path.read_text(encoding="utf-8"))
    assert "Organization Growth Priorities" in markdown
    assert "Priority Queue" in markdown
    assert payload["priorities"][0]["theme"] == "commercial_reliability"
