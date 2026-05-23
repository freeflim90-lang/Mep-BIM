# pyRevit BIM Coordinator Toolbar — Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Build 21 production pyRevit scripts across 5 panels of `BIMTools.extension/`, plus a shared utility library.

**Architecture:** Shared lib (`lib/bim_utils.py`) + thin `script.py` per button. pyRevit automatically adds `BIMTools.extension/lib/` to `sys.path` — no path manipulation needed in any script. All scripts import from `bim_utils` directly.

**Tech Stack:** Python 2.7 (IronPython via pyRevit), Revit API (Autodesk.Revit.DB), pyRevit forms/script modules, csv, os, datetime, uuid, tempfile.

**Verification:** This is a documentation-only package — no tests, no git. Verify each task by reading the written file back and confirming it matches the plan.

---

## Task 1: Folder Structure + __init__.py

**Files to create:**
- `BIMTools.extension/lib/__init__.py`
- `BIMTools.extension/Project_Setup.panel/InitializeProject.pushbutton/` (dir marker only — script in Task 8)
- `BIMTools.extension/Project_Setup.panel/CreateWorksets.pushbutton/` (dir marker — script in Task 3)
- `BIMTools.extension/Project_Setup.panel/LoadSharedParams.pushbutton/` (dir marker — script in Task 4)
- `BIMTools.extension/Project_Setup.panel/SetupViews.pushbutton/` (dir marker — script in Task 5)
- `BIMTools.extension/Project_Setup.panel/CreateSheets.pushbutton/` (dir marker — script in Task 6)
- `BIMTools.extension/Project_Setup.panel/BrowserOrg.pushbutton/` (dir marker — script in Task 7)
- `BIMTools.extension/Model_Health.panel/WarningManager.pushbutton/` (dir marker — script in Task 9)
- `BIMTools.extension/Model_Health.panel/FindCADImports.pushbutton/` (dir marker — script in Task 10)
- `BIMTools.extension/Model_Health.panel/FindLargeFamilies.pushbutton/` (dir marker — script in Task 11)
- `BIMTools.extension/Model_Health.panel/GroupInspector.pushbutton/` (dir marker — script in Task 12)
- `BIMTools.extension/Model_Health.panel/UnplacedViews.pushbutton/` (dir marker — script in Task 13)
- `BIMTools.extension/Model_Health.panel/UnusedFamilies.pushbutton/` (dir marker — script in Task 14)
- `BIMTools.extension/Coordination.panel/CreateClashViews.pushbutton/` (dir marker — script in Task 15)
- `BIMTools.extension/Coordination.panel/ColorByWorkset.pushbutton/` (dir marker — script in Task 16)
- `BIMTools.extension/Coordination.panel/ColorByDiscipline.pushbutton/` (dir marker — script in Task 17)
- `BIMTools.extension/Coordination.panel/ClashStatusManager.pushbutton/` (dir marker — script in Task 18)
- `BIMTools.extension/Coordination.panel/ZoneChecker.pushbutton/` (dir marker — script in Task 19)
- `BIMTools.extension/Coordination.panel/InterferenceCheck.pushbutton/` (dir marker — script in Task 20)
- `BIMTools.extension/Reporting.panel/CoordReport.pushbutton/` (dir marker — script in Task 21)
- `BIMTools.extension/Reporting.panel/ClashSummary.pushbutton/` (dir marker — script in Task 22)
- `BIMTools.extension/Utilities.panel/SyncAndClose.pushbutton/` (dir marker — script in Task 23)

**Step 1: Create `lib/__init__.py`**

```python
# BIMTools.extension/lib/__init__.py
```

**Step 2: Verify**

Read `BIMTools.extension/lib/__init__.py` — should exist and be empty (one comment line).

---

## Task 2: Shared Library — `lib/bim_utils.py`

**File:** `BIMTools.extension/lib/bim_utils.py`

```python
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
```

**Step 1: Write the file** (above content to `BIMTools.extension/lib/bim_utils.py`)

**Step 2: Verify**

Read the file back — confirm `OUTPUT_DIR`, `append_csv`, `write_csv`, `confirm`, and all six collectors are present.

---

## Task 3: Panel 1 — CreateWorksets

**File:** `BIMTools.extension/Project_Setup.panel/CreateWorksets.pushbutton/script.py`

Creates the 11 standard worksets. Idempotent — skips any workset that already exists by name.

```python
"""
CreateWorksets — Creates 11 standard BIM coordination worksets.
Idempotent: skips worksets that already exist.
"""
import traceback

import clr
clr.AddReference("RevitAPI")
from Autodesk.Revit.DB import Transaction, WorksetKind, FilteredWorksetCollector

from pyrevit import revit, script

doc = revit.doc
output = script.get_output()

STANDARD_WORKSETS = [
    "Shared Levels & Grids",
    "Arch",
    "Structure",
    "Mechanical",
    "Electrical",
    "Plumbing",
    "Civil",
    "Plant",
    "Links",
    "Coordination",
    "Scan",
]


def run():
    if not doc.IsWorkshared:
        output.print_md("**Error:** This model is not workshared. Enable worksharing first.")
        return

    existing = {
        ws.Name
        for ws in FilteredWorksetCollector(doc)
        .OfKind(WorksetKind.UserWorkset)
        .ToWorksets()
    }

    to_create = [name for name in STANDARD_WORKSETS if name not in existing]

    if not to_create:
        output.print_md("**Done:** All 11 standard worksets already exist.")
        return

    with Transaction(doc, "Create Standard Worksets") as t:
        t.Start()
        for name in to_create:
            from Autodesk.Revit.DB import Workset as WS
            WS.Create(doc, name)
        t.Commit()

    output.print_md(
        "**Created {} workset(s):** {}".format(len(to_create), ", ".join(to_create))
    )
    skipped = len(STANDARD_WORKSETS) - len(to_create)
    if skipped:
        output.print_md("**Skipped {} already existing.**".format(skipped))


try:
    run()
except Exception:
    output.print_md("**Error:**")
    output.print_md("```\n{}\n```".format(traceback.format_exc()))
```

**Step 1: Write the file** (above content)

**Step 2: Verify**

Read the file back — confirm `STANDARD_WORKSETS` has 11 items, idempotent check using `existing` set, Transaction wraps `Workset.Create`.

---

## Task 4: Panel 1 — LoadSharedParams

**File:** `BIMTools.extension/Project_Setup.panel/LoadSharedParams.pushbutton/script.py`

Adds 6 coordination parameters to the Project Information category. Creates a temporary shared parameter file, registers the parameters, then restores the original shared parameter file path.

```python
"""
LoadSharedParams — Adds 6 BIM coordination parameters to Project Information.
Idempotent: skips parameters that already exist in the model.

Parameters added (all Text type, Project Information category):
  Clash_Status, Issue_ID, Issue_Status, Coordination_Zone, Discipline, Model_Author

Note: For Revit 2022+ replace ParameterType.Text with
      SpecTypeId.String.Text (ForgeTypeId). The logic is identical.
"""
import os
import tempfile
import traceback
import uuid

import clr
clr.AddReference("RevitAPI")
from Autodesk.Revit.DB import (
    Transaction,
    BuiltInCategory,
    BuiltInParameterGroup,
    ExternalDefinitionCreationOptions,
)

try:
    # Revit 2021 and earlier
    from Autodesk.Revit.DB import ParameterType
    TEXT_TYPE = ParameterType.Text
    USE_FORGE = False
except ImportError:
    # Revit 2022+
    from Autodesk.Revit.DB import SpecTypeId
    TEXT_TYPE = SpecTypeId.String.Text
    USE_FORGE = True

from pyrevit import revit, script

doc = revit.doc
app = doc.Application
output = script.get_output()

PARAMS = [
    "Clash_Status",
    "Issue_ID",
    "Issue_Status",
    "Coordination_Zone",
    "Discipline",
    "Model_Author",
]
GROUP_NAME = "BIM Coordination"


def build_spf_content():
    lines = [
        "# This is a Revit shared parameter file.",
        "# Do not edit manually.",
        "*META\tVERSION\tMINVERSION",
        "META\t2\t1",
        "*GROUP\tID\tNAME",
        "GROUP\t1\t" + GROUP_NAME,
        "*PARAM\tGUID\tNAME\tDATATYPE\tDATACATEGORY\tGROUP\tVISIBLE\tDESCRIPTION\tUSERMODIFIABLE\tHIDEWHENNOVALUEISASSIGNED",
    ]
    for name in PARAMS:
        guid = str(uuid.uuid4())
        lines.append(
            "PARAM\t{}\t{}\tTEXT\t\t1\t1\t\t1\t0".format(guid, name)
        )
    return "\n".join(lines) + "\n"


def run():
    # Check which params already exist
    existing_params = set()
    it = doc.ParameterBindings.ForwardIterator()
    while it.MoveNext():
        existing_params.add(it.Key.Name)

    needed = [p for p in PARAMS if p not in existing_params]
    if not needed:
        output.print_md("**Done:** All 6 parameters already exist in this model.")
        return

    # Write temp shared parameter file
    tmp_path = tempfile.mktemp(suffix=".txt")
    with open(tmp_path, "w") as f:
        f.write(build_spf_content())

    old_spf = app.SharedParametersFilename
    try:
        app.SharedParametersFilename = tmp_path
        def_file = app.OpenSharedParameterFile()
        param_group = def_file.Groups.get_Item(GROUP_NAME)

        # Build category set for Project Information
        cat = doc.Settings.Categories.get_Item(
            BuiltInCategory.OST_ProjectInformation
        )
        cat_set = app.Create.NewCategorySet()
        cat_set.Insert(cat)
        binding = app.Create.NewInstanceBinding(cat_set)

        with Transaction(doc, "Load Shared Parameters") as t:
            t.Start()
            for ext_def in param_group.Definitions:
                if ext_def.Name not in needed:
                    continue
                doc.ParameterBindings.Insert(
                    ext_def, binding, BuiltInParameterGroup.PG_DATA
                )
            t.Commit()

    finally:
        app.SharedParametersFilename = old_spf
        try:
            os.remove(tmp_path)
        except OSError:
            pass

    output.print_md(
        "**Added {} parameter(s):** {}".format(len(needed), ", ".join(needed))
    )
    skipped = len(PARAMS) - len(needed)
    if skipped:
        output.print_md("**Skipped {} already existing.**".format(skipped))


try:
    run()
except Exception:
    output.print_md("**Error:**")
    output.print_md("```\n{}\n```".format(traceback.format_exc()))
```

**Step 1: Write the file** (above content)

**Step 2: Verify**

Read the file back — confirm `PARAMS` has 6 items, temp file created and cleaned up in `finally`, idempotent iterator check, `try/except ImportError` for ParameterType/ForgeTypeId.

---

## Task 5: Panel 1 — SetupViews

**File:** `BIMTools.extension/Project_Setup.panel/SetupViews.pushbutton/script.py`

Creates 7 standard 3D views. Idempotent — skips any view whose name already exists.

```python
"""
SetupViews — Creates 7 standard BIM coordination 3D views.
Idempotent: skips views that already exist by name.
"""
import traceback

import clr
clr.AddReference("RevitAPI")
from Autodesk.Revit.DB import (
    FilteredElementCollector,
    ViewFamilyType,
    ViewFamily,
    View3D,
    Transaction,
    View,
)

from pyrevit import revit, script

doc = revit.doc
output = script.get_output()

STANDARD_VIEWS = [
    "3D - Coordination",
    "3D - Navisworks",
    "3D - Clash Review",
    "3D - Worksets",
    "3D - Linked Models",
    "3D - QAQC",
    "3D - Scan Reference",
]


def get_3d_view_family_type():
    for vft in FilteredElementCollector(doc).OfClass(ViewFamilyType).ToElements():
        if vft.ViewFamily == ViewFamily.ThreeDimensional:
            return vft
    return None


def run():
    vft = get_3d_view_family_type()
    if vft is None:
        output.print_md("**Error:** No 3D ViewFamilyType found in this model.")
        return

    existing_names = {
        v.Name
        for v in FilteredElementCollector(doc).OfClass(View).ToElements()
        if not v.IsTemplate
    }

    to_create = [name for name in STANDARD_VIEWS if name not in existing_names]

    if not to_create:
        output.print_md("**Done:** All 7 standard 3D views already exist.")
        return

    with Transaction(doc, "Create Standard 3D Views") as t:
        t.Start()
        for name in to_create:
            view = View3D.CreateIsometric(doc, vft.Id)
            view.Name = name
        t.Commit()

    output.print_md(
        "**Created {} view(s):** {}".format(len(to_create), ", ".join(to_create))
    )
    skipped = len(STANDARD_VIEWS) - len(to_create)
    if skipped:
        output.print_md("**Skipped {} already existing.**".format(skipped))


try:
    run()
except Exception:
    output.print_md("**Error:**")
    output.print_md("```\n{}\n```".format(traceback.format_exc()))
```

**Step 1: Write the file** (above content)

**Step 2: Verify**

Read the file back — confirm `STANDARD_VIEWS` has 7 items, `View3D.CreateIsometric` call, idempotent name check.

---

## Task 6: Panel 1 — CreateSheets

**File:** `BIMTools.extension/Project_Setup.panel/CreateSheets.pushbutton/script.py`

Creates 5 standard sheets. Idempotent — skips sheets with matching sheet numbers. Uses the first available title block, or no title block if none are loaded.

```python
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
```

**Step 1: Write the file** (above content)

**Step 2: Verify**

Read the file back — confirm `STANDARD_SHEETS` has 5 tuples, idempotent `SheetNumber` check, `ElementId.InvalidElementId` fallback.

---

## Task 7: Panel 1 — BrowserOrg

**File:** `BIMTools.extension/Project_Setup.panel/BrowserOrg.pushbutton/script.py`

Applies browser organization by Type/Discipline. Looks for an existing browser organization whose name contains "Discipline" or "Type" and applies it. If none found, prints setup guidance.

```python
"""
BrowserOrg — Applies project browser organization by Type then Discipline.
Looks for an existing BrowserOrganization containing "Discipline" or "Type".
If none found, prints manual setup instructions.
"""
import traceback

import clr
clr.AddReference("RevitAPI")
from Autodesk.Revit.DB import BrowserOrganization

from pyrevit import revit, script

doc = revit.doc
output = script.get_output()

PREFERRED_KEYWORDS = ["discipline", "type"]


def run():
    all_orgs = list(BrowserOrganization.GetAllBrowserOrganization(doc))

    # Find best match: prefer org whose name contains a keyword
    match = None
    for keyword in PREFERRED_KEYWORDS:
        for org in all_orgs:
            if keyword in org.Name.lower():
                match = org
                break
        if match:
            break

    if match is None:
        output.print_md("**No matching browser organization found.**")
        output.print_md(
            "To configure manually: View tab → User Interface → "
            "Browser Organization → Views tab → select or create "
            "a Type/Discipline grouping."
        )
        output.print_md(
            "**Available organizations:** {}".format(
                ", ".join(o.Name for o in all_orgs) or "none"
            )
        )
        return

    BrowserOrganization.SetCurrentBrowserOrganizationForViews(doc, match.Id)
    output.print_md(
        "**Applied browser organization:** {}".format(match.Name)
    )


try:
    run()
except Exception:
    output.print_md("**Error:**")
    output.print_md("```\n{}\n```".format(traceback.format_exc()))
```

**Step 1: Write the file** (above content)

**Step 2: Verify**

Read the file back — confirm keyword search, `SetCurrentBrowserOrganizationForViews`, and manual guidance fallback.

---

## Task 8: Panel 1 — InitializeProject

**File:** `BIMTools.extension/Project_Setup.panel/InitializeProject.pushbutton/script.py`

Runs all 5 setup scripts in sequence after a confirmation dialog. This is the only Project Setup tool requiring confirmation (destructive in intent — creates many model elements at once).

```python
"""
InitializeProject — Runs all 5 Project Setup tools in sequence.
Requires confirmation before proceeding.
"""
import traceback

import clr
clr.AddReference("RevitAPI")
from Autodesk.Revit.DB import (
    Transaction,
    WorksetKind,
    FilteredWorksetCollector,
    ViewFamilyType,
    ViewFamily,
    View3D,
    View,
    FilteredElementCollector,
    FamilySymbol,
    BuiltInCategory,
    ViewSheet,
    ElementId,
    BrowserOrganization,
)

try:
    from Autodesk.Revit.DB import ParameterType
    TEXT_TYPE = ParameterType.Text
except ImportError:
    from Autodesk.Revit.DB import SpecTypeId
    TEXT_TYPE = SpecTypeId.String.Text

from Autodesk.Revit.DB import (
    ExternalDefinitionCreationOptions,
    BuiltInParameterGroup,
)

import os
import tempfile
import uuid

from pyrevit import revit, script, forms

doc = revit.doc
app = doc.Application
output = script.get_output()

# ---- Constants (mirrored from individual scripts) ----
STANDARD_WORKSETS = [
    "Shared Levels & Grids", "Arch", "Structure", "Mechanical",
    "Electrical", "Plumbing", "Civil", "Plant", "Links",
    "Coordination", "Scan",
]

PARAMS = [
    "Clash_Status", "Issue_ID", "Issue_Status",
    "Coordination_Zone", "Discipline", "Model_Author",
]
PARAM_GROUP_NAME = "BIM Coordination"

STANDARD_VIEWS = [
    "3D - Coordination", "3D - Navisworks", "3D - Clash Review",
    "3D - Worksets", "3D - Linked Models", "3D - QAQC",
    "3D - Scan Reference",
]

STANDARD_SHEETS = [
    ("G000", "Cover"), ("G001", "General Notes"),
    ("G100", "Level Plans"), ("G200", "Sections"),
    ("G300", "Coordination"),
]


# ---- Step functions ----

def step_worksets():
    if not doc.IsWorkshared:
        return "SKIP (model not workshared)"
    existing = {
        ws.Name
        for ws in FilteredWorksetCollector(doc)
        .OfKind(WorksetKind.UserWorkset).ToWorksets()
    }
    to_create = [n for n in STANDARD_WORKSETS if n not in existing]
    if not to_create:
        return "already exist"
    from Autodesk.Revit.DB import Workset as WS
    with Transaction(doc, "Create Worksets") as t:
        t.Start()
        for name in to_create:
            WS.Create(doc, name)
        t.Commit()
    return "created {}".format(len(to_create))


def step_shared_params():
    existing_params = set()
    it = doc.ParameterBindings.ForwardIterator()
    while it.MoveNext():
        existing_params.add(it.Key.Name)
    needed = [p for p in PARAMS if p not in existing_params]
    if not needed:
        return "already exist"

    lines = [
        "# This is a Revit shared parameter file.",
        "# Do not edit manually.",
        "*META\tVERSION\tMINVERSION",
        "META\t2\t1",
        "*GROUP\tID\tNAME",
        "GROUP\t1\t" + PARAM_GROUP_NAME,
        "*PARAM\tGUID\tNAME\tDATATYPE\tDATACATEGORY\tGROUP\tVISIBLE\tDESCRIPTION\tUSERMODIFIABLE\tHIDEWHENNOVALUEISASSIGNED",
    ]
    for name in PARAMS:
        lines.append("PARAM\t{}\t{}\tTEXT\t\t1\t1\t\t1\t0".format(str(uuid.uuid4()), name))
    spf_content = "\n".join(lines) + "\n"

    tmp_path = tempfile.mktemp(suffix=".txt")
    with open(tmp_path, "w") as f:
        f.write(spf_content)
    old_spf = app.SharedParametersFilename
    try:
        app.SharedParametersFilename = tmp_path
        def_file = app.OpenSharedParameterFile()
        pg = def_file.Groups.get_Item(PARAM_GROUP_NAME)
        cat = doc.Settings.Categories.get_Item(BuiltInCategory.OST_ProjectInformation)
        cat_set = app.Create.NewCategorySet()
        cat_set.Insert(cat)
        binding = app.Create.NewInstanceBinding(cat_set)
        with Transaction(doc, "Load Shared Parameters") as t:
            t.Start()
            for ext_def in pg.Definitions:
                if ext_def.Name in needed:
                    doc.ParameterBindings.Insert(ext_def, binding, BuiltInParameterGroup.PG_DATA)
            t.Commit()
    finally:
        app.SharedParametersFilename = old_spf
        try:
            os.remove(tmp_path)
        except OSError:
            pass
    return "added {}".format(len(needed))


def step_views():
    vft = None
    for v in FilteredElementCollector(doc).OfClass(ViewFamilyType).ToElements():
        if v.ViewFamily == ViewFamily.ThreeDimensional:
            vft = v
            break
    if vft is None:
        return "SKIP (no 3D ViewFamilyType)"
    existing = {
        v.Name
        for v in FilteredElementCollector(doc).OfClass(View).ToElements()
        if not v.IsTemplate
    }
    to_create = [n for n in STANDARD_VIEWS if n not in existing]
    if not to_create:
        return "already exist"
    with Transaction(doc, "Create 3D Views") as t:
        t.Start()
        for name in to_create:
            view = View3D.CreateIsometric(doc, vft.Id)
            view.Name = name
        t.Commit()
    return "created {}".format(len(to_create))


def step_sheets():
    existing = {
        s.SheetNumber
        for s in FilteredElementCollector(doc).OfClass(ViewSheet).ToElements()
    }
    to_create = [(n, nm) for n, nm in STANDARD_SHEETS if n not in existing]
    if not to_create:
        return "already exist"
    tbs = list(
        FilteredElementCollector(doc)
        .OfCategory(BuiltInCategory.OST_TitleBlocks)
        .OfClass(FamilySymbol).ToElements()
    )
    tb_id = tbs[0].Id if tbs else ElementId.InvalidElementId
    with Transaction(doc, "Create Sheets") as t:
        t.Start()
        for num, name in to_create:
            sheet = ViewSheet.Create(doc, tb_id)
            sheet.SheetNumber = num
            sheet.Name = name
        t.Commit()
    return "created {}".format(len(to_create))


def step_browser_org():
    all_orgs = list(BrowserOrganization.GetAllBrowserOrganization(doc))
    match = None
    for kw in ["discipline", "type"]:
        for org in all_orgs:
            if kw in org.Name.lower():
                match = org
                break
        if match:
            break
    if match is None:
        return "no matching org found — configure manually"
    BrowserOrganization.SetCurrentBrowserOrganizationForViews(doc, match.Id)
    return "applied '{}'".format(match.Name)


# ---- Main ----

def run():
    if not forms.alert(
        "Initialize Project will create worksets, parameters, views, and sheets.\n"
        "This is safe to run on a new project. Proceed?",
        yes=True, no=True,
    ):
        output.print_md("**Cancelled.**")
        return

    steps = [
        ("Worksets", step_worksets),
        ("Shared Parameters", step_shared_params),
        ("3D Views", step_views),
        ("Sheets", step_sheets),
        ("Browser Organization", step_browser_org),
    ]

    for label, fn in steps:
        try:
            result = fn()
            output.print_md("**{}:** {}".format(label, result))
        except Exception:
            output.print_md("**{} ERROR:**".format(label))
            output.print_md("```\n{}\n```".format(traceback.format_exc()))

    output.print_md("**Initialize Project complete.**")


try:
    run()
except Exception:
    output.print_md("**Fatal Error:**")
    output.print_md("```\n{}\n```".format(traceback.format_exc()))
```

**Step 1: Write the file** (above content)

**Step 2: Verify**

Read the file back — confirm `forms.alert` confirmation, all 5 step functions called, each wrapped in try/except.

---

## Task 9: Panel 2 — WarningManager

**File:** `BIMTools.extension/Model_Health.panel/WarningManager.pushbutton/script.py`

Collects all model warnings, groups by description, outputs `warnings_report.csv`.

```python
"""
WarningManager — Exports model warnings summary to warnings_report.csv.
Columns: Description, Count, Severity
Read-only. No model changes.
"""
import traceback
from collections import defaultdict

from bim_utils import write_csv, today

from pyrevit import revit, script

doc = revit.doc
output = script.get_output()

FILENAME = "warnings_report.csv"
HEADERS = ["RunDate", "ModelName", "Description", "Count", "Severity"]


def classify_severity(description):
    desc_lower = description.lower()
    if any(kw in desc_lower for kw in ["error", "corrupt", "missing", "unresolved"]):
        return "Critical"
    if any(kw in desc_lower for kw in ["overlap", "duplicate", "identical"]):
        return "High"
    return "Medium"


def run():
    warnings = list(doc.GetWarnings())

    if not warnings:
        output.print_md("**No warnings found in this model.**")
        return

    counts = defaultdict(int)
    for w in warnings:
        counts[w.GetDescriptionText()] += 1

    run_date = today()
    model_name = doc.Title
    rows = []
    for desc, count in sorted(counts.items(), key=lambda x: -x[1]):
        rows.append([run_date, model_name, desc, count, classify_severity(desc)])

    path = write_csv(FILENAME, HEADERS, rows)
    output.print_md(
        "**Warnings report written:** `{}`  \n"
        "Total warnings: {} across {} unique descriptions.".format(
            path, len(warnings), len(counts)
        )
    )


try:
    run()
except Exception:
    output.print_md("**Error:**")
    output.print_md("```\n{}\n```".format(traceback.format_exc()))
```

**Step 1: Write the file** (above content)

**Step 2: Verify**

Read the file back — confirm `from bim_utils import write_csv, today`, `GetWarnings()`, severity classification, CSV output.

---

## Task 10: Panel 2 — FindCADImports

**File:** `BIMTools.extension/Model_Health.panel/FindCADImports.pushbutton/script.py`

Finds all CAD import instances, outputs `cad_imports_report.csv`.

```python
"""
FindCADImports — Reports all CAD imports in the model.
Columns: RunDate, ModelName, ElementID, Name, Workset, ViewName
Read-only. No model changes.
"""
import traceback

import clr
clr.AddReference("RevitAPI")
from Autodesk.Revit.DB import ImportInstance, WorksetKind, FilteredWorksetCollector

from bim_utils import write_csv, today, get_import_instances

from pyrevit import revit, script

doc = revit.doc
output = script.get_output()

FILENAME = "cad_imports_report.csv"
HEADERS = ["RunDate", "ModelName", "ElementID", "Name", "Workset", "ViewName"]


def get_workset_name(elem):
    if not doc.IsWorkshared:
        return "N/A"
    ws_param = elem.get_Parameter(
        __import__("Autodesk.Revit.DB", fromlist=["BuiltInParameter"]).BuiltInParameter.ELEM_PARTITION_PARAM
    )
    if ws_param:
        ws_id = ws_param.AsElementId()
        ws = doc.GetWorksetTable().GetWorkset(ws_id)
        return ws.Name if ws else "Unknown"
    return "Unknown"


def get_view_name(elem):
    view_id = elem.OwnerViewId
    if view_id and view_id.IntegerValue != -1:
        view = doc.GetElement(view_id)
        return view.Name if view else "Unknown"
    return "Model (not view-specific)"


def run():
    imports = get_import_instances(doc)
    if not imports:
        output.print_md("**No CAD imports found in this model.**")
        return

    run_date = today()
    model_name = doc.Title
    rows = []
    for imp in imports:
        rows.append([
            run_date,
            model_name,
            imp.Id.IntegerValue,
            imp.Category.Name if imp.Category else "Unknown",
            get_workset_name(imp),
            get_view_name(imp),
        ])

    path = write_csv(FILENAME, HEADERS, rows)
    output.print_md(
        "**CAD imports report written:** `{}`  \n"
        "{} import(s) found.".format(path, len(imports))
    )


try:
    run()
except Exception:
    output.print_md("**Error:**")
    output.print_md("```\n{}\n```".format(traceback.format_exc()))
```

**Step 1: Write the file** (above content)

**Step 2: Verify**

Read the file back — confirm `get_import_instances`, workset/view name helpers, CSV output.

---

## Task 11: Panel 2 — FindLargeFamilies

**File:** `BIMTools.extension/Model_Health.panel/FindLargeFamilies.pushbutton/script.py`

Lists families by estimated size, outputs `large_families_report.csv`. Note: Revit API does not expose raw family file size — this script uses element count as a size proxy and notes this limitation.

```python
"""
FindLargeFamilies — Reports families sorted by instance count (size proxy).
Columns: RunDate, ModelName, FamilyName, Category, SymbolCount, InstanceCount
Read-only. No model changes.

Note: Revit API does not expose raw family file size in bytes.
Instance and symbol counts are the best available size proxy via API.
"""
import traceback
from collections import defaultdict

import clr
clr.AddReference("RevitAPI")
from Autodesk.Revit.DB import FilteredElementCollector, FamilyInstance

from bim_utils import write_csv, today, get_families

from pyrevit import revit, script

doc = revit.doc
output = script.get_output()

FILENAME = "large_families_report.csv"
HEADERS = [
    "RunDate", "ModelName", "FamilyName", "Category",
    "SymbolCount", "InstanceCount",
]


def run():
    families = get_families(doc)

    # Count instances per family name
    instance_counts = defaultdict(int)
    for inst in FilteredElementCollector(doc).OfClass(FamilyInstance).ToElements():
        try:
            fam_name = inst.Symbol.Family.Name
            instance_counts[fam_name] += 1
        except Exception:
            pass

    run_date = today()
    model_name = doc.Title
    rows = []
    for fam in families:
        cat_name = fam.FamilyCategory.Name if fam.FamilyCategory else "Unknown"
        symbol_count = fam.GetFamilySymbolIds().Count
        inst_count = instance_counts.get(fam.Name, 0)
        rows.append([
            run_date, model_name,
            fam.Name, cat_name, symbol_count, inst_count,
        ])

    # Sort by instance count descending
    rows.sort(key=lambda r: -r[5])

    path = write_csv(FILENAME, HEADERS, rows)
    output.print_md(
        "**Large families report written:** `{}`  \n"
        "{} families listed.".format(path, len(rows))
    )


try:
    run()
except Exception:
    output.print_md("**Error:**")
    output.print_md("```\n{}\n```".format(traceback.format_exc()))
```

**Step 1: Write the file** (above content)

**Step 2: Verify**

Read the file back — confirm size-proxy note in docstring, `FamilyInstance` count, sorted by instance count.

---

## Task 12: Panel 2 — GroupInspector

**File:** `BIMTools.extension/Model_Health.panel/GroupInspector.pushbutton/script.py`

Reports all model groups and their instance counts, outputs `groups_report.csv`.

```python
"""
GroupInspector — Reports model groups, types, and instance counts.
Columns: RunDate, ModelName, GroupName, Type, InstanceCount, NestedCount
Read-only. No model changes.
"""
import traceback
from collections import defaultdict

import clr
clr.AddReference("RevitAPI")
from Autodesk.Revit.DB import (
    FilteredElementCollector,
    Group,
    GroupType,
)

from bim_utils import write_csv, today

from pyrevit import revit, script

doc = revit.doc
output = script.get_output()

FILENAME = "groups_report.csv"
HEADERS = [
    "RunDate", "ModelName", "GroupName", "GroupType",
    "InstanceCount", "NestedGroupCount",
]


def run():
    all_groups = list(FilteredElementCollector(doc).OfClass(Group).ToElements())
    all_types = list(FilteredElementCollector(doc).OfClass(GroupType).ToElements())

    if not all_groups:
        output.print_md("**No groups found in this model.**")
        return

    # Count instances per group type
    type_instance_count = defaultdict(int)
    for grp in all_groups:
        type_instance_count[grp.GroupType.Id.IntegerValue] += 1

    run_date = today()
    model_name = doc.Title
    rows = []
    for gt in all_types:
        # Count nested group types in this group type
        nested = 0
        for member_id in gt.GetMemberIds():
            member = doc.GetElement(member_id)
            if isinstance(member, Group):
                nested += 1

        cat_name = gt.Category.Name if gt.Category else "Unknown"
        rows.append([
            run_date, model_name,
            gt.Name,
            cat_name,
            type_instance_count.get(gt.Id.IntegerValue, 0),
            nested,
        ])

    rows.sort(key=lambda r: -r[4])
    path = write_csv(FILENAME, HEADERS, rows)
    output.print_md(
        "**Groups report written:** `{}`  \n"
        "{} group type(s), {} instance(s) total.".format(
            path, len(all_types), len(all_groups)
        )
    )


try:
    run()
except Exception:
    output.print_md("**Error:**")
    output.print_md("```\n{}\n```".format(traceback.format_exc()))
```

**Step 1: Write the file** (above content)

**Step 2: Verify**

Read the file back — confirm `Group` and `GroupType` collectors, nested count logic, instance count per type.

---

## Task 13: Panel 2 — UnplacedViews

**File:** `BIMTools.extension/Model_Health.panel/UnplacedViews.pushbutton/script.py`

Reports views not placed on any sheet, outputs `unplaced_views_report.csv`.

```python
"""
UnplacedViews — Reports views not placed on any sheet.
Columns: RunDate, ModelName, ViewName, ViewType, Discipline, Level
Read-only. No model changes.
"""
import traceback

import clr
clr.AddReference("RevitAPI")
from Autodesk.Revit.DB import (
    FilteredElementCollector,
    View,
    ViewSheet,
    Viewport,
    BuiltInParameter,
)

from bim_utils import write_csv, today, get_views

from pyrevit import revit, script

doc = revit.doc
output = script.get_output()

FILENAME = "unplaced_views_report.csv"
HEADERS = ["RunDate", "ModelName", "ViewName", "ViewType", "Discipline", "Level"]


def get_placed_view_ids():
    placed = set()
    for vp in FilteredElementCollector(doc).OfClass(Viewport).ToElements():
        placed.add(vp.ViewId)
    return placed


def get_param_value(elem, bip):
    p = elem.get_Parameter(bip)
    if p:
        return p.AsString() or p.AsValueString() or ""
    return ""


def run():
    placed_ids = get_placed_view_ids()
    views = get_views(doc, exclude_templates=True)

    unplaced = [v for v in views if v.Id not in placed_ids]

    if not unplaced:
        output.print_md("**All views are placed on sheets.**")
        return

    run_date = today()
    model_name = doc.Title
    rows = []
    for v in unplaced:
        discipline = get_param_value(v, BuiltInParameter.VIEW_DISCIPLINE)
        level = get_param_value(v, BuiltInParameter.PLAN_VIEW_LEVEL)
        rows.append([
            run_date, model_name,
            v.Name,
            str(v.ViewType),
            discipline,
            level,
        ])

    rows.sort(key=lambda r: r[3])
    path = write_csv(FILENAME, HEADERS, rows)
    output.print_md(
        "**Unplaced views report written:** `{}`  \n"
        "{} unplaced view(s) out of {}.".format(path, len(unplaced), len(views))
    )


try:
    run()
except Exception:
    output.print_md("**Error:**")
    output.print_md("```\n{}\n```".format(traceback.format_exc()))
```

**Step 1: Write the file** (above content)

**Step 2: Verify**

Read the file back — confirm `Viewport` collector for placed IDs, exclude templates, discipline/level parameter helpers.

---

## Task 14: Panel 2 — UnusedFamilies

**File:** `BIMTools.extension/Model_Health.panel/UnusedFamilies.pushbutton/script.py`

Lists families with zero placed instances, outputs `unused_families_report.csv`. List-only — does NOT purge.

```python
"""
UnusedFamilies — Lists families with no placed instances.
Columns: RunDate, ModelName, FamilyName, Category, TypeCount
List-only: no automatic purge. Outputs unused_families_report.csv.
Read-only. No model changes.
"""
import traceback

import clr
clr.AddReference("RevitAPI")
from Autodesk.Revit.DB import FilteredElementCollector, FamilyInstance

from bim_utils import write_csv, today, get_families

from pyrevit import revit, script

doc = revit.doc
output = script.get_output()

FILENAME = "unused_families_report.csv"
HEADERS = ["RunDate", "ModelName", "FamilyName", "Category", "TypeCount"]


def run():
    # Collect all family names that have at least one placed instance
    placed_family_names = set()
    for inst in FilteredElementCollector(doc).OfClass(FamilyInstance).ToElements():
        try:
            placed_family_names.add(inst.Symbol.Family.Name)
        except Exception:
            pass

    families = get_families(doc)
    unused = [f for f in families if f.Name not in placed_family_names]

    if not unused:
        output.print_md("**No unused families found.**")
        return

    run_date = today()
    model_name = doc.Title
    rows = []
    for fam in unused:
        cat_name = fam.FamilyCategory.Name if fam.FamilyCategory else "Unknown"
        type_count = fam.GetFamilySymbolIds().Count
        rows.append([run_date, model_name, fam.Name, cat_name, type_count])

    rows.sort(key=lambda r: r[3])
    path = write_csv(FILENAME, HEADERS, rows)
    output.print_md(
        "**Unused families report written:** `{}`  \n"
        "{} unused familie(s) found. No automatic purge performed.".format(
            path, len(unused)
        )
    )


try:
    run()
except Exception:
    output.print_md("**Error:**")
    output.print_md("```\n{}\n```".format(traceback.format_exc()))
```

**Step 1: Write the file** (above content)

**Step 2: Verify**

Read the file back — confirm "list-only" in docstring, no `Transaction`, placed check via `FamilyInstance` names.

---

## Task 15: Panel 3 — CreateClashViews

**File:** `BIMTools.extension/Coordination.panel/CreateClashViews.pushbutton/script.py`

Creates one 3D view per discipline pair, named `3D - Clash - A vs B`. Idempotent.

```python
"""
CreateClashViews — Creates one 3D view per discipline pair for clash review.
View names: "3D - Clash - DISC_A vs DISC_B"
Idempotent: skips views that already exist by name.
"""
import traceback

import clr
clr.AddReference("RevitAPI")
from Autodesk.Revit.DB import (
    FilteredElementCollector,
    ViewFamilyType,
    ViewFamily,
    View3D,
    View,
    Transaction,
)

from pyrevit import revit, script

doc = revit.doc
output = script.get_output()

DISCIPLINES = ["Arch", "Structure", "Mechanical", "Electrical", "Plumbing", "Civil"]


def get_pairs(disciplines):
    pairs = []
    for i, a in enumerate(disciplines):
        for b in disciplines[i + 1:]:
            pairs.append((a, b))
    return pairs


def get_3d_vft():
    for vft in FilteredElementCollector(doc).OfClass(ViewFamilyType).ToElements():
        if vft.ViewFamily == ViewFamily.ThreeDimensional:
            return vft
    return None


def run():
    vft = get_3d_vft()
    if vft is None:
        output.print_md("**Error:** No 3D ViewFamilyType found.")
        return

    existing_names = {
        v.Name
        for v in FilteredElementCollector(doc).OfClass(View).ToElements()
        if not v.IsTemplate
    }

    pairs = get_pairs(DISCIPLINES)
    to_create = []
    for a, b in pairs:
        name = "3D - Clash - {} vs {}".format(a, b)
        if name not in existing_names:
            to_create.append((name,))

    if not to_create:
        output.print_md(
            "**Done:** All {} clash views already exist.".format(len(pairs))
        )
        return

    with Transaction(doc, "Create Clash Views") as t:
        t.Start()
        for (name,) in to_create:
            view = View3D.CreateIsometric(doc, vft.Id)
            view.Name = name
        t.Commit()

    output.print_md(
        "**Created {} clash view(s).**".format(len(to_create))
    )
    skipped = len(pairs) - len(to_create)
    if skipped:
        output.print_md("**Skipped {} already existing.**".format(skipped))


try:
    run()
except Exception:
    output.print_md("**Error:**")
    output.print_md("```\n{}\n```".format(traceback.format_exc()))
```

**Step 1: Write the file** (above content)

**Step 2: Verify**

Read the file back — confirm `get_pairs` produces 15 pairs for 6 disciplines, idempotent name check, `View3D.CreateIsometric`.

---

## Task 16: Panel 3 — ColorByWorkset

**File:** `BIMTools.extension/Coordination.panel/ColorByWorkset.pushbutton/script.py`

Applies solid fill color overrides per workset to the active view. Applies to active view only — no permanent model changes.

```python
"""
ColorByWorkset — Applies solid fill color overrides by workset in active view.
Active view only. Uses 8-color cycle. Resets on re-run.
No permanent model changes beyond view graphics overrides.
"""
import traceback

import clr
clr.AddReference("RevitAPI")
from Autodesk.Revit.DB import (
    FilteredElementCollector,
    FillPatternElement,
    FillPatternTarget,
    OverrideGraphicSettings,
    Color,
    Transaction,
    WorksetKind,
    FilteredWorksetCollector,
    ElementWorksetFilter,
)

from pyrevit import revit, script

doc = revit.doc
uidoc = revit.uidoc
output = script.get_output()

# 8-color palette (R, G, B)
COLORS = [
    (255, 99, 71),   # Tomato
    (70, 130, 180),  # Steel Blue
    (60, 179, 113),  # Medium Sea Green
    (255, 165, 0),   # Orange
    (147, 112, 219), # Medium Purple
    (0, 206, 209),   # Dark Turquoise
    (240, 128, 128), # Light Coral
    (154, 205, 50),  # Yellow Green
]


def get_solid_fill_id():
    for pat in FilteredElementCollector(doc).OfClass(FillPatternElement).ToElements():
        fp = pat.GetFillPattern()
        if fp.Target == FillPatternTarget.Drafting and fp.IsSolidFill:
            return pat.Id
    return None


def run():
    active_view = uidoc.ActiveView
    if active_view is None:
        output.print_md("**Error:** No active view.")
        return

    solid_id = get_solid_fill_id()
    if solid_id is None:
        output.print_md("**Error:** No solid fill pattern found in document.")
        return

    if not doc.IsWorkshared:
        output.print_md("**Error:** Model is not workshared — no worksets.")
        return

    worksets = list(
        FilteredWorksetCollector(doc).OfKind(WorksetKind.UserWorkset).ToWorksets()
    )

    with Transaction(doc, "Color by Workset") as t:
        t.Start()
        for idx, ws in enumerate(worksets):
            r, g, b = COLORS[idx % len(COLORS)]
            ogs = OverrideGraphicSettings()
            ogs.SetSurfaceForegroundPatternId(solid_id)
            ogs.SetSurfaceForegroundPatternColor(Color(r, g, b))
            ogs.SetSurfaceForegroundPatternVisible(True)

            # Apply to all elements in this workset
            filt = ElementWorksetFilter(ws.Id, False)
            for elem in FilteredElementCollector(doc, active_view.Id).WherePasses(filt).ToElements():
                try:
                    active_view.SetElementOverrides(elem.Id, ogs)
                except Exception:
                    pass
        t.Commit()

    output.print_md(
        "**Color by Workset applied** to '{}' — {} workset(s).".format(
            active_view.Name, len(worksets)
        )
    )


try:
    run()
except Exception:
    output.print_md("**Error:**")
    output.print_md("```\n{}\n```".format(traceback.format_exc()))
```

**Step 1: Write the file** (above content)

**Step 2: Verify**

Read the file back — confirm `uidoc.ActiveView`, `ElementWorksetFilter`, `SetElementOverrides`, 8-color palette, `FillPatternTarget.Drafting`.

---

## Task 17: Panel 3 — ColorByDiscipline

**File:** `BIMTools.extension/Coordination.panel/ColorByDiscipline.pushbutton/script.py`

Applies solid fill color overrides by `Discipline` parameter value in the active view.

```python
"""
ColorByDiscipline — Applies solid fill color overrides by Discipline parameter in active view.
Active view only. Uses 8-color cycle keyed to unique Discipline values found.
No permanent model changes beyond view graphics overrides.
"""
import traceback
from collections import defaultdict

import clr
clr.AddReference("RevitAPI")
from Autodesk.Revit.DB import (
    FilteredElementCollector,
    FillPatternElement,
    FillPatternTarget,
    OverrideGraphicSettings,
    Color,
    Transaction,
    StorageType,
)

from pyrevit import revit, script

doc = revit.doc
uidoc = revit.uidoc
output = script.get_output()

COLORS = [
    (255, 99, 71),
    (70, 130, 180),
    (60, 179, 113),
    (255, 165, 0),
    (147, 112, 219),
    (0, 206, 209),
    (240, 128, 128),
    (154, 205, 50),
]


def get_solid_fill_id():
    for pat in FilteredElementCollector(doc).OfClass(FillPatternElement).ToElements():
        fp = pat.GetFillPattern()
        if fp.Target == FillPatternTarget.Drafting and fp.IsSolidFill:
            return pat.Id
    return None


def get_discipline(elem):
    p = elem.LookupParameter("Discipline")
    if p and p.StorageType == StorageType.String:
        val = p.AsString()
        return val.strip() if val else ""
    return ""


def run():
    active_view = uidoc.ActiveView
    if active_view is None:
        output.print_md("**Error:** No active view.")
        return

    solid_id = get_solid_fill_id()
    if solid_id is None:
        output.print_md("**Error:** No solid fill pattern found.")
        return

    # Collect elements in view and group by Discipline
    all_elems = list(FilteredElementCollector(doc, active_view.Id).ToElements())
    discipline_map = defaultdict(list)
    for elem in all_elems:
        disc = get_discipline(elem)
        if disc:
            discipline_map[disc].append(elem)

    if not discipline_map:
        output.print_md(
            "**No elements with Discipline parameter found in active view.**"
        )
        return

    disciplines = sorted(discipline_map.keys())
    color_assignments = {disc: COLORS[i % len(COLORS)] for i, disc in enumerate(disciplines)}

    with Transaction(doc, "Color by Discipline") as t:
        t.Start()
        for disc, elems in discipline_map.items():
            r, g, b = color_assignments[disc]
            ogs = OverrideGraphicSettings()
            ogs.SetSurfaceForegroundPatternId(solid_id)
            ogs.SetSurfaceForegroundPatternColor(Color(r, g, b))
            ogs.SetSurfaceForegroundPatternVisible(True)
            for elem in elems:
                try:
                    active_view.SetElementOverrides(elem.Id, ogs)
                except Exception:
                    pass
        t.Commit()

    output.print_md(
        "**Color by Discipline applied** — {} discipline(s): {}".format(
            len(disciplines), ", ".join(disciplines)
        )
    )


try:
    run()
except Exception:
    output.print_md("**Error:**")
    output.print_md("```\n{}\n```".format(traceback.format_exc()))
```

**Step 1: Write the file** (above content)

**Step 2: Verify**

Read the file back — confirm `LookupParameter("Discipline")`, `StorageType.String`, active-view element collector, color assignment by sorted disciplines.

---

## Task 18: Panel 3 — ClashStatusManager

**File:** `BIMTools.extension/Coordination.panel/ClashStatusManager.pushbutton/script.py`

Sets `Clash_Status` on selected elements via a dialog. Requires user to pre-select elements.

```python
"""
ClashStatusManager — Sets Clash_Status parameter on selected elements.
User selects elements, then chooses status from dialog.
Valid values: Open, In Progress, Resolved
"""
import traceback

import clr
clr.AddReference("RevitAPI")
from Autodesk.Revit.DB import Transaction, StorageType

from pyrevit import revit, script, forms

doc = revit.doc
uidoc = revit.uidoc
output = script.get_output()

STATUS_OPTIONS = ["Open", "In Progress", "Resolved"]
PARAM_NAME = "Clash_Status"


def run():
    selection = [doc.GetElement(eid) for eid in uidoc.Selection.GetElementIds()]

    if not selection:
        forms.alert(
            "Select one or more elements before running Clash Status Manager.",
            exitscript=True,
        )
        return

    status = forms.SelectFromList.show(
        STATUS_OPTIONS,
        title="Set Clash Status",
        button_name="Apply",
        multiselect=False,
    )

    if not status:
        output.print_md("**Cancelled.**")
        return

    updated = 0
    skipped = 0
    with Transaction(doc, "Set Clash Status") as t:
        t.Start()
        for elem in selection:
            p = elem.LookupParameter(PARAM_NAME)
            if p and p.StorageType == StorageType.String and not p.IsReadOnly:
                p.Set(status)
                updated += 1
            else:
                skipped += 1
        t.Commit()

    output.print_md(
        "**Clash_Status set to '{}'** — {} element(s) updated, {} skipped "
        "(no parameter or read-only).".format(status, updated, skipped)
    )


try:
    run()
except Exception:
    output.print_md("**Error:**")
    output.print_md("```\n{}\n```".format(traceback.format_exc()))
```

**Step 1: Write the file** (above content)

**Step 2: Verify**

Read the file back — confirm `uidoc.Selection.GetElementIds()`, `forms.SelectFromList.show`, `LookupParameter`, read-only guard, `updated`/`skipped` count.

---

## Task 19: Panel 3 — ZoneChecker

**File:** `BIMTools.extension/Coordination.panel/ZoneChecker.pushbutton/script.py`

Finds elements missing `Coordination_Zone` parameter value, outputs `zone_check_report.csv`.

```python
"""
ZoneChecker — Lists elements missing a Coordination_Zone value.
Columns: RunDate, ModelName, ElementID, Category, Level, Workset
Outputs zone_check_report.csv. Read-only.
"""
import traceback

import clr
clr.AddReference("RevitAPI")
from Autodesk.Revit.DB import (
    FilteredElementCollector,
    StorageType,
    BuiltInParameter,
    BuiltInCategory,
)

from bim_utils import write_csv, today

from pyrevit import revit, script

doc = revit.doc
output = script.get_output()

FILENAME = "zone_check_report.csv"
HEADERS = ["RunDate", "ModelName", "ElementID", "Category", "Level", "Workset"]

# Categories to check — skip annotation and view elements
SKIP_CATEGORIES = {
    int(BuiltInCategory.OST_Cameras),
    int(BuiltInCategory.OST_Views),
    int(BuiltInCategory.OST_Sheets),
    int(BuiltInCategory.OST_DetailComponents),
    int(BuiltInCategory.OST_TextNotes),
    int(BuiltInCategory.OST_Dimensions),
    int(BuiltInCategory.OST_GenericAnnotation),
}


def get_param_str(elem, bip):
    p = elem.get_Parameter(bip)
    if p:
        return p.AsString() or p.AsValueString() or ""
    return ""


def get_workset_name(elem):
    if not doc.IsWorkshared:
        return "N/A"
    ws_param = elem.get_Parameter(BuiltInParameter.ELEM_PARTITION_PARAM)
    if ws_param:
        ws_id = ws_param.AsElementId()
        ws = doc.GetWorksetTable().GetWorkset(ws_id)
        return ws.Name if ws else "Unknown"
    return "Unknown"


def run():
    all_elems = list(
        FilteredElementCollector(doc).WhereElementIsNotElementType().ToElements()
    )

    missing = []
    for elem in all_elems:
        try:
            cat = elem.Category
            if cat is None:
                continue
            if int(cat.Id.IntegerValue) in SKIP_CATEGORIES:
                continue
            p = elem.LookupParameter("Coordination_Zone")
            if p is None:
                continue
            val = p.AsString() if p.StorageType == StorageType.String else None
            if val:
                continue  # has a value — OK
            level = get_param_str(elem, BuiltInParameter.FAMILY_LEVEL_PARAM)
            if not level:
                level = get_param_str(elem, BuiltInParameter.SCHEDULE_LEVEL_PARAM)
            missing.append([
                today(), doc.Title,
                elem.Id.IntegerValue,
                cat.Name,
                level,
                get_workset_name(elem),
            ])
        except Exception:
            pass

    if not missing:
        output.print_md("**All elements have a Coordination_Zone value.**")
        return

    path = write_csv(FILENAME, HEADERS, missing)
    output.print_md(
        "**Zone check report written:** `{}`  \n"
        "{} element(s) missing Coordination_Zone.".format(path, len(missing))
    )


try:
    run()
except Exception:
    output.print_md("**Error:**")
    output.print_md("```\n{}\n```".format(traceback.format_exc()))
```

**Step 1: Write the file** (above content)

**Step 2: Verify**

Read the file back — confirm `SKIP_CATEGORIES`, `LookupParameter("Coordination_Zone")`, both level BIPs tried, workset helper.

---

## Task 20: Panel 3 — InterferenceCheck

**File:** `BIMTools.extension/Coordination.panel/InterferenceCheck.pushbutton/script.py`

Posts the built-in Revit Interference Check command. No custom logic — just triggers the native dialog.

```python
"""
InterferenceCheck — Runs Revit's built-in interference check via PostCommand.
Opens the native Revit Interference Check dialog.
"""
import traceback

import clr
clr.AddReference("RevitAPIUI")
from Autodesk.Revit.UI import PostableCommand, RevitCommandId

from pyrevit import revit, script

uidoc = revit.uidoc
output = script.get_output()


def run():
    cmd_id = RevitCommandId.LookupPostableCommandId(PostableCommand.InterferenceCheck)
    uidoc.Application.PostCommand(cmd_id)
    output.print_md(
        "**Interference Check launched.** "
        "Select categories in the dialog, then click OK."
    )


try:
    run()
except Exception:
    output.print_md("**Error:**")
    output.print_md("```\n{}\n```".format(traceback.format_exc()))
```

**Step 1: Write the file** (above content)

**Step 2: Verify**

Read the file back — confirm `RevitAPIUI` reference, `PostableCommand.InterferenceCheck`, `PostCommand`.

---

## Task 21: Panel 8 — CoordReport

**File:** `BIMTools.extension/Reporting.panel/CoordReport.pushbutton/script.py`

Compiles data from existing output CSVs into `coordination_report.csv`. Reads from the pipeline output folder. Missing source CSVs show "N/A".

```python
"""
CoordReport — Compiles coordination summary from existing output CSVs.
Source CSVs (from BIM_Automation/data/output/):
  model_health_scores.csv, warnings_report.csv,
  unplaced_views_report.csv, cad_imports_report.csv
Output: coordination_report.csv
Missing source CSVs show N/A — not an error.
"""
import traceback
import csv
import os

from bim_utils import write_csv, today, OUTPUT_DIR

from pyrevit import revit, script

doc = revit.doc
output = script.get_output()

FILENAME = "coordination_report.csv"
HEADERS = [
    "RunDate", "ModelName",
    "HealthScore", "HealthStatus",
    "WarningCount",
    "UnplacedViewCount",
    "CADImportCount",
]

SOURCE_FILES = {
    "health": "model_health_scores.csv",
    "warnings": "warnings_report.csv",
    "unplaced": "unplaced_views_report.csv",
    "cad": "cad_imports_report.csv",
}


def read_csv_rows(filename):
    path = os.path.join(OUTPUT_DIR, filename)
    if not os.path.exists(path):
        return None
    rows = []
    with open(path, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append(row)
    return rows


def latest_for_model(rows, model_name_col, model_name):
    """Return last matching row for this model, or None."""
    if not rows:
        return None
    matches = [r for r in rows if r.get(model_name_col, "") == model_name]
    return matches[-1] if matches else None


def run():
    model_name = doc.Title

    health_rows = read_csv_rows(SOURCE_FILES["health"])
    warning_rows = read_csv_rows(SOURCE_FILES["warnings"])
    unplaced_rows = read_csv_rows(SOURCE_FILES["unplaced"])
    cad_rows = read_csv_rows(SOURCE_FILES["cad"])

    # Health score
    health_row = latest_for_model(health_rows, "ModelName", model_name)
    health_score = health_row["TotalScore"] if health_row else "N/A"
    health_status = health_row["Status"] if health_row else "N/A"

    # Warning count from warnings_report
    if warning_rows is not None:
        model_warnings = [r for r in warning_rows if r.get("ModelName") == model_name]
        warning_count = sum(int(r.get("Count", 0)) for r in model_warnings)
    else:
        warning_count = "N/A"

    # Unplaced view count
    if unplaced_rows is not None:
        unplaced_count = sum(
            1 for r in unplaced_rows if r.get("ModelName") == model_name
        )
    else:
        unplaced_count = "N/A"

    # CAD import count
    if cad_rows is not None:
        cad_count = sum(1 for r in cad_rows if r.get("ModelName") == model_name)
    else:
        cad_count = "N/A"

    row = [
        today(), model_name,
        health_score, health_status,
        warning_count, unplaced_count, cad_count,
    ]

    path = write_csv(FILENAME, HEADERS, [row])
    output.print_md("**Coordination report written:** `{}`".format(path))
    output.print_md(
        "Health: {} ({}) | Warnings: {} | Unplaced views: {} | CAD imports: {}".format(
            health_score, health_status, warning_count, unplaced_count, cad_count
        )
    )


try:
    run()
except Exception:
    output.print_md("**Error:**")
    output.print_md("```\n{}\n```".format(traceback.format_exc()))
```

**Step 1: Write the file** (above content)

**Step 2: Verify**

Read the file back — confirm all 4 source CSV references, `latest_for_model` helper, "N/A" fallback when CSV missing, summary print.

---

## Task 22: Panel 8 — ClashSummary

**File:** `BIMTools.extension/Reporting.panel/ClashSummary.pushbutton/script.py`

Reads `Clash_Status` parameter from all model elements, summarizes counts by status, outputs `clash_summary_report.csv`.

```python
"""
ClashSummary — Summarizes Clash_Status values from all model elements.
Columns: RunDate, ModelName, Status, Count
Outputs clash_summary_report.csv. Read-only.
"""
import traceback
from collections import Counter

import clr
clr.AddReference("RevitAPI")
from Autodesk.Revit.DB import FilteredElementCollector, StorageType

from bim_utils import write_csv, today

from pyrevit import revit, script

doc = revit.doc
output = script.get_output()

FILENAME = "clash_summary_report.csv"
HEADERS = ["RunDate", "ModelName", "Status", "Count"]

KNOWN_STATUSES = ["Open", "In Progress", "Resolved"]


def run():
    all_elems = list(
        FilteredElementCollector(doc).WhereElementIsNotElementType().ToElements()
    )

    status_counts = Counter()
    for elem in all_elems:
        p = elem.LookupParameter("Clash_Status")
        if p and p.StorageType == StorageType.String:
            val = p.AsString()
            if val and val.strip():
                status_counts[val.strip()] += 1

    if not status_counts:
        output.print_md(
            "**No elements with Clash_Status found.** "
            "Run Clash Status Manager to tag elements first."
        )
        return

    run_date = today()
    model_name = doc.Title
    rows = []
    for status in KNOWN_STATUSES:
        rows.append([run_date, model_name, status, status_counts.get(status, 0)])
    # Include any unexpected status values
    for status, count in status_counts.items():
        if status not in KNOWN_STATUSES:
            rows.append([run_date, model_name, status, count])

    path = write_csv(FILENAME, HEADERS, rows)
    total = sum(status_counts.values())
    output.print_md(
        "**Clash summary written:** `{}`  \n"
        "Total tagged: {} — {}".format(
            path, total,
            " | ".join("{}: {}".format(s, status_counts.get(s, 0)) for s in KNOWN_STATUSES)
        )
    )


try:
    run()
except Exception:
    output.print_md("**Error:**")
    output.print_md("```\n{}\n```".format(traceback.format_exc()))
```

**Step 1: Write the file** (above content)

**Step 2: Verify**

Read the file back — confirm `Counter`, known statuses listed in fixed order, unknown statuses appended, total count printed.

---

## Task 23: Panel 9 — SyncAndClose

**File:** `BIMTools.extension/Utilities.panel/SyncAndClose.pushbutton/script.py`

Confirms with user, syncs with central, relinquishes all worksets, closes the document.

```python
"""
SyncAndClose — Syncs with central, relinquishes all, closes document.
Requires confirmation. Only works on workshared models.
"""
import traceback

import clr
clr.AddReference("RevitAPI")
from Autodesk.Revit.DB import (
    TransactWithCentralOptions,
    SynchronizeWithCentralOptions,
    RelinquishOptions,
    WorksharingUtils,
)

from pyrevit import revit, script, forms

doc = revit.doc
uidoc = revit.uidoc
output = script.get_output()


def run():
    if not doc.IsWorkshared:
        forms.alert(
            "This model is not workshared. Sync and Close is only available "
            "for workshared (central) models.",
            exitscript=True,
        )
        return

    if not forms.alert(
        "Sync with central, relinquish all worksets, and close '{}'. "
        "This cannot be undone. Proceed?".format(doc.Title),
        yes=True,
        no=True,
    ):
        output.print_md("**Cancelled.**")
        return

    output.print_md("Syncing with central...")

    # Relinquish options
    relinquish_opts = RelinquishOptions(True)
    relinquish_opts.CheckedOutElements = True
    relinquish_opts.UserWorksets = True
    relinquish_opts.FamilyWorksets = True
    relinquish_opts.ViewWorksets = True
    relinquish_opts.StandardWorksets = True

    # Sync options
    sync_opts = SynchronizeWithCentralOptions()
    sync_opts.SetRelinquishOptions(relinquish_opts)
    sync_opts.Comment = "Sync and close via BIMTools"
    sync_opts.Compact = False

    twc_opts = TransactWithCentralOptions()

    doc.SynchronizeWithCentral(twc_opts, sync_opts)
    output.print_md("**Sync complete.** Closing document...")

    uidoc.Application.OpenAndActivateDocument(
        doc.PathName
    )  # re-activate to ensure close works
    doc.Close(False)  # False = do not save (already synced)


try:
    run()
except Exception:
    output.print_md("**Error:**")
    output.print_md("```\n{}\n```".format(traceback.format_exc()))
```

**Step 1: Write the file** (above content)

**Step 2: Verify**

Read the file back — confirm `forms.alert` confirmation, `RelinquishOptions`, `SynchronizeWithCentralOptions`, `doc.Close(False)`.

---

## Task 24: Update BIM Coordination Toolbar Design Doc

**File:** `BIM Coordination Toolbar design doc.md` (root of project)

Update to reference the production scripts now built in `BIMTools.extension/`.

**Step 1: Read the file** to see current content.

**Step 2: Add a "Production Status" section** near the top after any existing header, using Edit tool.

Content to add (insert after the first heading / intro paragraph):

```markdown
## Production Status

All 21 scripts built and deployed under `BIMTools.extension/`. See implementation plan:
`docs/plans/2026-03-07-pyrevit-toolbar.md`

| Panel | Scripts | Status |
|---|---|---|
| Project_Setup.panel | 6 tools | Built |
| Model_Health.panel | 6 tools | Built |
| Coordination.panel | 6 tools | Built |
| Reporting.panel | 2 tools | Built |
| Utilities.panel | 1 tool | Built |
| lib/ | bim_utils.py | Built |
```

---

## Verification Checklist

After all tasks:

- [ ] `BIMTools.extension/lib/__init__.py` exists
- [ ] `BIMTools.extension/lib/bim_utils.py` has all 9 functions + `OUTPUT_DIR`
- [ ] `Project_Setup.panel/` has 6 `script.py` files
- [ ] `Model_Health.panel/` has 6 `script.py` files
- [ ] `Coordination.panel/` has 6 `script.py` files
- [ ] `Reporting.panel/` has 2 `script.py` files
- [ ] `Utilities.panel/` has 1 `script.py` file
- [ ] All setup scripts are idempotent (skip-if-exists logic)
- [ ] All health scripts are read-only (no Transaction)
- [ ] Only InitializeProject and SyncAndClose have confirmation dialogs
- [ ] All scripts have top-level `try/except` with traceback output
- [ ] `bim_utils` imported from all Panel 2, 3, 8 scripts
