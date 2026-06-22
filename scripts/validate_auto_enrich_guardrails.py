#!/usr/bin/env python3
"""Validate and optionally add KST04 guardrails to auto-enrich KB sections.

Auto-enrich sections are useful as intake notes, but they must not be treated as
customer-confirmed standards. This script audits sections whose source line
contains ``Source: auto-enrich via`` and checks that the same section carries a
KST04/customer-confirmation guardrail.

Usage:
  python scripts/validate_auto_enrich_guardrails.py
  python scripts/validate_auto_enrich_guardrails.py --apply
  python scripts/validate_auto_enrich_guardrails.py --max-unguarded 0
"""
from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from backend.core.paths import AGENT_KB_DIR  # noqa: E402

AUTO_ENRICH_RE = re.compile(r"^- Source: auto-enrich via\b", re.MULTILINE)
SECTION_RE = re.compile(r"(?m)^(?=## )")
GUARDRAIL_LINE = (
    "- KST04 자동수집: 공식 출처/담당자 검증 전 고객 확정 답변, "
    "납품 기준, 견적 기준으로 사용 금지."
)
GUARDRAIL_SIGNALS = (
    "KST04",
    "확정 기준으로 사용하지",
    "확정 답변",
    "고객 확정",
    "납품 기준으로 사용하지",
    "견적 기준으로 사용하지",
)


@dataclass(frozen=True)
class GuardrailIssue:
    path: Path
    title: str
    line: int


def split_sections(content: str) -> list[str]:
    return SECTION_RE.split(content)


def has_auto_enrich_source(section: str) -> bool:
    return bool(AUTO_ENRICH_RE.search(section))


def has_guardrail(section: str) -> bool:
    return any(signal in section for signal in GUARDRAIL_SIGNALS)


def section_title(section: str) -> str:
    first = section.splitlines()[0].strip() if section.splitlines() else ""
    return first.removeprefix("## ").strip() or "(preamble)"


def line_number(content: str, section: str) -> int:
    index = content.find(section)
    if index < 0:
        return 1
    return content[:index].count("\n") + 1


def audit_file(path: Path) -> list[GuardrailIssue]:
    content = path.read_text(encoding="utf-8", errors="ignore")
    issues: list[GuardrailIssue] = []
    for section in split_sections(content):
        if has_auto_enrich_source(section) and not has_guardrail(section):
            issues.append(GuardrailIssue(path, section_title(section), line_number(content, section)))
    return issues


def add_guardrails_to_content(content: str) -> tuple[str, int]:
    sections = split_sections(content)
    changed = 0
    updated_sections: list[str] = []
    for section in sections:
        if has_auto_enrich_source(section) and not has_guardrail(section):
            lines = section.splitlines()
            for idx, line in enumerate(lines):
                if AUTO_ENRICH_RE.match(line):
                    lines.insert(idx + 1, GUARDRAIL_LINE)
                    changed += 1
                    break
            section = "\n".join(lines)
            if content.endswith("\n") and not section.endswith("\n"):
                section += "\n"
        updated_sections.append(section)
    return "".join(updated_sections), changed


def apply_guardrails(path: Path) -> int:
    content = path.read_text(encoding="utf-8", errors="ignore")
    updated, changed = add_guardrails_to_content(content)
    if changed:
        path.write_text(updated, encoding="utf-8")
    return changed


def audit_tree(root: Path = AGENT_KB_DIR) -> list[GuardrailIssue]:
    issues: list[GuardrailIssue] = []
    for path in sorted(root.rglob("*.md")):
        issues.extend(audit_file(path))
    return issues


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--apply", action="store_true", help="누락된 KST04 가드레일을 파일에 삽입")
    parser.add_argument("--max-unguarded", type=int, default=None, help="허용할 미가드 섹션 수")
    args = parser.parse_args()

    if args.apply:
        touched = 0
        inserted = 0
        for path in sorted(AGENT_KB_DIR.rglob("*.md")):
            count = apply_guardrails(path)
            if count:
                touched += 1
                inserted += count
        print(f"auto-enrich KST04 guardrails inserted: {inserted} sections in {touched} files")

    issues = audit_tree()
    print(f"auto-enrich guardrail audit: unguarded {len(issues)}")
    for issue in issues[:50]:
        rel = issue.path.relative_to(PROJECT_ROOT)
        print(f"  {rel}:{issue.line} | {issue.title}")
    if len(issues) > 50:
        print(f"  ... {len(issues) - 50} more")

    if args.max_unguarded is not None and len(issues) > args.max_unguarded:
        print(f"FAIL: unguarded {len(issues)} > max {args.max_unguarded}")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
