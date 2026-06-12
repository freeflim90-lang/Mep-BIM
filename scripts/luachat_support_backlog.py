#!/usr/bin/env python3
"""Generate support and FAQ backlog items from LUAChat metrics."""

from __future__ import annotations

import argparse
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any


PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from scripts import luachat_metrics_report

DEFAULT_INPUT = PROJECT_ROOT / "runtime" / "luachat_metrics_daily.json"
DEFAULT_OUTPUT = PROJECT_ROOT / "docs" / "revenue_products" / "LUACHAT_SUPPORT_BACKLOG_LATEST.md"


@dataclass(frozen=True)
class BacklogItem:
    priority: str
    title: str
    trigger: str
    customer_impact: str
    support_snippet: str
    knowledge_base_candidate: str
    owner: str
    next_action: str


def top_error_stage(totals: dict[str, Any]) -> str:
    stages = totals.get("error_stages")
    if not isinstance(stages, dict) or not stages:
        return ""
    return str(next(iter(stages)))


def build_backlog(report: dict[str, Any]) -> list[BacklogItem]:
    totals = report["totals"]
    items: list[BacklogItem] = []

    if totals["chat_total"] == 0:
        return [
            BacklogItem(
                priority="P2",
                title="Collect enough live LUAChat usage before publishing new FAQ items",
                trigger="No daily chat metrics are available.",
                customer_impact="Support cannot distinguish real recurring issues from assumptions yet.",
                support_snippet="We are monitoring live usage and will turn repeated questions into reviewed help content.",
                knowledge_base_candidate="LUAChat usage monitoring and FAQ promotion policy",
                owner="Operations + Knowledge Curator",
                next_action="Keep daily metrics snapshots enabled and review again after meaningful usage.",
            )
        ]

    stage = top_error_stage(totals)
    if stage == "note_persistence":
        items.append(
            BacklogItem(
                priority="P0",
                title="Restore Revit Assistant QA note archiving reliability",
                trigger="`note_persistence` is the top recorded error stage.",
                customer_impact="Answers can still be delivered, but QA archiving and follow-up tracking are degraded.",
                support_snippet="Your answer was generated successfully. We are separately checking the internal QA archive path used for follow-up tracking.",
                knowledge_base_candidate="Troubleshooting Revit Assistant note archive warnings",
                owner="Backend Maintainer + Customer Support",
                next_action="Check Obsidian QA note directory permissions, path configuration, and recent archive write failures.",
            )
        )
    elif totals["error_total"] > 0:
        items.append(
            BacklogItem(
                priority="P0",
                title=f"Investigate LUAChat `{stage or 'unknown'}` reliability failures",
                trigger=f"{totals['error_total']} chat error(s) were recorded.",
                customer_impact="Some customer requests may fail before a usable answer is returned.",
                support_snippet="We are checking a service reliability issue and will retry the request after the affected step is restored.",
                knowledge_base_candidate=f"LUAChat `{stage or 'unknown'}` failure response playbook",
                owner="Backend Maintainer",
                next_action="Reproduce the failing stage with TestClient coverage and add a customer-safe fallback if possible.",
            )
        )

    if totals["search_assist_rate"] >= 30:
        items.append(
            BacklogItem(
                priority="P1",
                title="Promote search-assisted LUAChat answers into reviewed FAQ entries",
                trigger=f"Search-assisted answer rate is {totals['search_assist_rate']}%.",
                customer_impact="Customers are asking questions not fully covered by local reviewed knowledge.",
                support_snippet="We found a related reference and are turning repeated questions into reviewed support content.",
                knowledge_base_candidate="High-frequency search-assisted Revit Assistant answers",
                owner="Knowledge Curator + Technical Writer",
                next_action="Review search-assisted knowledge candidates, approve stable answers, and publish customer-facing FAQ snippets.",
            )
        )

    if totals["feedback_total"] and totals["feedback_update_rate"] < 70:
        items.append(
            BacklogItem(
                priority="P1",
                title="Improve customer correction and feedback update loop",
                trigger=f"Feedback update rate is {totals['feedback_update_rate']}%.",
                customer_impact="Customer corrections may not consistently improve future answers.",
                support_snippet="Thank you for the correction. We review feedback before adding it to the approved knowledge base.",
                knowledge_base_candidate="LUAChat feedback review and approval workflow",
                owner="Customer Support + Knowledge Curator",
                next_action="Audit ignored feedback reasons and document which corrections can be safely promoted.",
            )
        )

    if totals["chat_local"] > totals["chat_search_assisted"]:
        items.append(
            BacklogItem(
                priority="P2",
                title="Package stable local-knowledge answers as support snippets",
                trigger="Local-knowledge answers outnumber search-assisted answers.",
                customer_impact="Repeated stable answers can reduce support response time and improve consistency.",
                support_snippet="This answer is based on our reviewed internal Revit Assistant knowledge.",
                knowledge_base_candidate="Approved Revit Assistant support snippet library",
                owner="Technical Writer",
                next_action="Select repeated local answers and convert them into reusable FAQ/support response templates.",
            )
        )

    if not items:
        items.append(
            BacklogItem(
                priority="P3",
                title="Maintain current LUAChat support coverage",
                trigger="No urgent reliability, search coverage, or feedback loop issues were detected.",
                customer_impact="Current support coverage appears stable from available metrics.",
                support_snippet="LUAChat is operating normally based on the latest health snapshot.",
                knowledge_base_candidate="Routine LUAChat operations review",
                owner="Operations",
                next_action="Continue daily review and watch for repeated customer-facing questions.",
            )
        )
    return items


def build_support_backlog(snapshot: dict[str, Any]) -> dict[str, Any]:
    report = luachat_metrics_report.build_report(snapshot)
    return {
        "service": report["service"],
        "totals": report["totals"],
        "recommendations": report["recommendations"],
        "items": build_backlog(report),
    }


def write_markdown(backlog: dict[str, Any], path: Path) -> None:
    totals = backlog["totals"]
    lines = [
        "# LUAChat Support Backlog",
        "",
        "## Metrics Basis",
        "",
        f"- chat_total: {totals['chat_total']}",
        f"- success_rate_percent: {totals['success_rate']}",
        f"- search_assist_rate_percent: {totals['search_assist_rate']}",
        f"- feedback_update_rate_percent: {totals['feedback_update_rate']}",
        f"- error_total: {totals['error_total']}",
        "",
        "## Backlog Items",
        "",
    ]
    for index, item in enumerate(backlog["items"], start=1):
        lines.extend(
            [
                f"### {index}. [{item.priority}] {item.title}",
                "",
                f"- trigger: {item.trigger}",
                f"- customer_impact: {item.customer_impact}",
                f"- support_snippet: {item.support_snippet}",
                f"- knowledge_base_candidate: {item.knowledge_base_candidate}",
                f"- owner: {item.owner}",
                f"- next_action: {item.next_action}",
                "",
            ]
        )

    lines.extend(["## Source Recommendations", ""])
    lines.extend(f"- {item}" for item in backlog["recommendations"])

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("--markdown", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()

    snapshot = luachat_metrics_report.load_metrics_snapshot(args.input)
    backlog = build_support_backlog(snapshot)
    write_markdown(backlog, args.markdown)
    print(args.markdown)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
