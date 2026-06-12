# IFC/IDS Pre-Validator

A lightweight command-line tool for pre-validating IFC models against
IDS (Information Delivery Specification) rules — before running a
full certified validation in Solibri or BIMcollab.

Developed as part of an openBIM QA/QC portfolio focused on BIM data
quality, digital handover, and IDS-based model delivery checks.

---

## What it does

- Parses IFC STEP files directly — no external IFC library required
- Reads IDS specifications conforming to buildingSMART IDS 1.0
- Evaluates Applicability filters to select relevant elements
- Checks Requirements against each applicable element
- Reports PASS / FAIL per element, per specification, per requirement
- Exports a structured QA/QC report as UTF-8 CSV

**Output columns:**
`ifc_file` · `spec` · `door_id` · `door_name` · `door_tag` ·
`requirement` · `status` · `actual` · `allowed` · `message`

---

## Scope and limitations

This is a **pre-validator**, not a certified IDS validator.

**Supported:**
- Entity: `IfcDoor`
- Facets: `attribute`, `property` (IfcPropertySingleValue)
- Cardinality: `required` (Specification and Facet level)
- Applicability filters: property-based boolean filters (e.g. `IsExternal = TRUE`)
- Value constraints: simple value lists, xs:enumeration
- Data types: IFCBOOLEAN, IFCLABEL, IFCIDENTIFIER, IFCLENGTHMEASURE,
  IFCPOSITIVELENGTHMEASURE, and all string/numeric measure types

**Not supported in this version:**
- Entities other than IfcDoor
- `prohibited` / `optional` cardinality at Facet level
- `classification`, `material`, `partOf` facets
- Regex patterns, numeric range constraints
- Multi-file or federated model validation

For production delivery validation, use
[Solibri Office](https://www.solibri.com) or
[BIMcollab Zoom](https://www.bimcollab.com) with the IDS Validation
workflow.

---

## Installation

```bash
pip install lxml
```

Python 3.9 or later required.

---

## Usage

```bash
python ids_prevalidator.py <ids-file> <ifc-file> [csv-output]
```

**Examples:**

```bash
# Console output only
python ids_prevalidator.py door.ids model.ifc

# Console output + CSV report
python ids_prevalidator.py door.ids model.ifc report.csv
```

**Console output example:**

```
IFC: LPH5_Door_IDS_TestModel_MIXED_PASS_FAIL_v2_5_aligned.ifc
IDS: LPH5_Door_IDS_AIA_AllCategories_v2_5_production_senior.ids
Requirement checks: 282; PASS: 275; FAIL: 7

Failed specs:
- D04 FireRating: 1
- D05 SecurityRating: 1
- D06 AcousticRating: 1
- D07 Tag: 1
- D08 ThermalTransmittance (external): 1
- D09 OperationType: 1
- D10 OpeningDirection: 1
```

---

## Test models

The repository `lph5-door-ids-qa` contains two IFC test models
for use with this validator:

| Model | Purpose |
|---|---|
| `LPH5_Door_IDS_TestModel_PASS_v2_5_aligned.ifc` | All 85 requirement checks pass |
| `LPH5_Door_IDS_TestModel_MIXED_PASS_FAIL_v2_5_aligned.ifc` | 7 intentional failures across 282 checks |

The 7 expected failures cover:
- Missing `IfcDoor.Tag`
- `OperationType = USERDEFINED` (not in controlled value list)
- `FireRating = T30` (invalid code per project value list)
- `OpeningDirection = LEFT` (invalid value)
- `AcousticRating = SST1` (invalid code)
- `SecurityRating = RC1` (invalid code)
- External door missing `ThermalTransmittance`

---

## IDS logic — Applicability vs. Requirements

Objects **outside** the Applicability scope are neither reported as
PASS nor FAIL — they are excluded from the check entirely.

This means every discriminating criterion (e.g. `IsExternal`,
`PredefinedType`, `ObjectType`) must be placed in `Applicability`,
not in `Requirements`. Misplacing a filter criterion in Requirements
generates false positives and invalidates QA/QC reports.

Example: `ThermalTransmittance` (U-value) applies only to external
doors. The filter `IsExternal = TRUE` is therefore set in
Applicability — internal doors are excluded before the check runs.

---

## Architecture

```
ids_prevalidator.py
├── split_top_level()   STEP argument tokeniser (handles nested brackets,
│                       quoted strings, doubled single-quote escaping)
├── unstep()            Strips STEP string delimiters and enum dots
├── parse_measure()     Resolves IFC measure wrappers to Python types
├── parse_ifc()         Regex-based STEP record parser → door/pset graph
├── parse_ids()         lxml XPath IDS reader → Specification list
├── filter_applies()    Evaluates Applicability filters per element
├── validate()          Core PASS/FAIL logic — returns row list
└── main()              CLI entry point, console summary, CSV export
```

---

## Repository context

This validator is part of a two-layer IDS QA stack:

```
AIA / LOIN
    │
    ▼
Gate-0: Basic Model Context IDS (C01–C14)
    │    Project hierarchy · spaces · spatial containment
    │    Element status · classification · proxy prohibition
    │
    ▼
Bauteil-IDS: LPH5 Door IDS (D01–D30)
    │    Door identity · fire · acoustics · accessibility
    │    security · thermal · digital handover attributes
    │
    ▼
Python Pre-Validator  ──▶  Solibri / BIMcollab (certified)
    │
    ▼
QA/QC Report (CSV)  ──▶  BCF Issues  ──▶  Digital Handover
```

IDS files, test models, and QA reports:
→ [lph5-door-ids-qa](https://github.com/agnes-schroeder-bim/lph5-door-ids-qa)

---

## Contact

Agnes Schröder — Architektin | BIM Data Quality & IFC/IDS Validation

agnes@architektur-schroeder.com
www.architektur-schroeder.com
