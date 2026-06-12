"""
report_generator.py — Tool 3: Weekly Coordination Report Generator

Produces three output files from the enriched, prioritized clash DataFrame:
    1. weekly_coordination_report.csv   — full enriched clash list
    2. weekly_coordination_report.xlsx  — 3 tabs: Summary, Discipline Breakdown, High Risk Areas
    3. weekly_coordination_report.pdf   — 1-page summary for Friday coordination meeting

Dependencies:
    pip install pandas openpyxl reportlab
"""

import logging
from datetime import date
from pathlib import Path

import pandas as pd
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle
from reportlab.lib import colors

from config import (
    REPORT_BASENAME,
    PDF_TITLE,
    EXCEL_SHEET_SUMMARY,
    EXCEL_SHEET_DISCIPLINE,
    EXCEL_SHEET_HIGHRISK,
    HIGH_RISK_THRESHOLD,
)

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# CSV output
# ---------------------------------------------------------------------------

def write_csv(detail_df: pd.DataFrame, output_dir: Path) -> Path:
    """Write full enriched clash list to CSV."""
    path = output_dir / f"{REPORT_BASENAME}.csv"
    detail_df.to_csv(path, index=False)
    logger.info("write_csv: wrote %d rows to %s", len(detail_df), path.name)
    return path


# ---------------------------------------------------------------------------
# Excel output
# ---------------------------------------------------------------------------

def _build_summary_df(detail_df: pd.DataFrame) -> pd.DataFrame:
    return pd.DataFrame({
        "Metric": [
            "Total Clashes",
            "Critical",
            "High",
            "Medium",
            "Low",
            "Unique Groups",
        ],
        "Value": [
            len(detail_df),
            (detail_df["Priority"] == "Critical").sum(),
            (detail_df["Priority"] == "High").sum(),
            (detail_df["Priority"] == "Medium").sum(),
            (detail_df["Priority"] == "Low").sum(),
            detail_df["GroupKey"].nunique(),
        ],
    })


def _build_discipline_df(detail_df: pd.DataFrame) -> pd.DataFrame:
    return (
        detail_df
        .groupby(["DisciplineA", "DisciplineB"])
        .agg(ClashCount=("ClashID", "count"))
        .reset_index()
        .sort_values("ClashCount", ascending=False)
        .reset_index(drop=True)
    )


def _build_highrisk_df(detail_df: pd.DataFrame, threshold: int) -> pd.DataFrame:
    group_counts = detail_df.groupby("GroupKey").size().reset_index(name="ClashCount")
    high_risk = group_counts[group_counts["ClashCount"] >= threshold].copy()
    return high_risk.sort_values("ClashCount", ascending=False).reset_index(drop=True)


def write_excel(detail_df: pd.DataFrame, output_dir: Path) -> Path:
    """Write 3-tab Excel report."""
    path = output_dir / f"{REPORT_BASENAME}.xlsx"

    summary_df = _build_summary_df(detail_df)
    discipline_df = _build_discipline_df(detail_df)
    highrisk_df = _build_highrisk_df(detail_df, HIGH_RISK_THRESHOLD)

    with pd.ExcelWriter(path, engine="openpyxl") as writer:
        summary_df.to_excel(writer, sheet_name=EXCEL_SHEET_SUMMARY, index=False)
        discipline_df.to_excel(writer, sheet_name=EXCEL_SHEET_DISCIPLINE, index=False)
        highrisk_df.to_excel(writer, sheet_name=EXCEL_SHEET_HIGHRISK, index=False)

    logger.info("write_excel: wrote 3-tab report to %s", path.name)
    return path


# ---------------------------------------------------------------------------
# PDF output
# ---------------------------------------------------------------------------

def write_pdf(detail_df: pd.DataFrame, output_dir: Path) -> Path:
    """Write 1-page PDF summary for the Friday coordination meeting."""
    path = output_dir / f"{REPORT_BASENAME}.pdf"
    doc = SimpleDocTemplate(str(path), pagesize=letter,
                            topMargin=0.75 * inch, bottomMargin=0.75 * inch)
    styles = getSampleStyleSheet()
    story = []

    # Title
    story.append(Paragraph(PDF_TITLE, styles["Title"]))
    story.append(Paragraph(f"Generated: {date.today().strftime('%B %d, %Y')}", styles["Normal"]))
    story.append(Spacer(1, 0.2 * inch))

    # Summary table
    story.append(Paragraph("Project Summary", styles["Heading2"]))
    summary_df = _build_summary_df(detail_df)
    summary_data = [summary_df.columns.tolist()] + summary_df.values.tolist()
    summary_table = Table(summary_data, colWidths=[3 * inch, 2 * inch])
    summary_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#2F5496")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#EEF2F8")]),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("FONTSIZE", (0, 0), (-1, -1), 10),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ]))
    story.append(summary_table)
    story.append(Spacer(1, 0.2 * inch))

    # Discipline breakdown (top 10)
    story.append(Paragraph("Discipline Clash Breakdown (Top 10)", styles["Heading2"]))
    disc_df = _build_discipline_df(detail_df).head(10)
    disc_data = [disc_df.columns.tolist()] + disc_df.values.tolist()
    disc_table = Table(disc_data, colWidths=[2.5 * inch, 2.5 * inch, 1.5 * inch])
    disc_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#2F5496")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#EEF2F8")]),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("FONTSIZE", (0, 0), (-1, -1), 10),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ]))
    story.append(disc_table)
    story.append(Spacer(1, 0.2 * inch))

    # High risk areas
    highrisk_df = _build_highrisk_df(detail_df, HIGH_RISK_THRESHOLD)
    if not highrisk_df.empty:
        story.append(Paragraph(
            f"High Risk Areas (≥{HIGH_RISK_THRESHOLD} clashes)", styles["Heading2"]
        ))
        hr_data = [highrisk_df.columns.tolist()] + highrisk_df.values.tolist()
        hr_table = Table(hr_data, colWidths=[4 * inch, 2 * inch])
        hr_table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#C00000")),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#FFF0F0")]),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
            ("FONTSIZE", (0, 0), (-1, -1), 10),
            ("LEFTPADDING", (0, 0), (-1, -1), 6),
            ("RIGHTPADDING", (0, 0), (-1, -1), 6),
            ("TOPPADDING", (0, 0), (-1, -1), 6),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ]))
        story.append(hr_table)

    doc.build(story)
    logger.info("write_pdf: wrote PDF summary to %s", path.name)
    return path


# ---------------------------------------------------------------------------
# Main entry point
# ---------------------------------------------------------------------------

def run(detail_df: pd.DataFrame, output_dir: Path) -> dict[str, Path]:
    """
    Generate all three report formats.

    Args:
        detail_df  — enriched, prioritized clash DataFrame
        output_dir — directory to write outputs

    Returns:
        dict with keys 'csv', 'excel', 'pdf' mapping to output Paths
    """
    logger.info("report_generator: starting")
    output_dir.mkdir(parents=True, exist_ok=True)

    outputs = {
        "csv": write_csv(detail_df, output_dir),
        "excel": write_excel(detail_df, output_dir),
        "pdf": write_pdf(detail_df, output_dir),
    }

    logger.info("report_generator: complete — 3 files written to %s", output_dir)
    return outputs
