"""
bim_utils.py — Shared utilities for BIMTools.extension scripts.

pyRevit automatically adds BIMTools.extension/lib/ to sys.path.
Import in any script with: from bim_utils import append_csv, confirm, ...
"""
import os
import csv
from datetime import date

import clr
clr.AddReference("RevitAPI")
from Autodesk.Revit.DB import (
    FilteredElementCollector,
    View,
    Family,
    RevitLinkInstance,
    ImportInstance,
    WorksetKind,
    FilteredWorksetCollector,
)

from pyrevit import forms

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------
OUTPUT_DIR = r"C:\BIM_Automation\data\output"


# ---------------------------------------------------------------------------
# Date helper
# ---------------------------------------------------------------------------
def today():
    return date.today().isoformat()


# ---------------------------------------------------------------------------
# CSV helpers
# ---------------------------------------------------------------------------
def append_csv(filename, headers, row):
    """Append one row to OUTPUT_DIR/filename. Creates file+headers if missing."""
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    path = os.path.join(OUTPUT_DIR, filename)
    write_header = not os.path.exists(path)
    with open(path, "a", newline="") as f:
        w = csv.writer(f)
        if write_header:
            w.writerow(headers)
        w.writerow(row)
    return path


def write_csv(filename, headers, rows):
    """Write CSV to OUTPUT_DIR/filename, overwriting if it exists."""
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    path = os.path.join(OUTPUT_DIR, filename)
    with open(path, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(headers)
        w.writerows(rows)
    return path


# ---------------------------------------------------------------------------
# UI helper
# ---------------------------------------------------------------------------
def confirm(message):
    """Show alert dialog with Yes/No. Returns True if user clicks Yes."""
    return forms.alert(message, yes=True, no=True)


# ---------------------------------------------------------------------------
# Revit element collectors
# ---------------------------------------------------------------------------
def get_warnings(doc):
    """Return list of all FailureMessage objects in the document."""
    return list(doc.GetWarnings())


def get_views(doc, exclude_templates=True):
    """Return list of View elements. Excludes view templates by default."""
    views = list(FilteredElementCollector(doc).OfClass(View).ToElements())
    if exclude_templates:
        return [v for v in views if not v.IsTemplate]
    return views


def get_families(doc):
    """Return list of all Family elements in the document."""
    return list(FilteredElementCollector(doc).OfClass(Family).ToElements())


def get_links(doc):
    """Return list of all RevitLinkInstance elements."""
    return list(FilteredElementCollector(doc).OfClass(RevitLinkInstance).ToElements())


def get_import_instances(doc):
    """Return list of all ImportInstance elements (CAD imports)."""
    return list(FilteredElementCollector(doc).OfClass(ImportInstance).ToElements())


def get_worksets(doc):
    """Return list of user worksets. Returns [] if model is not workshared."""
    if not doc.IsWorkshared:
        return []
    return list(
        FilteredWorksetCollector(doc).OfKind(WorksetKind.UserWorkset).ToWorksets()
    )
