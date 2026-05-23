"""
issue_stub.py — Tool 2: ACC Issue Creation (Phase 2 Stub)

This module is a placeholder for the Autodesk Construction Cloud (ACC)
issue creation integration. In Phase 2, this module will:
    1. Authenticate with ACC using OAuth 2.0 (Client Credentials flow)
    2. Iterate over Critical and High priority clashes
    3. Create a coordination issue in ACC for each clash
    4. Assign the issue to the responsible trade
    5. Set a due date (7 days from creation)

Current behavior:
    - Logs what would be created without making any API calls
    - Returns a list of simulated issue dicts for pipeline visibility

Phase 2 implementation checklist:
    TODO (Phase 2): Set ACC_CLIENT_ID and ACC_CLIENT_SECRET in config.py
    TODO (Phase 2): Set ACC_PROJECT_ID in config.py
    TODO (Phase 2): Implement _get_access_token() using requests + OAuth
    TODO (Phase 2): Implement _create_issue() using ACC Issues API v1
    TODO (Phase 2): Add retry logic for API rate limits (429 responses)
    TODO (Phase 2): Add email alert on authentication failure
    TODO (Phase 2): Replace simulated_issues return with live API responses

ACC API reference:
    https://aps.autodesk.com/en/docs/acc/v1/reference/http/issues-v1-issues-POST/
"""

import logging
from datetime import date, timedelta
from typing import Any

import pandas as pd

logger = logging.getLogger(__name__)

ISSUE_DISCIPLINES = {"Critical", "High"}
DEFAULT_DUE_DAYS = 7


def _discipline_to_trade(discipline_a: str, discipline_b: str) -> str:
    """
    Map a discipline pair to the responsible trade for assignment.
    In Phase 2, this will resolve against ACC project members.
    """
    # TODO (Phase 2): resolve against ACC project member list
    if discipline_a == "Structure" and discipline_b == "Structure":
        logger.warning("_discipline_to_trade: both disciplines are Structure — defaulting to 'Structure Contractor'")
        return "Structure Contractor"
    priority_discipline = discipline_a if discipline_a != "Structure" else discipline_b
    return f"{priority_discipline} Contractor"


def run(detail_df: pd.DataFrame) -> list[dict[str, Any]]:
    """
    Simulate ACC issue creation for Critical and High priority clashes.

    Args:
        detail_df — enriched, prioritized clash DataFrame

    Returns:
        List of simulated issue dicts (what would be sent to ACC API)
    """
    logger.info("issue_stub: starting (Phase 2 stub — no API calls made)")

    if detail_df.empty:
        logger.warning("issue_stub: empty DataFrame, no issues to create")
        return []

    if "Priority" not in detail_df.columns:
        logger.warning("issue_stub: 'Priority' column missing from DataFrame — skipping issue creation")
        return []
    actionable = detail_df[detail_df["Priority"].isin(ISSUE_DISCIPLINES)].copy()
    logger.info(
        "issue_stub: %d clashes qualify for issue creation (%s)",
        len(actionable), ", ".join(ISSUE_DISCIPLINES)
    )

    due_date = (date.today() + timedelta(days=DEFAULT_DUE_DAYS)).isoformat()
    simulated_issues = []

    for _, row in actionable.iterrows():
        trade = _discipline_to_trade(row["DisciplineA"], row["DisciplineB"])
        issue = {
            "title": f"{row['DisciplineA']} vs {row['DisciplineB']} Clash — {row['Level']} Grid {row['Grid']}",
            "description": row["Description"],
            "status": "open",
            "priority": row["Priority"].lower(),
            "assignedTo": trade,
            "dueDate": due_date,
            "clashId": row["ClashID"],
            "groupKey": row["GroupKey"],
            "projectId": None,   # TODO (Phase 2): set from config.ACC_PROJECT_ID
            "issueType": None,   # TODO (Phase 2): set from ACC issue type list
        }
        simulated_issues.append(issue)
        logger.info(
            "issue_stub: [SIMULATED] would create issue — %s | %s | due %s",
            issue["title"], trade, due_date
        )

    logger.info(
        "issue_stub: complete — %d issues simulated (Phase 2: replace with live API calls)",
        len(simulated_issues)
    )
    return simulated_issues
