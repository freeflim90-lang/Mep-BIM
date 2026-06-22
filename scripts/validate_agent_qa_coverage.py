#!/usr/bin/env python3
"""Validate per-agent Q&A coverage breadth.

This complements validate_agent_qa_quality.py: quality can be high while an
agent still has too few Q&A pairs to represent its actual responsibility.

Usage:
  .dev-venv/bin/python scripts/validate_agent_qa_coverage.py
  .dev-venv/bin/python scripts/validate_agent_qa_coverage.py --min-pairs 1 --max-single-pair-count 53
  .dev-venv/bin/python scripts/validate_agent_qa_coverage.py --min-pairs 3 --max-min-pair-count 62
"""
from __future__ import annotations

import argparse
import sys
from collections import Counter
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from scripts.validate_agent_qa_quality import run  # noqa: E402


def evaluate(
    min_pairs: int,
    max_single_pair_count: int | None,
    max_min_pair_count: int | None = None,
) -> dict:
    result = run(agent_filter=None, min_score=0)
    agents = result["agents"]
    distribution = Counter(agent["pair_count"] for agent in agents)
    below_min = [agent for agent in agents if agent["pair_count"] < min_pairs]
    single_pair_agents = [agent for agent in agents if agent["pair_count"] == 1]
    min_pair_count = distribution[min_pairs]
    lowest = sorted(agents, key=lambda item: (item["pair_count"], item["agent"]))[:20]

    passed = not below_min
    if max_single_pair_count is not None and len(single_pair_agents) > max_single_pair_count:
        passed = False
    if max_min_pair_count is not None and min_pair_count > max_min_pair_count:
        passed = False

    return {
        "agent_count": len(agents),
        "total_pairs": result["total_pairs"],
        "min_pairs": min_pairs,
        "max_single_pair_count": max_single_pair_count,
        "max_min_pair_count": max_min_pair_count,
        "distribution": dict(sorted(distribution.items())),
        "below_min": below_min,
        "single_pair_count": len(single_pair_agents),
        "single_pair_agents": single_pair_agents,
        "min_pair_count": min_pair_count,
        "lowest": lowest,
        "passed": passed,
    }


def build_report(result: dict) -> str:
    lines = [
        "# Agent Q&A Coverage Report",
        "",
        f"agents: {result['agent_count']} | Q&A: {result['total_pairs']} | "
        f"min_pairs: {result['min_pairs']} | "
        f"min_pair_agents: {result['min_pair_count']} | "
        f"single_pair: {result['single_pair_count']}",
        "",
        "## Distribution",
        "",
    ]
    for pair_count, agent_count in result["distribution"].items():
        lines.append(f"- {pair_count} pairs: {agent_count} agents")

    lines += ["", "## Lowest Coverage", ""]
    for agent in result["lowest"]:
        lines.append(f"- {agent['agent']}: {agent['pair_count']} pair(s)")

    if result["below_min"]:
        lines += ["", "## Below Minimum", ""]
        for agent in result["below_min"]:
            lines.append(f"- {agent['agent']}: {agent['pair_count']} < {result['min_pairs']}")

    if (
        result["max_single_pair_count"] is not None
        and result["single_pair_count"] > result["max_single_pair_count"]
    ):
        lines += [
            "",
            f"FAIL: single-pair agents {result['single_pair_count']} > "
            f"limit {result['max_single_pair_count']}",
        ]

    if (
        result["max_min_pair_count"] is not None
        and result["min_pair_count"] > result["max_min_pair_count"]
    ):
        lines += [
            "",
            f"FAIL: min-pair agents {result['min_pair_count']} > "
            f"limit {result['max_min_pair_count']}",
        ]

    lines.append("")
    lines.append("PASS" if result["passed"] else "FAIL")
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate per-agent Q&A coverage breadth.")
    parser.add_argument("--min-pairs", type=int, default=1, help="Minimum Q&A pairs per agent.")
    parser.add_argument(
        "--max-single-pair-count",
        type=int,
        help="Maximum allowed number of agents that still have only one Q&A pair.",
    )
    parser.add_argument(
        "--max-min-pair-count",
        type=int,
        help="Maximum allowed number of agents exactly at the configured minimum pair count.",
    )
    args = parser.parse_args()

    result = evaluate(args.min_pairs, args.max_single_pair_count, args.max_min_pair_count)
    print(build_report(result))
    sys.exit(0 if result["passed"] else 1)


if __name__ == "__main__":
    main()
