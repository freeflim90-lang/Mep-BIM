"""
clash_grouper.py — Tool 1: Automatic Clash Grouping

Reads all CSV files from the input directory.
Groups clashes by Level + DisciplineA + DisciplineB.
Adds a GroupKey column to each row.
Returns a single consolidated DataFrame.

Expected input columns:
    ClashID, Level, Grid, DisciplineA, DisciplineB,
    ClashType, Description, Distance
"""

import logging
import pandas as pd
from pathlib import Path

logger = logging.getLogger(__name__)


def load_clash_csvs(input_dir: Path) -> pd.DataFrame:
    """
    Load all CSV files from input_dir into a single DataFrame.
    Skips files that are missing required columns and logs a warning.
    Returns an empty DataFrame if no valid files are found.
    """
    if not input_dir.exists() or not input_dir.is_dir():
        logger.warning("load_clash_csvs: input directory does not exist: %s", input_dir)
        return pd.DataFrame()

    required_columns = {
        "ClashID", "Level", "Grid",
        "DisciplineA", "DisciplineB",
        "ClashType", "Description", "Distance"
    }

    frames = []
    csv_files = list(input_dir.glob("*.csv"))

    if not csv_files:
        logger.warning("load_clash_csvs: no CSV files found in %s", input_dir)
        return pd.DataFrame()

    for path in csv_files:
        try:
            df = pd.read_csv(path)
            missing = required_columns - set(df.columns)
            if missing:
                logger.warning(
                    "Skipping %s — missing columns: %s", path.name, missing
                )
                continue
            df["_source_file"] = path.name
            frames.append(df)
            logger.info("Loaded %d rows from %s", len(df), path.name)
        except Exception as exc:
            logger.warning("Skipping %s — read error: %s", path.name, exc)

    if not frames:
        logger.warning("load_clash_csvs: no valid CSV files loaded.")
        return pd.DataFrame()

    combined = pd.concat(frames, ignore_index=True)
    logger.info("load_clash_csvs: total %d clashes loaded from %d file(s)",
                len(combined), len(frames))
    return combined


def add_group_key(df: pd.DataFrame) -> pd.DataFrame:
    """
    Add a GroupKey column: Level_DisciplineA_vs_DisciplineB
    e.g. 'Level3_Mechanical_vs_Structure'

    Normalizes level names by removing spaces.
    """
    if df.empty:
        return df

    df = df.copy()
    level = df["Level"].str.replace(" ", "", regex=False)
    disc_a = df["DisciplineA"].str.strip()
    disc_b = df["DisciplineB"].str.strip()
    df["GroupKey"] = level + "_" + disc_a + "_vs_" + disc_b
    logger.info("add_group_key: %d unique GroupKeys created", df["GroupKey"].nunique())
    return df


def summarize_groups(df: pd.DataFrame) -> pd.DataFrame:
    """
    Return a summary DataFrame: one row per GroupKey with clash count.
    Sorted descending by count.
    """
    if df.empty:
        return pd.DataFrame(columns=["GroupKey", "ClashCount"])

    summary = (
        df.groupby("GroupKey")
        .size()
        .reset_index(name="ClashCount")
        .sort_values("ClashCount", ascending=False)
        .reset_index(drop=True)
    )
    logger.info("summarize_groups: %d unique groups identified", len(summary))
    return summary


def run(input_dir: Path) -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Main entry point for clash grouping.

    Returns:
        detail_df  — full clash list with GroupKey column
        summary_df — one row per group with ClashCount
    """
    logger.info("clash_grouper: starting")
    detail_df = load_clash_csvs(input_dir)
    if detail_df.empty:
        logger.warning("clash_grouper: no data to process, exiting early")
        return detail_df, pd.DataFrame()

    detail_df = add_group_key(detail_df)
    summary_df = summarize_groups(detail_df)
    logger.info(
        "clash_grouper: complete — %d clashes in %d groups",
        len(detail_df), len(summary_df)
    )
    return detail_df, summary_df
