#!/usr/bin/env python3
"""Validate AI collaboration register and escalation audit artifacts."""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_REGISTER = PROJECT_ROOT / "data/knowledge_base/conflict_resolution/SESSION_REGISTER_202606.md"
DEFAULT_SLA = PROJECT_ROOT / "data/knowledge_base/conflict_resolution/ESCALATION_SLA_TRACKER_202606.md"
CASE_ROOT = PROJECT_ROOT / "data/knowledge_base/conflict_resolution"

SESSION_STATUSES = {"CLOSED", "ESCALATED"}
CONSENSUS_STATUSES = {"CONSENSUS_WITH_GUARDRAILS", "ESCALATE"}
RISK_STATUSES = {
    "NOT_NEEDED",
    "LOCAL_ONLY",
    "REDACTED_REVIEW",
    "APPROVED",
    "APPROVED_WITH_HOLD",
    "BLOCKED",
}
DECISION_STATUSES = {"Explicitly Deferred", "Draft Created"}
REUSE_STATUSES = {"Created", "Updated", "Explicitly Deferred", "Missing"}
SLA_STATUSES = {"ON_TRACK", "AT_RISK", "BREACHED", "CLOSED"}
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
SESSION_ID_RE = re.compile(r"^AICOL-\d{8}-\d{3}$")


def audit_error(subject: str, message: str, fix: str) -> str:
    return f"{subject}: {message} | fix: {fix}"


@dataclass(frozen=True)
class SessionRow:
    session_id: str
    date_time: str
    mode: str
    status: str
    consensus: str
    risk: str
    decision: str
    case_file: str
    reuse: str
    next_review: str


@dataclass(frozen=True)
class SlaRow:
    case_id: str
    session_id: str
    owner: str
    due_by: str
    risk: str
    status: str
    evidence: str


def split_markdown_row(line: str) -> list[str]:
    return [cell.strip().strip("`") for cell in line.strip().strip("|").split("|")]


def is_separator(cells: list[str]) -> bool:
    return all(re.fullmatch(r":?-{3,}:?", cell.strip()) for cell in cells)


def iter_table_rows(path: Path) -> list[list[str]]:
    rows: list[list[str]] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if not stripped.startswith("|") or not stripped.endswith("|"):
            continue
        cells = split_markdown_row(stripped)
        if cells and not is_separator(cells):
            rows.append(cells)
    return rows


def load_sessions(path: Path) -> list[SessionRow]:
    sessions: list[SessionRow] = []
    for cells in iter_table_rows(path):
        if not cells or not SESSION_ID_RE.fullmatch(cells[0]):
            continue
        if len(cells) != 13:
            raise ValueError(f"{path}: session row has {len(cells)} cells, expected 13: {cells[0]}")
        sessions.append(
            SessionRow(
                session_id=cells[0],
                date_time=cells[1],
                mode=cells[3],
                status=cells[6],
                consensus=cells[7],
                risk=cells[8],
                decision=cells[9],
                case_file=cells[10],
                reuse=cells[11],
                next_review=cells[12],
            )
        )
    return sessions


def load_sla_rows(path: Path) -> list[SlaRow]:
    rows: list[SlaRow] = []
    for cells in iter_table_rows(path):
        if len(cells) < 8:
            continue
        if not cells[0].startswith("AITEST_") or not cells[1].startswith("AICOL-"):
            continue
        rows.append(
            SlaRow(
                case_id=cells[0],
                session_id=cells[1],
                owner=cells[2],
                due_by=cells[3],
                risk=cells[4],
                status=cells[6],
                evidence=cells[7],
            )
        )
    return rows


def case_id_from_path(case_file: str) -> str:
    return Path(case_file).stem


def validate(register: Path, sla_tracker: Path) -> tuple[list[str], dict[str, int]]:
    errors: list[str] = []
    sessions = load_sessions(register)
    sla_rows = load_sla_rows(sla_tracker)
    sla_by_session = {row.session_id: row for row in sla_rows}

    if not sessions:
        errors.append(
            audit_error(
                str(register),
                "no AICOL session rows found",
                "check the session register table and AICOL ID format",
            )
        )

    seen_sessions: set[str] = set()
    for session in sessions:
        if session.session_id in seen_sessions:
            errors.append(
                audit_error(
                    session.session_id,
                    "duplicate session id",
                    "assign a unique AICOL session ID in SESSION_REGISTER_202606.md",
                )
            )
        seen_sessions.add(session.session_id)

        if session.status not in SESSION_STATUSES:
            errors.append(
                audit_error(
                    session.session_id,
                    f"invalid status {session.status}",
                    "use CLOSED or ESCALATED in the register status column",
                )
            )
        if session.consensus not in CONSENSUS_STATUSES:
            errors.append(
                audit_error(
                    session.session_id,
                    f"invalid consensus {session.consensus}",
                    "use CONSENSUS_WITH_GUARDRAILS or ESCALATE in the consensus column",
                )
            )
        if session.risk not in RISK_STATUSES:
            errors.append(
                audit_error(
                    session.session_id,
                    f"invalid risk {session.risk}",
                    "replace with one of NOT_NEEDED, LOCAL_ONLY, REDACTED_REVIEW, APPROVED, APPROVED_WITH_HOLD, BLOCKED",
                )
            )
        if session.decision not in DECISION_STATUSES:
            errors.append(
                audit_error(
                    session.session_id,
                    f"invalid decision {session.decision}",
                    "use Explicitly Deferred for test sessions or Draft Created for escalated draft decisions",
                )
            )
        if session.reuse not in REUSE_STATUSES:
            errors.append(
                audit_error(
                    session.session_id,
                    f"invalid reuse closure {session.reuse}",
                    "use Created, Updated, Explicitly Deferred, or Missing",
                )
            )
        if not DATE_RE.fullmatch(session.next_review):
            errors.append(
                audit_error(
                    session.session_id,
                    f"invalid next review date {session.next_review}",
                    "enter next review as YYYY-MM-DD",
                )
            )
        if session.status == "ESCALATED" and session.consensus != "ESCALATE":
            errors.append(
                audit_error(
                    session.session_id,
                    "ESCALATED session must use ESCALATE consensus",
                    "change the consensus column to ESCALATE or change the session status",
                )
            )
        if session.status == "CLOSED" and session.consensus == "ESCALATE":
            errors.append(
                audit_error(
                    session.session_id,
                    "CLOSED session cannot use ESCALATE consensus",
                    "change consensus to CONSENSUS_WITH_GUARDRAILS or keep the session ESCALATED",
                )
            )
        if session.status == "CLOSED" and session.reuse != "Updated":
            errors.append(
                audit_error(
                    session.session_id,
                    "CLOSED session reuse closure must be Updated",
                    "update KB/QA/backlog evidence or reopen the session before marking it CLOSED",
                )
            )
        if session.status == "ESCALATED" and session.reuse not in {"Created", "Updated"}:
            errors.append(
                audit_error(
                    session.session_id,
                    "ESCALATED session reuse closure must be Created or Updated",
                    "create a source-of-truth draft, SLA row, or other follow-up artifact",
                )
            )

        case_path = CASE_ROOT / session.case_file
        if not case_path.is_file():
            errors.append(
                audit_error(
                    session.session_id,
                    f"missing case file {case_path.relative_to(PROJECT_ROOT)}",
                    "create the case file under conflict_resolution/cases or fix the register link",
                )
            )

        if session.status == "ESCALATED":
            sla = sla_by_session.get(session.session_id)
            if not sla:
                errors.append(
                    audit_error(
                        session.session_id,
                        "missing SLA tracker row",
                        "add this ESCALATED session to ESCALATION_SLA_TRACKER_202606.md",
                    )
                )
            else:
                if sla.case_id != case_id_from_path(session.case_file):
                    errors.append(
                        audit_error(
                            session.session_id,
                            f"SLA case {sla.case_id} does not match {session.case_file}",
                            "align the SLA case ID with the register case file stem",
                        )
                    )
                if not sla.owner:
                    errors.append(
                        audit_error(
                            session.session_id,
                            "SLA owner is empty",
                            "fill the Owner column in ESCALATION_SLA_TRACKER_202606.md",
                        )
                    )
                if not DATE_RE.fullmatch(sla.due_by):
                    errors.append(
                        audit_error(
                            session.session_id,
                            f"invalid SLA due date {sla.due_by}",
                            "enter SLA Due by as YYYY-MM-DD",
                        )
                    )
                if sla.risk != session.risk:
                    errors.append(
                        audit_error(
                            session.session_id,
                            f"SLA risk {sla.risk} != register risk {session.risk}",
                            "make the SLA risk state match the session register risk gate",
                        )
                    )
                if sla.status not in SLA_STATUSES:
                    errors.append(
                        audit_error(
                            session.session_id,
                            f"invalid SLA status {sla.status}",
                            "use ON_TRACK, AT_RISK, BREACHED, or CLOSED",
                        )
                    )
                if not sla.evidence:
                    errors.append(
                        audit_error(
                            session.session_id,
                            "SLA evidence is empty",
                            "add evidence or current basis in the SLA tracker evidence column",
                        )
                    )

    metrics = {
        "sessions": len(sessions),
        "closed": sum(1 for session in sessions if session.status == "CLOSED"),
        "escalated": sum(1 for session in sessions if session.status == "ESCALATED"),
        "sla_rows": len(sla_rows),
    }
    return errors, metrics


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate AI collaboration audit artifacts.")
    parser.add_argument("--register", type=Path, default=DEFAULT_REGISTER)
    parser.add_argument("--sla-tracker", type=Path, default=DEFAULT_SLA)
    parser.add_argument("--quiet", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    errors, metrics = validate(args.register.resolve(), args.sla_tracker.resolve())
    if errors:
        for error in errors:
            print(f"FAIL {error}", file=sys.stderr)
        print(
            "SUMMARY "
            f"sessions={metrics['sessions']} closed={metrics['closed']} "
            f"escalated={metrics['escalated']} sla_rows={metrics['sla_rows']}",
            file=sys.stderr,
        )
        return 1
    if not args.quiet:
        print(
            "PASS "
            f"sessions={metrics['sessions']} closed={metrics['closed']} "
            f"escalated={metrics['escalated']} sla_rows={metrics['sla_rows']}"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
