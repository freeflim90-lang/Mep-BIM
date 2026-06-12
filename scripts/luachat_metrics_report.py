#!/usr/bin/env python3
"""Generate an operational review from LUAChat daily metrics snapshots."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_INPUT = PROJECT_ROOT / "runtime" / "luachat_metrics_daily.json"
DEFAULT_OUTPUT = PROJECT_ROOT / "docs" / "revenue_products" / "LUACHAT_OPERATIONAL_METRICS_LATEST.md"


def load_metrics_snapshot(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {"service": "luachat", "days": {}}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {"service": "luachat", "days": {}}
    return data if isinstance(data, dict) else {"service": "luachat", "days": {}}


def metric_value(metrics: dict[str, Any], key: str) -> int:
    value = metrics.get(key, 0)
    return value if isinstance(value, int) else 0


def summarize_days(snapshot: dict[str, Any]) -> list[dict[str, Any]]:
    days = snapshot.get("days")
    if not isinstance(days, dict):
        return []

    rows = []
    for date, row in sorted(days.items()):
        if not isinstance(row, dict):
            continue
        metrics = row.get("metrics")
        if not isinstance(metrics, dict):
            continue
        chat_total = metric_value(metrics, "chat_total")
        chat_success = metric_value(metrics, "chat_success")
        search_assisted = metric_value(metrics, "chat_search_assisted")
        feedback_total = metric_value(metrics, "feedback_total")
        feedback_updated = metric_value(metrics, "feedback_updated")
        error_total = metric_value(metrics, "error_total")
        rows.append({
            "date": str(date),
            "updated_at": str(row.get("updated_at", "")),
            "chat_total": chat_total,
            "chat_success": chat_success,
            "chat_local": metric_value(metrics, "chat_local"),
            "chat_search_assisted": search_assisted,
            "feedback_total": feedback_total,
            "feedback_updated": feedback_updated,
            "error_total": error_total,
            "success_rate": round(chat_success / chat_total * 100, 1) if chat_total else 0.0,
            "search_assist_rate": round(search_assisted / chat_total * 100, 1) if chat_total else 0.0,
            "feedback_update_rate": round(feedback_updated / feedback_total * 100, 1) if feedback_total else 0.0,
            "error_stages": metrics.get("error_stages", {}) if isinstance(metrics.get("error_stages"), dict) else {},
        })
    return rows


def aggregate_rows(rows: list[dict[str, Any]]) -> dict[str, Any]:
    totals = {
        "chat_total": sum(row["chat_total"] for row in rows),
        "chat_success": sum(row["chat_success"] for row in rows),
        "chat_local": sum(row["chat_local"] for row in rows),
        "chat_search_assisted": sum(row["chat_search_assisted"] for row in rows),
        "feedback_total": sum(row["feedback_total"] for row in rows),
        "feedback_updated": sum(row["feedback_updated"] for row in rows),
        "error_total": sum(row["error_total"] for row in rows),
        "error_stages": {},
    }
    error_stages: dict[str, int] = {}
    for row in rows:
        for stage, count in row["error_stages"].items():
            if isinstance(count, int):
                error_stages[stage] = error_stages.get(stage, 0) + count
    totals["error_stages"] = dict(sorted(error_stages.items(), key=lambda item: (-item[1], item[0])))
    chat_total = totals["chat_total"]
    feedback_total = totals["feedback_total"]
    totals["success_rate"] = round(totals["chat_success"] / chat_total * 100, 1) if chat_total else 0.0
    totals["search_assist_rate"] = round(totals["chat_search_assisted"] / chat_total * 100, 1) if chat_total else 0.0
    totals["feedback_update_rate"] = round(totals["feedback_updated"] / feedback_total * 100, 1) if feedback_total else 0.0
    return totals


def recommendations(totals: dict[str, Any]) -> list[str]:
    items: list[str] = []
    if totals["chat_total"] == 0:
        return ["Collect live LUAChat usage before prioritizing new support content."]
    if totals["search_assist_rate"] >= 30:
        items.append("Promote high-frequency search-assisted answers into reviewed FAQ and knowledge-base entries.")
    if totals["error_total"] > 0:
        top_stage = next(iter(totals["error_stages"]), "unknown")
        if top_stage == "note_persistence":
            items.append("Investigate `note_persistence` warnings first; answers can continue, but QA archiving and follow-up tracking are degraded.")
        else:
            items.append(f"Investigate `{top_stage}` errors first; they are blocking operational reliability.")
    if totals["feedback_total"] and totals["feedback_update_rate"] < 70:
        items.append("Review ignored or rejected feedback paths to improve customer correction loops.")
    if totals["chat_local"] > totals["chat_search_assisted"]:
        items.append("Package stable local-knowledge answers as customer-facing support snippets.")
    if not items:
        items.append("Maintain current support coverage and monitor trends daily.")
    return items


def build_report(snapshot: dict[str, Any]) -> dict[str, Any]:
    rows = summarize_days(snapshot)
    totals = aggregate_rows(rows)
    return {
        "service": snapshot.get("service", "luachat"),
        "days": rows,
        "totals": totals,
        "recommendations": recommendations(totals),
    }


def write_markdown(report: dict[str, Any], path: Path) -> None:
    totals = report["totals"]
    lines = [
        "# LUAChat Operational Metrics Review",
        "",
        "## Summary",
        "",
        f"- days: {len(report['days'])}",
        f"- chat_total: {totals['chat_total']}",
        f"- success_rate_percent: {totals['success_rate']}",
        f"- search_assist_rate_percent: {totals['search_assist_rate']}",
        f"- feedback_update_rate_percent: {totals['feedback_update_rate']}",
        f"- error_total: {totals['error_total']}",
        "",
        "## Recommendations",
        "",
    ]
    lines.extend(f"- {item}" for item in report["recommendations"])
    lines.extend(["", "## Daily Rows", ""])
    if not report["days"]:
        lines.append("- No daily metrics snapshots found.")
    else:
        for row in report["days"]:
            lines.append(
                f"- {row['date']}: chats {row['chat_total']}, success {row['success_rate']}%, "
                f"search-assisted {row['search_assist_rate']}%, errors {row['error_total']}"
            )

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("--markdown", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()

    report = build_report(load_metrics_snapshot(args.input))
    write_markdown(report, args.markdown)
    print(args.markdown)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
