#!/usr/bin/env python3
"""Generate an organization growth and operations priority report."""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any


PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from scripts import luachat_metrics_report, luachat_support_backlog

DEFAULT_HEALTH_JSON = PROJECT_ROOT / "runtime" / "codebase_health_latest.json"
DEFAULT_LUACHAT_METRICS = PROJECT_ROOT / "runtime" / "luachat_metrics_daily.json"
DEFAULT_MARKDOWN = PROJECT_ROOT / "docs" / "ORG_GROWTH_OPPORTUNITIES_LATEST.md"
DEFAULT_JSON = PROJECT_ROOT / "runtime" / "org_growth_opportunities_latest.json"


@dataclass(frozen=True)
class GrowthPriority:
    score: int
    priority: str
    theme: str
    finding: str
    evidence: str
    owner: str
    next_action: str
    business_impact: str


def load_json(path: Path, default: dict[str, Any] | None = None) -> dict[str, Any]:
    if not path.exists():
        return default or {}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return default or {}
    return data if isinstance(data, dict) else (default or {})


def priority_label(score: int) -> str:
    if score >= 90:
        return "P0"
    if score >= 75:
        return "P1"
    if score >= 60:
        return "P2"
    return "P3"


def _risk_by_area(health: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {
        str(item.get("area", "")): item
        for item in health.get("risks", [])
        if isinstance(item, dict)
    }


def build_growth_priorities(
    health: dict[str, Any],
    luachat_snapshot: dict[str, Any],
) -> list[GrowthPriority]:
    priorities: list[GrowthPriority] = []
    summary = health.get("summary", {})
    risks = _risk_by_area(health)
    luachat_report = luachat_metrics_report.build_report(luachat_snapshot)
    luachat_backlog = luachat_support_backlog.build_backlog(luachat_report)
    totals = luachat_report["totals"]

    if totals["error_total"] > 0:
        top_item = luachat_backlog[0]
        priorities.append(GrowthPriority(
            score=98,
            priority="P0",
            theme="commercial_reliability",
            finding=top_item.title,
            evidence=f"LUAChat error_total={totals['error_total']}; top_error_stage={luachat_support_backlog.top_error_stage(totals) or 'unknown'}",
            owner=top_item.owner,
            next_action=top_item.next_action,
            business_impact="Protects paid product trust by keeping generated answers, QA archive, and support follow-up reliable.",
        ))

    if "large_modules" in risks:
        priorities.append(GrowthPriority(
            score=86,
            priority="P1",
            theme="engineering_velocity",
            finding=risks["large_modules"]["finding"],
            evidence=f"backend_lines={summary.get('backend_lines', 0)}; server_total.py remains a concentrated runtime module.",
            owner="Backend Maintainer",
            next_action=risks["large_modules"]["action"],
            business_impact="Reduces regression risk and makes revenue-facing backend changes faster to ship.",
        ))

    if "automation_surface" in risks:
        priorities.append(GrowthPriority(
            score=78,
            priority="P1",
            theme="automation_roi",
            finding=risks["automation_surface"]["finding"],
            evidence=f"script_lines={summary.get('script_lines', 0)}; test_lines={summary.get('test_lines', 0)}",
            owner="Operations + Automation Maintainer",
            next_action=risks["automation_surface"]["action"],
            business_impact="Turns existing automation into dependable operating leverage instead of opaque scheduled work.",
        ))

    test_ratio = float(summary.get("test_to_backend_ratio_percent") or 0)
    if test_ratio < 25:
        priorities.append(GrowthPriority(
            score=72,
            priority="P2",
            theme="delivery_confidence",
            finding="Backend test ratio is still below the next confidence threshold.",
            evidence=f"test_to_backend_ratio_percent={test_ratio}",
            owner="Backend Maintainer",
            next_action="Add focused tests around remaining Telegram, automation, and BIM Land mutation paths before expanding features.",
            business_impact="Raises confidence for frequent releases while preserving current working behavior.",
        ))

    if "repository_boundary" in risks:
        priorities.append(GrowthPriority(
            score=66,
            priority="P2",
            theme="repository_boundary",
            finding=risks["repository_boundary"]["finding"],
            evidence="Knowledge/data/vendor material dominates source volume.",
            owner="Operations + Knowledge Curator",
            next_action=risks["repository_boundary"]["action"],
            business_impact="Keeps product source reviewable while still using knowledge assets for sales and support.",
        ))

    if totals["chat_total"] == 0:
        priorities.append(GrowthPriority(
            score=62,
            priority="P2",
            theme="product_usage_signal",
            finding="LUAChat usage signal is not yet large enough for FAQ/product decisions.",
            evidence="chat_total=0",
            owner="Operations + Customer Support",
            next_action="Keep daily metrics enabled and review again after live customer usage accumulates.",
            business_impact="Prevents premature content decisions and makes support investment evidence-based.",
        ))

    seen = set()
    deduped = []
    for item in sorted(priorities, key=lambda row: row.score, reverse=True):
        key = (item.theme, item.finding)
        if key in seen:
            continue
        seen.add(key)
        deduped.append(item)
    return deduped


def build_report(health: dict[str, Any], luachat_snapshot: dict[str, Any]) -> dict[str, Any]:
    priorities = build_growth_priorities(health, luachat_snapshot)
    summary = health.get("summary", {})
    luachat_totals = luachat_metrics_report.build_report(luachat_snapshot)["totals"]
    return {
        "summary": {
            "backend_lines": summary.get("backend_lines", 0),
            "script_lines": summary.get("script_lines", 0),
            "test_lines": summary.get("test_lines", 0),
            "test_to_backend_ratio_percent": summary.get("test_to_backend_ratio_percent", 0),
            "luachat_chat_total": luachat_totals["chat_total"],
            "luachat_error_total": luachat_totals["error_total"],
            "luachat_success_rate_percent": luachat_totals["success_rate"],
        },
        "priorities": [asdict(item) for item in priorities],
    }


def write_markdown(report: dict[str, Any], path: Path) -> None:
    lines = [
        "# LUA BIM LABS Organization Growth Priorities",
        "",
        "## Operating Snapshot",
        "",
    ]
    for key, value in report["summary"].items():
        lines.append(f"- {key}: {value}")

    lines.extend(["", "## Priority Queue", ""])
    for index, item in enumerate(report["priorities"], start=1):
        lines.extend([
            f"### {index}. [{item['priority']}] {item['theme']} - score {item['score']}",
            "",
            f"- finding: {item['finding']}",
            f"- evidence: {item['evidence']}",
            f"- owner: {item['owner']}",
            f"- next_action: {item['next_action']}",
            f"- business_impact: {item['business_impact']}",
            "",
        ])

    if not report["priorities"]:
        lines.extend([
            "No urgent growth or operational priorities were detected from the available metrics.",
            "",
        ])

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--health-json", type=Path, default=DEFAULT_HEALTH_JSON)
    parser.add_argument("--luachat-metrics", type=Path, default=DEFAULT_LUACHAT_METRICS)
    parser.add_argument("--markdown", type=Path, default=DEFAULT_MARKDOWN)
    parser.add_argument("--json", dest="json_path", type=Path, default=DEFAULT_JSON)
    args = parser.parse_args()

    health = load_json(args.health_json, default={"summary": {}, "risks": []})
    luachat_snapshot = luachat_metrics_report.load_metrics_snapshot(args.luachat_metrics)
    report = build_report(health, luachat_snapshot)

    write_markdown(report, args.markdown)
    args.json_path.parent.mkdir(parents=True, exist_ok=True)
    args.json_path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(args.markdown)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
