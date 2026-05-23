"""
CreateSheets — Creates 5 standard BIM coordination sheets.
Idempotent: skips sheets whose sheet number already exists.
Uses first loaded title block, or ElementId.InvalidElementId if none.
"""
import traceback

import clr
clr.AddReference("RevitAPI")
from Autodesk.Revit.DB import (
    FilteredElementCollector,
    FamilySymbol,
    BuiltInCategory,
    ViewSheet,
    Transaction,
    ElementId,
)

from pyrevit import revit, script

doc = revit.doc
output = script.get_output()

# (sheet_number, sheet_name)
STANDARD_SHEETS = [
    ("G000", "Cover"),
    ("G001", "General Notes"),
    ("G100", "Level Plans"),
    ("G200", "Sections"),
    ("G300", "Coordination"),
]


def get_title_block_id():
    title_blocks = list(
        FilteredElementCollector(doc)
        .OfCategory(BuiltInCategory.OST_TitleBlocks)
        .OfClass(FamilySymbol)
        .ToElements()
    )
    if title_blocks:
        return title_blocks[0].Id
    return ElementId.InvalidElementId


def run():
    existing_numbers = {
        s.SheetNumber
        for s in FilteredElementCollector(doc).OfClass(ViewSheet).ToElements()
    }

    to_create = [
        (num, name)
        for num, name in STANDARD_SHEETS
        if num not in existing_numbers
    ]

    if not to_create:
        output.print_md("**Done:** All 5 standard sheets already exist.")
        return

    tb_id = get_title_block_id()

    with Transaction(doc, "Create Standard Sheets") as t:
        t.Start()
        for num, name in to_create:
            sheet = ViewSheet.Create(doc, tb_id)
            sheet.SheetNumber = num
            sheet.Name = name
        t.Commit()

    output.print_md(
        "**Created {} sheet(s):** {}".format(
            len(to_create),
            ", ".join("{} {}".format(n, nm) for n, nm in to_create),
        )
    )
    skipped = len(STANDARD_SHEETS) - len(to_create)
    if skipped:
        output.print_md("**Skipped {} already existing.**".format(skipped))


try:
    run()
except Exception:
    output.print_md("**Error:**")
    output.print_md("```\n{}\n```".format(traceback.format_exc()))
