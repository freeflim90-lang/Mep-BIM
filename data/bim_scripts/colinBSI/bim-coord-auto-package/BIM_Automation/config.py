"""
config.py — Central configuration for BIM Automation Pipeline
Edit paths and thresholds here. Do not modify other modules for configuration.
"""

from pathlib import Path

# --- Directory paths ---
BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"
INPUT_DIR = DATA_DIR / "input"
OUTPUT_DIR = DATA_DIR / "output"
ARCHIVE_DIR = DATA_DIR / "archive"
LOG_DIR = BASE_DIR / "logs"
LOG_FILE = LOG_DIR / "pipeline.log"

# --- Clash priority rules ---
# Discipline pairs containing these strings are elevated to Critical or High.
CRITICAL_DISCIPLINES = {"Structure", "Structural"}
HIGH_DISCIPLINES = {"Mechanical", "Plumbing"}

# --- Report settings ---
REPORT_BASENAME = "weekly_coordination_report"  # extensions added automatically
PDF_TITLE = "BIM Weekly Coordination Summary"
EXCEL_SHEET_SUMMARY = "Summary"
EXCEL_SHEET_DISCIPLINE = "Discipline Breakdown"
EXCEL_SHEET_HIGHRISK = "High Risk Areas"
HIGH_RISK_THRESHOLD = 20  # groups with >= this many clashes appear in High Risk tab

# --- Logging ---
LOG_MAX_BYTES = 5 * 1024 * 1024   # 5 MB per log file
LOG_BACKUP_COUNT = 6               # ~6 weeks of history at weekly runs

# --- Phase 2 placeholders (not yet active) ---
# ACC_CLIENT_ID = ""
# ACC_CLIENT_SECRET = ""
# ACC_PROJECT_ID = ""
# ACC_ISSUE_ENDPOINT = "https://developer.api.autodesk.com/issues/v1/issues"
