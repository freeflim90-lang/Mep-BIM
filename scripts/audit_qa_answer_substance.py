#!/usr/bin/env python3
"""Audit whether each stored Q&A has answer-specific substance.

The standard quality rubric intentionally rewards conclusions, evidence,
conditions, actions and risk boundaries.  Many older Q&A records also contain
the same operational guidance after every answer.  That shared guidance is
useful, but it must not make a thin original answer look complete.

This audit scores only the answer text before repeated quality scaffolding and
produces a ranked remediation queue.  It is an audit, not a publication gate:
an item in the queue remains usable only according to its recorded KST status.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from backend.core.paths import QA_KB_DIR  # noqa: E402
from scripts.validate_agent_qa_quality import parse_pairs, score_pair  # noqa: E402

SCAFFOLD_MARKERS = (
    "\n\n실무 보강 (",
    "\n\nA: 실무 보강 (",
    "\n\n다만 예외 조건이 있거나 승인권자 판단이 필요한 경우에는",
)
SOURCE_RE = re.compile(r"(?:source\s*:|출처\s*:|https?://|kst0[1-6])", re.IGNORECASE)
SCOPE_RE = re.compile(r"(?:적용|대상|프로젝트|발주처|지자체|계약|현장|조건)", re.IGNORECASE)
ACTION_RE = re.compile(r"(?:확인|검토|요청|기록|공유|보고|반영|분류)")
RISK_RE = re.compile(r"(?:안전|법무|법적|비용|일정|보안|책임|리스크|확정하지)")
# 표준 루브릭(score_pair)이 구조화(+8)를 보상하는 것과 동일한 패턴.
# 재작성이 번호/불릿 구조를 없애 점수가 떨어지던 회귀를 감사에서 잡는다.
STRUCTURE_RE = re.compile(r"①|②|③|1\.|2\.|3\.|- ")


def core_answer(answer: str) -> str:
    """Return the answer that is specific to this Q&A, excluding shared text."""
    end = len(answer)
    for marker in SCAFFOLD_MARKERS:
        found = answer.find(marker)
        if found >= 0:
            end = min(end, found)
    return answer[:end].strip()


def assess(question: str, answer: str) -> dict:
    core = core_answer(answer)
    quality = score_pair(question, core)
    missing = []
    if len(core) < 120:
        missing.append("답변 고유 설명 120자 이상")
    if not SOURCE_RE.search(core):
        missing.append("문답 단위 근거 또는 KST 상태")
    if not SCOPE_RE.search(core):
        missing.append("적용 범위 또는 전제조건")
    if not ACTION_RE.search(core):
        missing.append("확인·검토·기록 같은 다음 액션")
    if not STRUCTURE_RE.search(core):
        missing.append("번호(1. 2. 3.)/불릿(- ) 구조 — 재작성 시 반드시 보존")
    if RISK_RE.search(f"{question}\n{core}") and not SOURCE_RE.search(core):
        missing.append("고위험 답변의 확인 가능한 근거")
    return {
        "core_length": len(core),
        "core_score": quality["total"],
        "missing": missing,
        "core_answer": core,
    }


def run(min_core_score: int, max_items: int) -> dict:
    findings = []
    all_pairs = 0
    for path in sorted(QA_KB_DIR.glob("*_QA.md")):
        agent = path.stem.removesuffix("_QA")
        for pair in parse_pairs(path):
            all_pairs += 1
            result = assess(pair["question"], pair["answer"])
            if result["core_score"] < min_core_score or result["missing"]:
                findings.append({
                    "agent": agent,
                    "path": str(path.relative_to(PROJECT_ROOT)),
                    "line": pair["line"],
                    "question": pair["question"],
                    **result,
                })
    findings.sort(key=lambda item: (item["core_score"], item["core_length"], item["agent"]))
    return {
        "total_pairs": all_pairs,
        "min_core_score": min_core_score,
        "findings": findings[:max_items],
        "finding_count": len(findings),
        "missing_counts": dict(Counter(m for item in findings for m in item["missing"])),
    }


def report(result: dict) -> str:
    lines = [
        "# Q&A Answer Substance Audit",
        "",
        f"pairs: {result['total_pairs']} | core-score threshold: {result['min_core_score']} | remediation queue: {result['finding_count']}",
        "",
        "Shared operational scaffolding is excluded from this audit.",
        "",
        "## Recurring gaps",
        "",
    ]
    for label, count in sorted(result["missing_counts"].items(), key=lambda item: (-item[1], item[0])):
        lines.append(f"- {label}: {count}")
    lines += ["", "## Highest-priority remediation items", ""]
    for item in result["findings"]:
        gaps = "; ".join(item["missing"]) or "core score below threshold"
        lines.append(
            f"- [{item['agent']}] {item['question']}  "
            f"(core {item['core_score']}/100, {item['core_length']} chars; {gaps})  "
            f"— {item['path']}:{item['line']}"
        )
    return "\n".join(lines) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(description="Audit Q&A-specific substance separately from shared guidance.")
    parser.add_argument("--min-core-score", type=int, default=70)
    parser.add_argument("--max-items", type=int, default=40)
    parser.add_argument("--json", action="store_true", help="Emit JSON instead of Markdown.")
    args = parser.parse_args()
    result = run(args.min_core_score, args.max_items)
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(report(result), end="")


if __name__ == "__main__":
    main()
