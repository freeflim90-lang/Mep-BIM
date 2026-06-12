"""
clash_prioritizer.py — Tool 4: Clash Prioritization Engine

Takes the enriched clash DataFrame (with GroupKey) from clash_grouper.
Adds a Priority column to each row: Critical, High, Medium, or Low.

Priority logic (based on construction risk):
    Critical — either discipline is structural
    High     — either discipline is mechanical or plumbing
    Medium   — all other combinations
    Low      — cosmetic clashes (Lighting vs Ceiling, etc.)

Low-priority overrides: defined in LOW_PRIORITY_PAIRS below.
"""

import logging
import pandas as pd

from config import CRITICAL_DISCIPLINES, HIGH_DISCIPLINES

logger = logging.getLogger(__name__)

# Frozensets so order doesn't matter: {"Lighting", "Ceiling"} matches either direction
LOW_PRIORITY_PAIRS = [
    frozenset({"Lighting", "Ceiling"}),
    frozenset({"Lighting", "Furniture"}),
    frozenset({"Ceiling", "Furniture"}),
]


def classify_priority(discipline_a: str, discipline_b: str) -> str:
    """
    Return the priority string for a clash between two disciplines.
    Returns 'Medium' if either discipline value is missing/null.
    """
    if not isinstance(discipline_a, str) or not isinstance(discipline_b, str):
        return "Medium"
    pair = frozenset({discipline_a.strip(), discipline_b.strip()})

    if pair in LOW_PRIORITY_PAIRS:
        return "Low"
    if CRITICAL_DISCIPLINES & pair:
        return "Critical"
    if HIGH_DISCIPLINES & pair:
        return "High"
    return "Medium"


def add_priority(df: pd.DataFrame) -> pd.DataFrame:
    """
    Add a Priority column to the clash DataFrame.
    Operates row-by-row using classify_priority().
    Returns the modified DataFrame.
    """
    if df.empty:
        logger.warning("add_priority: received empty DataFrame, skipping")
        return df

    df = df.copy()
    df["Priority"] = df.apply(
        lambda row: classify_priority(row["DisciplineA"], row["DisciplineB"]),
        axis=1
    )

    counts = df["Priority"].value_counts().to_dict()
    logger.info("add_priority: priority distribution — %s", counts)
    return df


def run(detail_df: pd.DataFrame) -> pd.DataFrame:
    """
    Main entry point for clash prioritization.

    Args:
        detail_df — enriched clash DataFrame from clash_grouper.run()

    Returns:
        detail_df with Priority column added
    """
    logger.info("clash_prioritizer: starting")
    result = add_priority(detail_df)
    logger.info("clash_prioritizer: complete — %d clashes prioritized", len(result))
    return result
