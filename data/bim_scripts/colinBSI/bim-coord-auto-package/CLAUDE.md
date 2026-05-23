# BIM Coord Auto Package

## Project Type
Documentation-only package — no code tests, no git. Verification = read files back after editing.

## Critical File Quirk
Several .md files use non-breaking spaces (U+00A0) for indentation. The Edit tool will fail to match these lines. Use Python on raw bytes via subagent if Edit fails.

## Architecture
5-phase implementation structure. See `BIM Coordination Package - Index.md` for the full map.
- Phase 5 (`BIM compliance dashboard Requirements.md`) is the advanced tier — supersedes simpler CSV exports from Phases 1–4.
- Phase 5 uses `Portfolio_` shared parameter convention; Phases 1–4 use `BIM_Status`, `Clash_Status` etc.

## Build Status
- Phases 1–4: complete. All production scripts built.
- Phase 5: not yet started (portfolio exporter, governance scoring, predictive engine).
- `BIMTools.extension/lib/bim_utils.py` — shared pyRevit lib; pyRevit auto-adds `lib/` to sys.path, import with `from bim_utils import ...`
- `docs/powerbi/` — Power BI build guides (markdown only; .pbix is binary, can't be written as text)

## Revit / pyRevit API Gotchas
- UnitUtils changed in Revit 2022: `DisplayUnitType.DUT_DECIMAL_FEET` → `UnitTypeId.Feet`. Use try/except ImportError to handle both.
- Worksets: use `FilteredWorksetCollector(doc).OfKind(WorksetKind.UserWorkset).ToWorksets()`, not FilteredElementCollector.
- Solid fill pattern for color overrides: filter `FillPatternTarget.Drafting`, not Model.
- InterferenceCheck PostCommand requires `clr.AddReference("RevitAPIUI")` (not RevitAPI).
- Confirmation dialogs: `forms.alert(msg, yes=True, no=True)` returns True/False.
- Selected elements: `uidoc.Selection.GetElementIds()` → iterate, call `doc.GetElement(eid)` on each.

## Navisworks XML Structure
- Discipline pair comes from `<clashtest name="Arch vs Structure">`, not individual `<clashresult>` elements.
- Clash status is an attribute on `<clashresult status="active">`.
- Clash XYZ position: `<clashpoint><pos3f x="..." y="..." z="..."/></clashpoint>`.

## Canonical Standards (do not contradict these)
- Model health score: 150-pt scale. Thresholds: Elite ≥130, Excellent ≥115, Healthy ≥100, Needs Cleanup ≥85, Critical <85
- Minimum score for coordination entry: 100
- Weekly workflow: Mon=uploads, Tue=clashes, Wed=automation/grouping, Thu=ACC issues, Fri=meeting
- Warning target: <300 ideal, <1000 acceptable
- File size target: <300MB ideal, <500MB acceptable
- Clash tolerances: 0in hard, 1–2in MEP clearance, 24–36in equipment clearance

## LiDAR / Point Clouds
RCP/RCS and RCMR files are visual reference overlays only — not used for clash detection.
All point cloud files go on the **Scan workset** in Revit.
Standard view: `3D - Scan Reference`
