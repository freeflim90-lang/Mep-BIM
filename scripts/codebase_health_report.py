#!/usr/bin/env python3
"""Generate a maintainability and growth-potential snapshot for LUA BIM LABS."""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


PROJECT_ROOT = Path(__file__).resolve().parents[1]
import sys as _sys  # noqa: E402
if str(PROJECT_ROOT) not in _sys.path:
    _sys.path.insert(0, str(PROJECT_ROOT))
from backend.core.paths import BIM_SCRIPTS_DIR  # noqa: E402

DEFAULT_IGNORE_DIRS = {
    ".git",
    ".dev-venv",
    ".venv",
    "__pycache__",
    ".pytest_cache",
    "node_modules",
    "dist",
    "logs",
    "runtime",
    ".wrangler",
}
DEFAULT_IGNORE_PATH_PREFIXES = {
    BIM_SCRIPTS_DIR.relative_to(PROJECT_ROOT).as_posix() + "/",
}
CODE_SUFFIXES = {".py", ".js", ".ts", ".tsx", ".cs", ".html", ".css"}
DOC_SUFFIXES = {".md", ".txt", ".rst"}
FIRST_PARTY_PREFIXES = ("backend/", "scripts/", "frontend/", "website/", "tests/")


@dataclass(frozen=True)
class FileMetric:
    path: str
    lines: int
    suffix: str


def should_skip(path: Path, ignored_dirs: set[str], ignored_path_prefixes: set[str]) -> bool:
    rel = path.as_posix()
    return any(part in ignored_dirs for part in path.parts) or any(
        rel == prefix.rstrip("/") or rel.startswith(prefix)
        for prefix in ignored_path_prefixes
    )


def iter_files(root: Path, ignored_dirs: set[str], ignored_path_prefixes: set[str]) -> Iterable[Path]:
    for path in root.rglob("*"):
        if path.is_file() and not should_skip(path.relative_to(root), ignored_dirs, ignored_path_prefixes):
            yield path


def count_lines(path: Path) -> int:
    try:
        return len(path.read_text(encoding="utf-8", errors="ignore").splitlines())
    except OSError:
        return 0


def collect_file_metrics(
    root: Path,
    ignored_dirs: set[str],
    ignored_path_prefixes: set[str] | None = None,
) -> list[FileMetric]:
    ignored_path_prefixes = ignored_path_prefixes or set()
    metrics: list[FileMetric] = []
    for path in iter_files(root, ignored_dirs, ignored_path_prefixes):
        suffix = path.suffix.lower()
        if suffix in CODE_SUFFIXES or suffix in DOC_SUFFIXES:
            metrics.append(FileMetric(path.relative_to(root).as_posix(), count_lines(path), suffix))
    return metrics


def directory_totals(metrics: list[FileMetric]) -> dict[str, int]:
    totals: dict[str, int] = {}
    for metric in metrics:
        top = metric.path.split("/", 1)[0]
        totals[top] = totals.get(top, 0) + metric.lines
    return dict(sorted(totals.items(), key=lambda item: item[1], reverse=True))


def top_large_files(metrics: list[FileMetric], limit: int = 15) -> list[dict]:
    rows = sorted(metrics, key=lambda item: item.lines, reverse=True)[:limit]
    return [{"path": row.path, "lines": row.lines, "suffix": row.suffix} for row in rows]


def categorize(metrics: list[FileMetric]) -> dict[str, int]:
    code_lines = sum(item.lines for item in metrics if item.suffix in CODE_SUFFIXES)
    doc_lines = sum(item.lines for item in metrics if item.suffix in DOC_SUFFIXES)
    test_lines = sum(item.lines for item in metrics if item.path.startswith("tests/"))
    backend_lines = sum(item.lines for item in metrics if item.path.startswith("backend/"))
    script_lines = sum(item.lines for item in metrics if item.path.startswith("scripts/"))
    first_party_code_lines = sum(
        item.lines
        for item in metrics
        if item.suffix in CODE_SUFFIXES and item.path.startswith(FIRST_PARTY_PREFIXES)
    )
    return {
        "tracked_text_files_scanned": len(metrics),
        "code_lines": code_lines,
        "doc_lines": doc_lines,
        "first_party_code_lines": first_party_code_lines,
        "backend_lines": backend_lines,
        "script_lines": script_lines,
        "test_lines": test_lines,
        "test_to_backend_ratio_percent": round((test_lines / backend_lines * 100), 2) if backend_lines else 0,
        "test_to_first_party_code_ratio_percent": round((test_lines / first_party_code_lines * 100), 2) if first_party_code_lines else 0,
    }


def identify_risks(metrics: list[FileMetric], dirs: dict[str, int]) -> list[dict]:
    risks: list[dict] = []
    large_files = [item for item in metrics if item.suffix in CODE_SUFFIXES and item.lines >= 500]
    if large_files:
        risks.append({
            "severity": "high",
            "area": "large_modules",
            "finding": f"{len(large_files)} code files are 500+ lines.",
            "action": "Extract pure helpers and route/service modules, keeping tests green after each move.",
        })

    backend_lines = sum(item.lines for item in metrics if item.path.startswith("backend/"))
    test_lines = sum(item.lines for item in metrics if item.path.startswith("tests/"))
    if backend_lines and test_lines / backend_lines < 0.08:
        risks.append({
            "severity": "high",
            "area": "test_coverage_proxy",
            "finding": f"Test lines are only {round(test_lines / backend_lines * 100, 2)}% of backend lines.",
            "action": "Add endpoint and persistence tests around existing profitable/operational workflows.",
        })

    if "data" in dirs and dirs["data"] > dirs.get("backend", 0):
        risks.append({
            "severity": "medium",
            "area": "repository_boundary",
            "finding": "Data/knowledge/vendor material is larger than backend source.",
            "action": "Keep runtime/vendor data ignored or moved behind explicit import/export workflows.",
        })

    if "scripts" in dirs and dirs["scripts"] > dirs.get("tests", 0) * 10:
        risks.append({
            "severity": "medium",
            "area": "automation_surface",
            "finding": "Automation scripts are much larger than their tests.",
            "action": "Promote reusable script logic into small modules and test the scheduling-critical paths.",
        })

    return risks


def growth_opportunities(summary: dict, risks: list[dict]) -> list[dict]:
    opportunities = [
        {
            "theme": "commercial_reliability",
            "opportunity": "Treat LUAChat/Revit Assistant as an operational product surface with health, auth, and feedback tests.",
            "next_step": "Review recurring LUAChat support backlog items weekly and convert approved items into customer-facing FAQ pages.",
        },
        {
            "theme": "knowledge_productization",
            "opportunity": "Use the knowledge base as reusable product collateral instead of passive notes.",
            "next_step": "Generate service FAQ, sales snippets, and Revit add-in support answers from approved knowledge only.",
        },
        {
            "theme": "automation_roi",
            "opportunity": "Standardize high-frequency scripts behind make targets and measurable outputs.",
            "next_step": "Add make targets for market briefing, knowledge curation, and add-in readiness audit with dry-run modes.",
        },
    ]
    if any(risk["area"] == "large_modules" for risk in risks):
        opportunities.append({
            "theme": "engineering_velocity",
            "opportunity": "Reducing `server_total.py` responsibility will make feature delivery less risky.",
            "next_step": "Continue extracting the next high-traffic API area from `server_total.py` into router/controller/service modules.",
        })
    if summary.get("test_to_backend_ratio_percent", 0) < 10:
        opportunities.append({
            "theme": "delivery_confidence",
            "opportunity": "A small number of high-signal endpoint tests can unlock safer frequent releases.",
            "next_step": "Target 15% test-to-backend line ratio before adding major new product features.",
        })
    return opportunities


def build_report(
    root: Path = PROJECT_ROOT,
    ignored_dirs: set[str] | None = None,
    ignored_path_prefixes: set[str] | None = None,
) -> dict:
    ignored = ignored_dirs or DEFAULT_IGNORE_DIRS
    ignored_prefixes = ignored_path_prefixes if ignored_path_prefixes is not None else DEFAULT_IGNORE_PATH_PREFIXES
    metrics = collect_file_metrics(root, ignored, ignored_prefixes)
    dirs = directory_totals(metrics)
    summary = categorize(metrics)
    risks = identify_risks(metrics, dirs)
    return {
        "summary": summary,
        "top_directories_by_lines": dirs,
        "largest_files": top_large_files(metrics),
        "risks": risks,
        "growth_opportunities": growth_opportunities(summary, risks),
        "excluded_reference_paths": sorted(ignored_prefixes),
    }


def write_markdown(report: dict, path: Path) -> None:
    lines = [
        "# LUA BIM LABS Codebase Health Report",
        "",
        "## Summary",
        "",
    ]
    for key, value in report["summary"].items():
        lines.append(f"- {key}: {value}")

    if report.get("excluded_reference_paths"):
        lines.extend(["", "## Excluded Reference Paths", ""])
        for item in report["excluded_reference_paths"]:
            lines.append(f"- `{item}`")

    lines.extend(["", "## Largest Files", ""])
    for item in report["largest_files"][:10]:
        lines.append(f"- `{item['path']}`: {item['lines']} lines")

    lines.extend(["", "## Risks", ""])
    for risk in report["risks"]:
        lines.append(f"- {risk['severity'].upper()} `{risk['area']}`: {risk['finding']} Action: {risk['action']}")

    lines.extend(["", "## Growth Opportunities", ""])
    for item in report["growth_opportunities"]:
        lines.append(f"- `{item['theme']}`: {item['opportunity']} Next: {item['next_step']}")

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", dest="json_path", type=Path, help="Write report JSON to this path.")
    parser.add_argument("--markdown", dest="markdown_path", type=Path, help="Write report markdown to this path.")
    args = parser.parse_args()

    report = build_report()
    if args.json_path:
        args.json_path.parent.mkdir(parents=True, exist_ok=True)
        args.json_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    if args.markdown_path:
        write_markdown(report, args.markdown_path)
    if not args.json_path and not args.markdown_path:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
