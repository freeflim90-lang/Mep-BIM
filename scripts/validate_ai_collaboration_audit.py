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
DEFAULT_CONFLICT_LOG = PROJECT_ROOT / "data/knowledge_base/conflict_resolution/CONFLICT_LOG.md"
CASE_ROOT = PROJECT_ROOT / "data/knowledge_base/conflict_resolution"
KST04_SOURCE_DRAFT = CASE_ROOT / "KST04_CUSTOMER_RESPONSE_PROMOTION_SOURCE_OF_TRUTH_DRAFT_20260606.md"
KST04_MISSING_MATRIX = CASE_ROOT / "KST04_PROMOTION_MISSING_EVIDENCE_MATRIX_20260606.md"

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


@dataclass(frozen=True)
class ConflictIndexRow:
    case_id: str
    status: str
    opened: str
    due_by: str
    owner: str


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


def load_conflict_summary(path: Path) -> dict[str, int]:
    summary: dict[str, int] = {}
    for cells in iter_table_rows(path):
        if len(cells) != 2:
            continue
        if cells[0] in {"상태", "건수"}:
            continue
        if cells[0] in {"OPEN", "PENDING", "MEDIATED", "ESCALATED", "SETTLED", "PRECEDENT", "누계"}:
            try:
                summary[cells[0]] = int(cells[1])
            except ValueError:
                summary[cells[0]] = -1
    return summary


def load_conflict_index_rows(path: Path) -> list[ConflictIndexRow]:
    rows: list[ConflictIndexRow] = []
    for cells in iter_table_rows(path):
        if len(cells) != 10:
            continue
        if not cells[0].startswith("AITEST_"):
            continue
        rows.append(
            ConflictIndexRow(
                case_id=cells[0],
                status=cells[5],
                opened=cells[6],
                due_by=cells[7],
                owner=cells[8],
            )
        )
    return rows


def case_id_from_path(case_file: str) -> str:
    return Path(case_file).stem


def find_decision_log_path(case_path: Path) -> str | None:
    for cells in iter_table_rows(case_path):
        if len(cells) >= 2 and cells[0] == "Decision Log":
            return cells[1]
    return None


def clean_artifact_path(value: str) -> str:
    return value.strip().strip("`")


def key_value_rows(path: Path) -> dict[str, str]:
    values: dict[str, str] = {}
    for cells in iter_table_rows(path):
        if len(cells) >= 2 and cells[0] not in {"항목", "선택지", "체크", "일자"}:
            values.setdefault(cells[0], cells[1])
    return values


def count_choice_rows(path: Path) -> int:
    return sum(1 for cells in iter_table_rows(path) if len(cells) >= 4 and re.fullmatch(r"[A-D]\..+", cells[0]))


def has_current_draft_decision(path: Path) -> bool:
    values = key_value_rows(path)
    return all(values.get(key) for key in ("선택안", "결정 사유", "후속 조치"))


def has_unfinalized_decision_markers(path: Path) -> bool:
    text = path.read_text(encoding="utf-8")
    markers = ("Draft Created", "재판정 예정", "예정", "후보", "Missing", "재판정 후", "현재 초안 판정")
    return any(marker in text for marker in markers)


def table_rows_with_first_cell(path: Path, first_cell: str) -> list[list[str]]:
    return [cells for cells in iter_table_rows(path) if cells and cells[0] == first_cell]


def is_kst04_escalation(session: SessionRow, case_path: Path) -> bool:
    if session.status != "ESCALATED":
        return False
    if "KNOWLEDGE_PROMOTION" in session.mode:
        return True
    if not case_path.is_file():
        return False
    return "KST04" in case_path.read_text(encoding="utf-8")


def validate_kst04_followup(session: SessionRow, case_path: Path, sla_text: str) -> list[str]:
    errors: list[str] = []
    case_id = case_id_from_path(session.case_file)
    required_artifacts = [
        ("KST04 source of truth draft", KST04_SOURCE_DRAFT),
        ("KST04 missing evidence matrix", KST04_MISSING_MATRIX),
    ]

    for label, artifact_path in required_artifacts:
        if not artifact_path.is_file():
            errors.append(
                audit_error(
                    session.session_id,
                    f"missing {label} {artifact_path.relative_to(PROJECT_ROOT)}",
                    "create the KST04 follow-up artifact before leaving the KST04 escalation ON_TRACK",
                )
            )
            continue
        artifact_text = artifact_path.read_text(encoding="utf-8")
        if session.session_id not in artifact_text:
            errors.append(
                audit_error(
                    session.session_id,
                    f"{label} does not reference {session.session_id}",
                    "add the original ESCALATED AICOL session ID to the KST04 follow-up artifact",
                )
            )
        if session.case_file not in artifact_text and case_id not in artifact_text:
            errors.append(
                audit_error(
                    session.session_id,
                    f"{label} does not reference {case_id}",
                    "link the KST04 follow-up artifact back to the original case file",
                )
            )

    if KST04_SOURCE_DRAFT.name not in sla_text or KST04_MISSING_MATRIX.name not in sla_text:
        errors.append(
            audit_error(
                session.session_id,
                "SLA tracker does not reference KST04 follow-up artifacts",
                "add the KST04 source draft and missing evidence matrix to the SLA tracker readiness section",
            )
        )

    if KST04_MISSING_MATRIX.is_file():
        p0_rows = table_rows_with_first_cell(KST04_MISSING_MATRIX, "P0")
        if len(p0_rows) < 4:
            errors.append(
                audit_error(
                    session.session_id,
                    f"KST04 missing evidence matrix has only {len(p0_rows)} P0 rows",
                    "keep P0 rows for official source, customer wording, legal review, and QA counterexamples",
                )
            )
        for row in p0_rows:
            if len(row) < 7 or not all(row[index] for index in (1, 2, 3, 4, 5, 6)):
                errors.append(
                    audit_error(
                        session.session_id,
                        "KST04 P0 evidence row is incomplete",
                        "fill evidence, owner, validator, due by, default action, and target state in the matrix",
                    )
                )
                continue
            if not DATE_RE.fullmatch(row[4]):
                errors.append(
                    audit_error(
                        session.session_id,
                        f"KST04 P0 evidence row has invalid due date {row[4]}",
                        "enter KST04 Missing Matrix Due by as YYYY-MM-DD",
                    )
                )
            if row[4] != session.next_review:
                errors.append(
                    audit_error(
                        session.session_id,
                        f"KST04 P0 due date {row[4]} != register next review {session.next_review}",
                        "align KST04 P0 due dates with the original escalation review date",
                    )
                )
            if "고객 확정 응답 금지" not in row[5] and "확정" not in row[5]:
                errors.append(
                    audit_error(
                        session.session_id,
                        "KST04 P0 row default action does not preserve customer-confirmed-response hold",
                        "state the pre-remediation default action as KST04 hold or customer confirmed response ban",
                    )
                )

    if KST04_SOURCE_DRAFT.is_file():
        source_text = KST04_SOURCE_DRAFT.read_text(encoding="utf-8")
        for required_phrase in ("고객 확정 응답", "KST04 유지", "재판정"):
            if required_phrase not in source_text:
                errors.append(
                    audit_error(
                        session.session_id,
                        f"KST04 source draft missing required guardrail phrase {required_phrase}",
                        "keep customer response hold, KST04 fallback, and redecision language in the source draft",
                    )
                )

    return errors


def validate(register: Path, sla_tracker: Path, conflict_log: Path) -> tuple[list[str], dict[str, int]]:
    errors: list[str] = []
    sessions = load_sessions(register)
    sla_rows = load_sla_rows(sla_tracker)
    sla_by_session = {row.session_id: row for row in sla_rows}
    sla_text = sla_tracker.read_text(encoding="utf-8")
    conflict_summary = load_conflict_summary(conflict_log)
    conflict_index_rows = load_conflict_index_rows(conflict_log)
    conflict_by_case = {row.case_id: row for row in conflict_index_rows}

    if not sessions:
        errors.append(
            audit_error(
                str(register),
                "no AICOL session rows found",
                "check the session register table and AICOL ID format",
            )
        )

    seen_sessions: set[str] = set()
    sessions_by_case: dict[str, SessionRow] = {}
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
        sessions_by_case[case_id_from_path(session.case_file)] = session

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
            if case_path.is_file():
                decision_log = find_decision_log_path(case_path)
                if not decision_log or clean_artifact_path(decision_log) in {"", "TBD"}:
                    errors.append(
                        audit_error(
                            session.session_id,
                            "missing decision log draft path in case Reuse Closure",
                            "replace the Decision Log TBD with a real draft path under conflict_resolution/decision_logs",
                        )
                    )
                else:
                    decision_path = PROJECT_ROOT / clean_artifact_path(decision_log)
                    if not decision_path.is_file():
                        errors.append(
                            audit_error(
                                session.session_id,
                                f"missing decision log draft {decision_path.relative_to(PROJECT_ROOT)}",
                                "create the decision log draft file or fix the case Reuse Closure path",
                            )
                        )
                    else:
                        decision_values = key_value_rows(decision_path)
                        expected_decision_id = decision_path.stem
                        if decision_values.get("Decision ID") != expected_decision_id:
                            errors.append(
                                audit_error(
                                    session.session_id,
                                    f"decision log ID {decision_values.get('Decision ID', '<missing>')} != file stem {expected_decision_id}",
                                    "make the Decision ID field match the decision log filename",
                                )
                            )
                        if decision_values.get("AI 협업 세션 ID") != session.session_id:
                            errors.append(
                                audit_error(
                                    session.session_id,
                                    "decision log session id does not match register",
                                    "set AI 협업 세션 ID in the decision log to the ESCALATED AICOL session ID",
                                )
                            )
                        expected_case_id = case_id_from_path(session.case_file)
                        if decision_values.get("관련 케이스") != expected_case_id:
                            errors.append(
                                audit_error(
                                    session.session_id,
                                    "decision log case id does not match register case file",
                                    "set 관련 케이스 in the decision log to the case file stem",
                                )
                            )
                        if decision_values.get("합의 상태") != session.consensus:
                            errors.append(
                                audit_error(
                                    session.session_id,
                                    "decision log consensus does not match register",
                                    "set 합의 상태 in the decision log to the register consensus value",
                                )
                            )
                        if count_choice_rows(decision_path) < 4:
                            errors.append(
                                audit_error(
                                    session.session_id,
                                    "decision log has fewer than four redecision choices",
                                    "include A/B/C/D rows for approval, deferral, remediation, and breach",
                                )
                            )
                        if not has_current_draft_decision(decision_path):
                            errors.append(
                                audit_error(
                                    session.session_id,
                                    "decision log current draft decision is incomplete",
                                    "fill 선택안, 결정 사유, and 후속 조치 in the current draft decision section",
                                )
                            )

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

            if is_kst04_escalation(session, case_path):
                errors.extend(validate_kst04_followup(session, case_path, sla_text))

    conflict_status_counts: dict[str, int] = {}
    for row in conflict_index_rows:
        conflict_status_counts[row.status] = conflict_status_counts.get(row.status, 0) + 1
        if row.status in {"ESCALATED", "SETTLED", "PRECEDENT"}:
            if not DATE_RE.fullmatch(row.opened):
                errors.append(
                    audit_error(
                        row.case_id,
                        f"invalid conflict opened date {row.opened}",
                        "enter CONFLICT_LOG Opened as YYYY-MM-DD",
                    )
                )
            if not DATE_RE.fullmatch(row.due_by):
                errors.append(
                    audit_error(
                        row.case_id,
                        f"invalid conflict due date {row.due_by}",
                        "enter CONFLICT_LOG Due by as YYYY-MM-DD",
                    )
                )
            if not row.owner:
                errors.append(
                    audit_error(
                        row.case_id,
                        "conflict index owner is empty",
                        "fill Owner in the CONFLICT_LOG case index",
                    )
                )

    for status in ("OPEN", "PENDING", "MEDIATED", "ESCALATED", "SETTLED", "PRECEDENT"):
        expected = conflict_status_counts.get(status, 0)
        actual = conflict_summary.get(status)
        if actual is None:
            errors.append(
                audit_error(
                    "CONFLICT_LOG",
                    f"missing summary row for {status}",
                    "add all standard status rows to the CONFLICT_LOG status summary",
                )
            )
        elif actual != expected:
            errors.append(
                audit_error(
                    "CONFLICT_LOG",
                    f"summary {status}={actual} but index has {expected}",
                    "update the CONFLICT_LOG status summary to match the case index",
                )
            )

    expected_total = len(conflict_index_rows)
    actual_total = conflict_summary.get("누계")
    if actual_total is None:
        errors.append(
            audit_error(
                "CONFLICT_LOG",
                "missing summary row for 누계",
                "add the total row to the CONFLICT_LOG status summary",
            )
        )
    elif actual_total != expected_total:
        errors.append(
            audit_error(
                "CONFLICT_LOG",
                f"summary total={actual_total} but index has {expected_total}",
                "update the CONFLICT_LOG 누계 row to match the case index count",
            )
        )

    escalated_sessions = [session for session in sessions if session.status == "ESCALATED"]
    for session in escalated_sessions:
        case_id = case_id_from_path(session.case_file)
        conflict_row = conflict_by_case.get(case_id)
        if not conflict_row:
            errors.append(
                audit_error(
                    session.session_id,
                    f"ESCALATED case {case_id} missing from CONFLICT_LOG index",
                    "add the ESCALATED case to the CONFLICT_LOG case index with Owner and Due by",
                )
            )
            continue
        if conflict_row.status != "ESCALATED":
            errors.append(
                audit_error(
                    session.session_id,
                    f"CONFLICT_LOG status {conflict_row.status} != register ESCALATED",
                    "align the CONFLICT_LOG case index status with the session register",
                )
            )
        if conflict_row.due_by != session.next_review:
            errors.append(
                audit_error(
                    session.session_id,
                    f"CONFLICT_LOG due {conflict_row.due_by} != register next review {session.next_review}",
                    "align the CONFLICT_LOG Due by date with the ESCALATED register review date",
                )
            )

    for conflict_row in conflict_index_rows:
        if conflict_row.status != "ESCALATED":
            continue
        session = sessions_by_case.get(conflict_row.case_id)
        if not session:
            errors.append(
                audit_error(
                    conflict_row.case_id,
                    "CONFLICT_LOG ESCALATED case has no matching session register row",
                    "add the matching AICOL row to the session register or downgrade the Conflict Log status with evidence",
                )
            )
            continue
        if session.status != "ESCALATED":
            errors.append(
                audit_error(
                    session.session_id,
                    f"CONFLICT_LOG still ESCALATED but register status is {session.status}",
                    "when closing a register session, update CONFLICT_LOG status/summary and supporting decision evidence in the same pass",
                )
            )

    for conflict_row in conflict_index_rows:
        if conflict_row.status not in {"SETTLED", "PRECEDENT"}:
            continue
        session = sessions_by_case.get(conflict_row.case_id)
        if session and session.status != "CLOSED":
            errors.append(
                audit_error(
                    session.session_id,
                    f"CONFLICT_LOG is {conflict_row.status} but register status is {session.status}",
                    "when settling a conflict, close the matching register row and update Reuse Closure in the same pass",
                )
            )

    for session in sessions:
        if session.status != "CLOSED":
            continue
        sla = sla_by_session.get(session.session_id)
        if sla and sla.status != "CLOSED":
            errors.append(
                audit_error(
                    session.session_id,
                    f"register is CLOSED but SLA status is {sla.status}",
                    "when closing an escalated register row, set the matching SLA row to CLOSED or remove/reclassify the stale SLA tracking row",
                )
            )
        conflict_row = conflict_by_case.get(case_id_from_path(session.case_file))
        requires_final_decision = bool(sla) or (conflict_row is not None and conflict_row.status in {"SETTLED", "PRECEDENT"})
        if not requires_final_decision:
            continue
        case_path = CASE_ROOT / session.case_file
        if not case_path.is_file():
            continue
        decision_log = find_decision_log_path(case_path)
        clean_decision_log = clean_artifact_path(decision_log or "")
        if not clean_decision_log or clean_decision_log in {"", "TBD"} or not clean_decision_log.endswith(".md"):
            if not sla:
                continue
            errors.append(
                audit_error(
                    session.session_id,
                    "closed escalated/settled case has no final decision log path",
                    "keep the Decision Log path and finalize it when closing an escalated or settled conflict",
                )
            )
            continue
        decision_path = PROJECT_ROOT / clean_decision_log
        if not decision_path.is_file():
            errors.append(
                audit_error(
                    session.session_id,
                    f"closed case decision log is missing {decision_path.relative_to(PROJECT_ROOT)}",
                    "create the final decision log or fix the case Reuse Closure path",
                )
            )
            continue
        if has_unfinalized_decision_markers(decision_path):
            errors.append(
                audit_error(
                    session.session_id,
                    "closed case decision log still contains draft or missing-evidence markers",
                    "replace Draft/예정/후보/Missing language with the actual final choice, date, reason, and follow-up actions before closing",
                )
            )

    metrics = {
        "sessions": len(sessions),
        "closed": sum(1 for session in sessions if session.status == "CLOSED"),
        "escalated": sum(1 for session in sessions if session.status == "ESCALATED"),
        "sla_rows": len(sla_rows),
        "conflicts": len(conflict_index_rows),
    }
    return errors, metrics


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate AI collaboration audit artifacts.")
    parser.add_argument("--register", type=Path, default=DEFAULT_REGISTER)
    parser.add_argument("--sla-tracker", type=Path, default=DEFAULT_SLA)
    parser.add_argument("--conflict-log", type=Path, default=DEFAULT_CONFLICT_LOG)
    parser.add_argument("--quiet", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    errors, metrics = validate(args.register.resolve(), args.sla_tracker.resolve(), args.conflict_log.resolve())
    if errors:
        for error in errors:
            print(f"FAIL {error}", file=sys.stderr)
        print(
            "SUMMARY "
            f"sessions={metrics['sessions']} closed={metrics['closed']} "
            f"escalated={metrics['escalated']} sla_rows={metrics['sla_rows']} "
            f"conflicts={metrics['conflicts']}",
            file=sys.stderr,
        )
        return 1
    if not args.quiet:
        print(
            "PASS "
            f"sessions={metrics['sessions']} closed={metrics['closed']} "
            f"escalated={metrics['escalated']} sla_rows={metrics['sla_rows']} "
            f"conflicts={metrics['conflicts']}"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
