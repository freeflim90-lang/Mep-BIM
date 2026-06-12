"""
main.py — BIM Automation Pipeline Master Runner

Runs the full coordination pipeline in sequence:
    0. Clash XML Parser    (clash_processing/clash_parser.py)   ← skipped if no XML
    1. Clash Grouping      (clash_processing/clash_grouper.py)
    2. Clash Prioritization (clash_processing/clash_prioritizer.py)
    3. Report Generation   (reports/report_generator.py)
    4. ACC Issue Stub      (acc_integration/issue_stub.py)
    5. Pipeline Metadata  (pipeline_metadata/metadata_writer.py) ← always runs

Schedule this script with Windows Task Scheduler to run every Wednesday.
Entry point: python main.py

Logs to: logs/pipeline.log (rotating, 30-day retention)

Setup:
    pip install pandas openpyxl reportlab
    Place Navisworks CSV exports in: data/input/
    Reports are written to:         data/output/
    Processed CSVs are archived to: data/archive/
"""

import logging
import shutil
import sys
from datetime import datetime
from logging.handlers import RotatingFileHandler
from pathlib import Path

# Add BIM_Automation root to path so modules can import config
sys.path.insert(0, str(Path(__file__).parent))

from config import (
    INPUT_DIR, OUTPUT_DIR, ARCHIVE_DIR, LOG_DIR, LOG_FILE,
    LOG_MAX_BYTES, LOG_BACKUP_COUNT
)
from clash_processing import clash_grouper, clash_prioritizer, clash_parser
from reports import report_generator
from acc_integration import issue_stub
from pipeline_metadata import metadata_writer


# ---------------------------------------------------------------------------
# Logging setup
# ---------------------------------------------------------------------------

def setup_logging() -> None:
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    handler = RotatingFileHandler(
        LOG_FILE,
        maxBytes=LOG_MAX_BYTES,
        backupCount=LOG_BACKUP_COUNT,
        encoding="utf-8"
    )
    formatter = logging.Formatter(
        "%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    handler.setFormatter(formatter)

    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)
    if not root_logger.handlers:
        root_logger.addHandler(handler)

    # Also log to console when running manually
    console = logging.StreamHandler(sys.stdout)
    console.setFormatter(formatter)
    if not any(isinstance(h, logging.StreamHandler) for h in root_logger.handlers):
        root_logger.addHandler(console)


# ---------------------------------------------------------------------------
# Archive helpers
# ---------------------------------------------------------------------------

def archive_inputs(input_dir: Path, archive_dir: Path) -> None:
    """Move processed CSV files from input/ to archive/ with a timestamp prefix."""
    archive_dir.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    moved = 0
    for csv_file in input_dir.glob("*.csv"):
        dest = archive_dir / f"{timestamp}_{csv_file.name}"
        shutil.move(str(csv_file), dest)
        logging.getLogger(__name__).info("Archived %s → %s", csv_file.name, dest.name)
        moved += 1
    logging.getLogger(__name__).info("archive_inputs: %d file(s) archived", moved)


# ---------------------------------------------------------------------------
# Pipeline
# ---------------------------------------------------------------------------

def run_pipeline() -> None:
    logger = logging.getLogger(__name__)
    start_time = datetime.now()
    logger.info("=" * 60)
    logger.info("BIM Automation Pipeline — starting at %s", start_time.strftime("%Y-%m-%d %H:%M:%S"))
    logger.info("=" * 60)

    # Ensure directories exist
    INPUT_DIR.mkdir(parents=True, exist_ok=True)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    stages_completed = 0
    clashes_processed = 0
    input_files_found = len(list(INPUT_DIR.glob("*.csv")))

    # Stage 0: Clash XML Parser (non-blocking — skipped if clash_report.xml absent)
    try:
        clash_count = clash_parser.run(INPUT_DIR, OUTPUT_DIR)
        if clash_count:
            logger.info("Stage 0 complete: %d clashes parsed to clash_heatmap_data.csv", clash_count)
            stages_completed += 1
        else:
            logger.info("Stage 0 skipped: clash_report.xml not found")
    except Exception:
        logger.exception("Stage 0 failed — continuing pipeline without heatmap data")

    # Stage 1: Clash Grouping
    detail_df, summary_df = clash_grouper.run(INPUT_DIR)

    if detail_df.empty:
        logger.warning("Pipeline halted — no clash data found in %s", INPUT_DIR)
        logger.warning("Place Navisworks CSV exports in the input folder and re-run.")
        archive_inputs(INPUT_DIR, ARCHIVE_DIR)
        try:
            metadata_writer.run(
                output_dir=OUTPUT_DIR,
                stages_completed=stages_completed,
                clashes_processed=0,
                input_files_found=input_files_found,
                status="Failed",
            )
        except Exception:
            logger.exception("Stage 5 failed — metadata not written")
        return

    logger.info("Stage 1 complete: %d clashes, %d groups", len(detail_df), len(summary_df))
    stages_completed += 1
    clashes_processed = len(detail_df)

    try:
        # Stage 2: Clash Prioritization
        detail_df = clash_prioritizer.run(detail_df)
        logger.info("Stage 2 complete: priorities assigned")
        stages_completed += 1

        # Stage 3: Report Generation
        outputs = report_generator.run(detail_df, OUTPUT_DIR)
        logger.info("Stage 3 complete: reports written — %s", ", ".join(outputs.keys()))
        stages_completed += 1

        # Stage 4: ACC Issue Stub
        issues = issue_stub.run(detail_df)
        logger.info("Stage 4 complete: %d issues simulated", len(issues))
        stages_completed += 1
    except Exception:
        logger.exception("Pipeline failed — see traceback above. Input CSVs left in place for retry.")
        try:
            metadata_writer.run(
                output_dir=OUTPUT_DIR,
                stages_completed=stages_completed,
                clashes_processed=clashes_processed,
                input_files_found=input_files_found,
                status="Failed",
            )
        except Exception:
            logger.exception("Stage 5 also failed — metadata not written")
        return
    finally:
        # Archive runs whether stages succeed or fail, so files are not reprocessed next week
        archive_inputs(INPUT_DIR, ARCHIVE_DIR)

    # Stage 5: Pipeline Metadata (non-blocking)
    try:
        metadata_writer.run(
            output_dir=OUTPUT_DIR,
            stages_completed=stages_completed,
            clashes_processed=clashes_processed,
            input_files_found=input_files_found,
            status="Success",
        )
    except Exception:
        logger.exception("Stage 5 failed — metadata not written, pipeline still complete")

    elapsed = (datetime.now() - start_time).total_seconds()
    logger.info("=" * 60)
    logger.info("Pipeline complete in %.1f seconds", elapsed)
    logger.info("Reports: %s", OUTPUT_DIR)
    logger.info("=" * 60)


if __name__ == "__main__":
    setup_logging()
    run_pipeline()
