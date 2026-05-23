"""
metadata_writer.py — Stage 5: Pipeline Metadata Writer

Appends one row per pipeline run to pipeline_metadata.csv in the output directory.
Rows accumulate over time so Power BI can show run history and a "last updated" card.

Called by main.py as a non-blocking Stage 5.
"""

import csv
import logging
from datetime import datetime
from pathlib import Path

log = logging.getLogger(__name__)

METADATA_FILE = "pipeline_metadata.csv"

COLUMNS = [
    "RunDate",
    "RunTimestamp",
    "StagesCompleted",
    "ClashesProcessed",
    "InputFilesFound",
    "PipelineStatus",
]


def run(
    output_dir: Path,
    stages_completed: int,
    clashes_processed: int,
    input_files_found: int,
    status: str,
) -> None:
    """Append a metadata row for this pipeline run."""
    output_dir.mkdir(parents=True, exist_ok=True)
    now = datetime.now()
    row = [
        now.strftime("%Y-%m-%d"),
        now.strftime("%Y-%m-%d %H:%M:%S"),
        stages_completed,
        clashes_processed,
        input_files_found,
        status,
    ]

    dest = output_dir / METADATA_FILE
    write_header = not dest.exists()

    with dest.open("a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if write_header:
            writer.writerow(COLUMNS)
        writer.writerow(row)

    log.info("Stage 5 complete: row appended to %s", METADATA_FILE)
