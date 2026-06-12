# BIM Model QA/QC Checklists — HVAC and Electrical
## LUA BIM LABS | Project Mentor Template Pack | PM-T02 / PM-T03
**Version:** 1.0 | For use before any model submission, coordination release, or milestone delivery

---

## HOW TO USE THESE CHECKLISTS

1. Complete this checklist before submitting any model to the CDE Shared zone or to a client.
2. Every item must be checked. If an item is not applicable to your project, mark it "N/A" and write a brief note.
3. If any item receives a FAIL result: do not submit the model. Correct the deficiency and re-check.
4. The completed checklist must be signed by the reviewer and stored in the CDE alongside the submitted model.
5. The BIM Lead may re-check any submitted model against this checklist at any time. Discrepancies between the checklist sign-off and the actual model are a serious compliance issue.

**Result Classifications:**
- **PASS:** All items checked and compliant. Model may be submitted.
- **CONDITIONAL PASS:** Minor non-critical items are noted but do not prevent submission. Corrective actions must be completed by [agreed date].
- **FAIL:** One or more critical items are non-compliant. Model must not be submitted until all FAIL items are resolved.

---

## HVAC BIM MODEL QA/QC CHECKLIST

**LUA BIM LABS | Project Mentor Template | PM-T02**
**Version:** 1.0

```
PROJECT: _________________________ DATE: ____________
MODEL VERSION / REVISION: _________________________
REVIEWER: ________________________ TITLE: __________
ORGANIZATION: _____________________________________
SUBMISSION TYPE: □ Coordination   □ Milestone Delivery   □ As-Built
```

---

### CATEGORY 1: SYSTEM SETUP

| # | Check Item | Pass | Fail | N/A | Notes |
|---|-----------|------|------|-----|-------|
| 1.01 | Shared coordinates are set to the project coordinate point (confirmed against reference structural model) | □ | □ | □ | |
| 1.02 | Project North is set correctly and matches the reference file | □ | □ | □ | |
| 1.03 | All levels in the HVAC model match the levels in the reference structural model (name and elevation) | □ | □ | □ | |
| 1.04 | All grid lines match the reference structural model exactly | □ | □ | □ | |
| 1.05 | All MEP systems are correctly defined in the model (Supply Air, Return Air, Exhaust Air, Chilled Water Supply, Chilled Water Return, Condenser Water, etc.) | □ | □ | □ | |
| 1.06 | No undefined or "Default" system assignments exist on any element in the active design | □ | □ | □ | |
| 1.07 | Worksets are correctly named and all elements are in the correct workset | □ | □ | □ | |
| 1.08 | Only HVAC elements are included in this model — no structural, architectural, or other MEP elements | □ | □ | □ | |

---

### CATEGORY 2: GEOMETRY AND ROUTING

| # | Check Item | Pass | Fail | N/A | Notes |
|---|-----------|------|------|-----|-------|
| 2.01 | All supply air ducts are modeled at the correct elevation (AFF) as per the latest coordination agreement | □ | □ | □ | |
| 2.02 | All return air ducts are modeled at the correct elevation and route | □ | □ | □ | |
| 2.03 | All duct sizes match the design engineer's duct sizing schedule | □ | □ | □ | |
| 2.04 | No ducts pass through structural members (beams, columns, slabs) without an approved opening | □ | □ | □ | |
| 2.05 | Minimum duct clearances are maintained (access for maintenance, filter servicing, joint inspection) | □ | □ | □ | |
| 2.06 | All AHU, FCU, and major plant items are modeled with correct clearance zones (maintenance access volumes) | □ | □ | □ | |
| 2.07 | Flexible duct connections are modeled where required (not extended rigid duct connections) | □ | □ | □ | |
| 2.08 | All duct transitions (reducers, offsets, elbows) are correctly modeled — no "floating" elements or unresolved transitions | □ | □ | □ | |
| 2.09 | All roof-mounted and plant-room equipment is placed at the correct elevation and orientation | □ | □ | □ | |
| 2.10 | All chilled water and condenser water piping is modeled at the correct elevation and system | □ | □ | □ | |

---

### CATEGORY 3: CONNECTIONS AND CONTINUITY

| # | Check Item | Pass | Fail | N/A | Notes |
|---|-----------|------|------|-----|-------|
| 3.01 | All duct runs are connected end-to-end — no open ends except at terminal units, equipment connections, or deliberate system boundaries | □ | □ | □ | |
| 3.02 | All terminal units (diffusers, grilles, fan coil units) are connected to their serving duct system | □ | □ | □ | |
| 3.03 | All pipe systems are connected — no open pipe ends except at intentional system boundaries | □ | □ | □ | |
| 3.04 | All mechanical equipment (AHU, chiller, cooling tower, pumps) is connected to their associated duct and pipe systems in the model | □ | □ | □ | |
| 3.05 | Valve locations are modeled correctly (isolation valves, balancing valves, control valves at locations specified in the design) | □ | □ | □ | |

---

### CATEGORY 4: PARAMETERS AND DATA

| # | Check Item | Pass | Fail | N/A | Notes |
|---|-----------|------|------|-----|-------|
| 4.01 | All ducts have the correct system classification parameter populated | □ | □ | □ | |
| 4.02 | All equipment has the "Equipment Mark" parameter populated with the reference from the mechanical schedule | □ | □ | □ | |
| 4.03 | All equipment has the "Manufacturer" and "Model Number" parameters populated (where specified in the design) | □ | □ | □ | |
| 4.04 | All elements have the correct LOD assigned (where LOD tracking parameters are required by the BEP) | □ | □ | □ | |
| 4.05 | No parameters contain placeholder text such as "TBD", "To Be Confirmed", or "Unknown" unless approved by BIM Lead | □ | □ | □ | |

---

### CATEGORY 5: NAMING CONVENTION COMPLIANCE

| # | Check Item | Pass | Fail | N/A | Notes |
|---|-----------|------|------|-----|-------|
| 5.01 | The model file name follows the project naming convention (Section 7 of BEP) | □ | □ | □ | |
| 5.02 | All duct system names match the approved system naming list from the BEP or CDE setup | □ | □ | □ | |
| 5.03 | All pipe system names match the approved system naming list | □ | □ | □ | |
| 5.04 | All view names follow the project naming convention | □ | □ | □ | |
| 5.05 | All sheet names and numbers follow the project naming convention | □ | □ | □ | |

---

### CATEGORY 6: MODEL HEALTH

| # | Check Item | Pass | Fail | N/A | Notes |
|---|-----------|------|------|-----|-------|
| 6.01 | Revit model has been run through the Warnings dialog — all critical warnings resolved | □ | □ | □ | |
| 6.02 | Total number of remaining warnings is within the agreed project limit ([X] warnings) | □ | □ | □ | |
| 6.03 | File size is within the agreed limit ([X] MB per discipline model) | □ | □ | □ | |
| 6.04 | No unused families remain loaded in the model (purge performed) | □ | □ | □ | |
| 6.05 | No unnecessary view templates or filters remain (purge performed) | □ | □ | □ | |
| 6.06 | Model has been saved and synchronized to the central file (if workshared) — no local-only elements | □ | □ | □ | |
| 6.07 | IFC export (if required) has been checked — all HVAC elements appear in the IFC viewer and are correctly classified | □ | □ | □ | |

---

### CATEGORY 7: LOD COMPLIANCE

| # | Check Item | Pass | Fail | N/A | Notes |
|---|-----------|------|------|-----|-------|
| 7.01 | All elements are modeled at or above the LOD required for this submission stage (per Section 4 of the BEP) | □ | □ | □ | |
| 7.02 | No elements are placeholders (symbolic representations) where the LOD requires actual geometry | □ | □ | □ | |
| 7.03 | Equipment clearance zones are modeled where required by the current LOD stage | □ | □ | □ | |
| 7.04 | All required parameter data is populated for the current LOD stage | □ | □ | □ | |

---

### HVAC QA/QC RESULT AND SIGN-OFF

```
Total Items Checked: _____ / 35
Items Passed: _____   Items Failed: _____   Items N/A: _____

Critical failures (any FAIL in Categories 1, 2, 3, or 6): □ Yes □ No

Result:
□ PASS — Model approved for submission
□ CONDITIONAL PASS — Minor items noted. Model may be submitted.
   Corrective actions required by: ____________
□ FAIL — Model must not be submitted. Correct all FAIL items and re-check.

Notes:
_________________________________________________________________
_________________________________________________________________
_________________________________________________________________

Reviewer Name: _________________________ Date: ________________
Reviewer Signature: _____________________________
Organization: _________________________

BIM Lead Verification (for milestone deliveries):
Name: _________________________ Date: ________________
Signature: _____________________________
```

---
---

## ELECTRICAL BIM MODEL QA/QC CHECKLIST

**LUA BIM LABS | Project Mentor Template | PM-T03**
**Version:** 1.0

```
PROJECT: _________________________ DATE: ____________
MODEL VERSION / REVISION: _________________________
REVIEWER: ________________________ TITLE: __________
ORGANIZATION: _____________________________________
SUBMISSION TYPE: □ Coordination   □ Milestone Delivery   □ As-Built
```

---

### CATEGORY 1: SYSTEM SETUP

| # | Check Item | Pass | Fail | N/A | Notes |
|---|-----------|------|------|-----|-------|
| 1.01 | Shared coordinates are set to the project coordinate point (confirmed against reference structural model) | □ | □ | □ | |
| 1.02 | Project North is set correctly | □ | □ | □ | |
| 1.03 | All levels match the structural reference model (name and elevation exactly) | □ | □ | □ | |
| 1.04 | All grid lines match the structural reference model | □ | □ | □ | |
| 1.05 | All electrical systems are defined and classified correctly (LV Power, Lighting, ELV, Data, Emergency Power, Fire Alarm, etc.) | □ | □ | □ | |
| 1.06 | No elements have "Default" or undefined system assignments | □ | □ | □ | |
| 1.07 | Worksets are correctly named and all elements are in the correct workset | □ | □ | □ | |
| 1.08 | Only electrical elements are included in this model — no HVAC, structural, or other MEP elements | □ | □ | □ | |

---

### CATEGORY 2: CABLE TRAY MODELING

| # | Check Item | Pass | Fail | N/A | Notes |
|---|-----------|------|------|-----|-------|
| 2.01 | All cable trays are modeled at the correct elevation (AFF) per the latest coordination agreement | □ | □ | □ | |
| 2.02 | Cable tray sizes match the design engineer's cable tray schedule | □ | □ | □ | |
| 2.03 | No cable trays pass through structural members without an approved opening | □ | □ | □ | |
| 2.04 | Minimum clearances above cable trays are maintained (for cable pulling and maintenance access) — typically 300mm above tray or as specified | □ | □ | □ | |
| 2.05 | All cable tray turns (elbows, tees, cross-pieces) are modeled — no abrupt straight-line breaks through walls or partitions | □ | □ | □ | |
| 2.06 | Cable tray support hanger positions are modeled (or noted as not required for this LOD stage) | □ | □ | □ | |
| 2.07 | Cable tray systems are separated by type (LV power, ELV/data, fire alarm) where required by the specification | □ | □ | □ | |
| 2.08 | All cable tray runs are continuous — no unexplained breaks or gaps in the routing | □ | □ | □ | |

---

### CATEGORY 3: PANEL BOARDS AND DISTRIBUTION BOARDS

| # | Check Item | Pass | Fail | N/A | Notes |
|---|-----------|------|------|-----|-------|
| 3.01 | All main switchboards (MSB), distribution boards (DB), and sub-distribution boards are modeled at correct location and elevation | □ | □ | □ | |
| 3.02 | Clearance zones (front and rear access) are modeled for all switchboards and distribution boards as per the specification and local code | □ | □ | □ | |
| 3.03 | Panel board room / electrical room dimensions are checked against the switchboard footprint + clearance zone — confirmed to fit | □ | □ | □ | |
| 3.04 | Riser shafts and vertical cable tray runs are modeled through all floors, correctly located and sized | □ | □ | □ | |
| 3.05 | All panel boards are connected to their associated cable tray or conduit feed in the model | □ | □ | □ | |

---

### CATEGORY 4: CONDUIT MODELING

| # | Check Item | Pass | Fail | N/A | Notes |
|---|-----------|------|------|-----|-------|
| 4.01 | All conduit runs are modeled where required by the current LOD stage (conduit modeling is typically required at LOD 300 for main runs, LOD 350 for all runs) | □ | □ | □ | |
| 4.02 | All conduit sizes are per the design schedule — no default sizes | □ | □ | □ | |
| 4.03 | All conduit runs are connected at both ends (from cable tray or DB to termination point or next junction) | □ | □ | □ | |
| 4.04 | Fire-rated conduit runs are correctly identified in the model (separate system classification or parameter) | □ | □ | □ | |
| 4.05 | No conduit runs penetrate structural members or slabs without a documented approved opening | □ | □ | □ | |

---

### CATEGORY 5: PARAMETERS AND DATA

| # | Check Item | Pass | Fail | N/A | Notes |
|---|-----------|------|------|-----|-------|
| 5.01 | All panel boards and switchboards have the "Equipment Mark" parameter populated per the electrical schedule | □ | □ | □ | |
| 5.02 | All cable trays have the system type parameter populated (Power / ELV / Fire / Data) | □ | □ | □ | |
| 5.03 | All major equipment (transformers, UPS, generators) has Manufacturer and Model Number populated where specified | □ | □ | □ | |
| 5.04 | All elements have the correct LOD parameter value (where tracking is required by the BEP) | □ | □ | □ | |
| 5.05 | No parameters contain "TBD," "Unknown," or placeholder text unless approved in writing by the BIM Lead | □ | □ | □ | |

---

### CATEGORY 6: NAMING CONVENTION COMPLIANCE

| # | Check Item | Pass | Fail | N/A | Notes |
|---|-----------|------|------|-----|-------|
| 6.01 | Model file name follows the project naming convention | □ | □ | □ | |
| 6.02 | All electrical system names match the approved system list from the BEP | □ | □ | □ | |
| 6.03 | All panel board and switchboard element marks match the electrical drawings and schedules | □ | □ | □ | |
| 6.04 | All view names follow the project naming convention | □ | □ | □ | |
| 6.05 | All sheet names and numbers follow the project naming convention | □ | □ | □ | |

---

### CATEGORY 7: MODEL HEALTH

| # | Check Item | Pass | Fail | N/A | Notes |
|---|-----------|------|------|-----|-------|
| 7.01 | Revit model Warnings dialog has been reviewed — all critical warnings resolved | □ | □ | □ | |
| 7.02 | Total warnings are within the agreed project limit | □ | □ | □ | |
| 7.03 | File size is within the agreed limit | □ | □ | □ | |
| 7.04 | Unused families have been purged from the model | □ | □ | □ | |
| 7.05 | Unused view templates and filters have been purged | □ | □ | □ | |
| 7.06 | Model has been synchronized to the central file — no local-only elements outstanding | □ | □ | □ | |
| 7.07 | IFC export (if required) has been checked — all electrical elements appear and are correctly classified | □ | □ | □ | |
| 7.08 | No duplicate elements exist (especially panel boards modeled twice — once as equipment and once as generic model) | □ | □ | □ | |

---

### ELECTRICAL QA/QC RESULT AND SIGN-OFF

```
Total Items Checked: _____ / 33
Items Passed: _____   Items Failed: _____   Items N/A: _____

Critical failures (any FAIL in Categories 1, 2, 3, or 7): □ Yes □ No

Result:
□ PASS — Model approved for submission
□ CONDITIONAL PASS — Minor items noted. Model may be submitted.
   Corrective actions required by: ____________
□ FAIL — Model must not be submitted. Correct all FAIL items and re-check.

Notes:
_________________________________________________________________
_________________________________________________________________
_________________________________________________________________

Reviewer Name: _________________________ Date: ________________
Reviewer Signature: _____________________________
Organization: _________________________

BIM Lead Verification (for milestone deliveries):
Name: _________________________ Date: ________________
Signature: _____________________________
```

---

## NOTES FOR THE BIM LEAD — RECEIVING THESE CHECKLISTS

When receiving a QA/QC checklist alongside a model submission:

1. **Verify the checklist is complete.** If any item is blank (not checked), return the checklist to the submitter for completion.

2. **Spot-check the model.** Do not assume the self-review is accurate. Open the model and verify at least 5 randomly selected items from the critical categories (1, 2, 3 for HVAC; 1, 2, 3 for Electrical). If the spot-check reveals items marked as "Pass" that are actually "Fail," issue a formal non-compliance notice to the submitting party.

3. **Log the result.** Record in the CDE and in the Master Issue Log: Submission Date, Reviewer, Result (Pass / Conditional / Fail), and any Conditional action items with deadlines.

4. **Maintain a running record.** Track each party's QA/QC compliance over time. Patterns of repeated failures are a project risk and should be escalated to the Project Manager.

---

*LUA BIM LABS Project Mentor Template Pack PM-T02/PM-T03 v1.0 — For subscriber use only.*
