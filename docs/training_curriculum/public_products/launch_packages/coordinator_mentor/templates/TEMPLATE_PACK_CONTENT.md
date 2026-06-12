# Coordinator Mentor — Template Pack Content
## LUA BIM LABS | 5 Templates for Immediate Use
**Version:** 1.0 | For distribution to all Coordinator Mentor clients at onboarding

---

# TEMPLATE 1: CLASH PRIORITY MATRIX

**File Name:** CM-T01_Clash_Priority_Matrix
**Format:** Excel / Google Sheets table
**Purpose:** Score and rank clashes to determine which ones to resolve first. Prevents teams from wasting time on low-impact clashes while critical ones are deferred.

---

## Instructions

1. Enter each clash (or clash group) as one row.
2. Score Impact, Urgency, and Difficulty from 1–5 using the scoring guide below.
3. The Priority Score column is a formula: **Impact × Urgency** (do not multiply by Difficulty — difficulty is tracked separately so you know which high-priority clashes are also complex).
4. Sort the table by Priority Score (high to low) before each coordination meeting.
5. Focus discussion time on clashes with a Priority Score of 15 or higher.

**Scoring Guide:**

| Score | Impact | Urgency | Difficulty |
|-------|--------|---------|------------|
| 1 | Cosmetic issue / no construction impact | Can wait more than 2 weeks | Can resolve in < 30 min |
| 2 | Minor rework / small area affected | Should resolve within 2 weeks | Requires 30 min–2 hours |
| 3 | Moderate rework / affects one floor or zone | Should resolve within 1 week | Requires 2–8 hours |
| 4 | Major rework / affects multiple floors | Should resolve within 3 days | Requires full design revision |
| 5 | Construction halt risk / structural/life safety concern | Resolve today or tomorrow | Requires multi-discipline agreement and redesign |

---

## Table Structure

| Clash ID | Clash Type | Disciplines Involved | Location (Grid / Level) | Description | Impact (1–5) | Urgency (1–5) | Difficulty (1–5) | Priority Score (Impact × Urgency) | Responsible Discipline | Target Resolution Date | Status | Resolution Notes |
|----------|------------|---------------------|------------------------|-------------|--------------|--------------|-----------------|----------------------------------|----------------------|----------------------|--------|-----------------|
| CL-001 | Hard | HVAC vs. Structural | Grid C3 / L03 | 800×400 HVAC supply duct penetrates 600-deep structural beam web at 3,200mm AFF. Beam cannot be modified. | 5 | 5 | 4 | 25 | HVAC | 2026-06-05 | Open | Reroute duct — HVAC designer notified 2026-05-28 |
| CL-002 | Hard | Electrical vs. HVAC | Grid E5 / L02 | 600×100 cable tray route conflicts with existing chilled water return pipe. 350mm overlap. | 4 | 4 | 2 | 16 | Electrical | 2026-06-08 | In Progress | Electrical to drop tray 200mm. Revised model expected by 2026-06-03. |
| CL-003 | Soft | Fire Sprinkler vs. Plumbing | Grid A1 / L01 | Sprinkler branch pipe and domestic water supply pipe within 50mm of each other in ceiling zone. No physical clash but clearance issue for maintenance. | 2 | 2 | 1 | 4 | Fire Sprinkler | 2026-06-15 | Open | Low priority. Review during next coordination pass. |

---

## Status Options (use consistently)

- **Open** — Clash identified, no action taken yet
- **In Progress** — Responsible discipline is working on resolution
- **Awaiting Design Input** — Resolution depends on a design decision not yet made
- **Awaiting Approval** — Proposed solution submitted, waiting for sign-off
- **Resolved** — Clash resolved; updated model received and confirmed
- **Accepted** — Clash accepted as-is (documented decision, not an oversight)
- **Cancelled** — Clash no longer exists due to design change

---

# TEMPLATE 2: COORDINATION MEETING AGENDA

**File Name:** CM-T02_Coordination_Meeting_Agenda
**Format:** Word / Google Docs
**Purpose:** A consistent meeting structure that ensures every coordination meeting produces clear outcomes and documented action items. Use this for every coordination meeting.

---

## MEETING HEADER

```
PROJECT: _______________________________________
MEETING TYPE: BIM Coordination Meeting
MEETING NUMBER: CM-[Project Code]-[Number] (e.g., CM-PRJ01-007)
DATE: _____________ TIME: _______ to _______
LOCATION / PLATFORM: ________________________________
CHAIR: _____________________________________________
PREPARED BY: _______________________________________
DISTRIBUTION: _______________________________________

ATTENDEES:
Name | Company | Discipline | Present (Y/N)
_____|_________|___________|______________
_____|_________|___________|______________
_____|_________|___________|______________
_____|_________|___________|______________
_____|_________|___________|______________
```

---

## STANDING AGENDA

### Item 1: Apologies and Quorum (5 minutes)
- Confirm attendance and note apologies
- Confirm quorum (at least [N] disciplines represented — adjust per project)
- Confirm that this meeting is valid to make decisions

**Notes:**
```
_________________________________________________________________
_________________________________________________________________
```

---

### Item 2: Previous Meeting Follow-Up (10 minutes)
- Review action items from Meeting [previous number]
- Status of each action item: Completed / In Progress / Overdue

**Action Item Review Table:**

| Ref | Action Item | Owner | Due Date | Status | Comments |
|-----|-------------|-------|----------|--------|----------|
| | | | | | |
| | | | | | |
| | | | | | |

**Escalation flag:** Were any overdue items flagged to the project manager? Yes / No / N/A

**Notes:**
```
_________________________________________________________________
```

---

### Item 3: New and Open Clash Review (20 minutes)
- Present the updated Clash Priority Matrix (sorted by Priority Score)
- Review all clashes with Priority Score ≥ 15 in detail
- For each: confirm responsible party, target date, and required action
- Review clashes that changed status since last meeting
- Identify any new clashes requiring urgent attention

**Clash Summary (updated from Clash Priority Matrix):**

| Category | Count This Meeting | Change from Last Meeting |
|----------|--------------------|--------------------------|
| Total Clashes | | |
| Critical (Score 20–25) | | |
| High (Score 12–19) | | |
| Medium (Score 6–11) | | |
| Low (Score 1–5) | | |
| Resolved This Week | | |
| New This Week | | |

**Key clashes discussed:**
```
Clash ID: ___ — Discussion: _______________________________
Clash ID: ___ — Discussion: _______________________________
Clash ID: ___ — Discussion: _______________________________
```

---

### Item 4: Design Change Impacts (10 minutes)
- Any design changes issued since the last meeting that affect coordination?
- Which previously resolved clashes are now reactivated?
- Who is responsible for impact assessment?

**Design Changes Noted:**

| Change Reference | Description | Issuing Discipline | Impact on Clashes | Assessment By | Due By |
|-----------------|-------------|-------------------|-------------------|--------------|--------|
| | | | | | |

**Notes:**
```
_________________________________________________________________
_________________________________________________________________
```

---

### Item 5: New Business and Escalations (5 minutes)
- Any items requiring decision from those not in the room?
- Coordination timeline risks — is the program at risk?
- Upcoming model submission dates
- Any information requests outstanding

**Notes:**
```
_________________________________________________________________
_________________________________________________________________
```

---

### Item 6: Next Steps and Close (5 minutes)
- Confirm all action items below are logged
- Confirm date, time, and location of next coordination meeting
- Next Meeting: _____________ at _______ | Location: _____________

---

## ACTION ITEM TABLE (complete before closing the meeting)

| # | Action | Owner | Discipline | Target Date | Priority |
|---|--------|-------|------------|-------------|----------|
| 1 | | | | | |
| 2 | | | | | |
| 3 | | | | | |
| 4 | | | | | |
| 5 | | | | | |

**Total action items this meeting:** ___
**Meeting closed at:** _______
**Minutes prepared by:** _______
**Minutes distribution date:** _______

---

*Note to Chair: Distribute meeting minutes within 24 hours. All attendees have 2 business days to raise corrections. After that, the minutes stand as the official record.*

---

# TEMPLATE 3: ISSUE LOG MASTER

**File Name:** CM-T03_Issue_Log_Master
**Format:** Excel / Google Sheets
**Purpose:** The single source of truth for all coordination issues on a project. Every clash, concern, and coordination problem is tracked here. This document is the permanent record — clash detection reports are inputs to this log, not replacements for it.

---

## Usage Instructions

1. Create one Issue Log per project. Store it in the project's Common Data Environment (CDE).
2. Every coordination issue — whether from clash detection, site observation, RFI, or design review — gets its own row.
3. Never delete rows. If an issue is cancelled, set Status to "Cancelled" with a note.
4. The Issue Log is presented at every coordination meeting. Update it before each meeting, not after.
5. Issue IDs never repeat. Once a number is used, it stays in the log permanently.
6. Include a hyperlink to evidence (clash report export, screenshot, RFI document) in the Evidence Reference column.

**Issue ID Format:** `[Project Code]-ISS-[4-digit number]` (e.g., PRJ01-ISS-0001)

---

## Table Structure

| Issue ID | Date Raised | Raised By | Discipline | Location (Grid / Level) | Description | Clash ID Reference | Priority (Critical / High / Medium / Low) | Status | Assigned To | Target Date | Resolution Date | Resolution Description | Evidence Reference |
|----------|-------------|-----------|------------|------------------------|-------------|-------------------|------------------------------------------|--------|-------------|-------------|----------------|----------------------|-------------------|
| PRJ01-ISS-0001 | 2026-05-28 | Chen Wei | HVAC | Grid C3 / L03 | 800×400 HVAC supply duct conflicts with 600-deep structural beam web at 3,200mm AFF. Duct cannot pass above or below without exceeding ceiling height constraint. | CL-001 | Critical | In Progress | HVAC Designer | 2026-06-05 | — | — | [Link to Navisworks clash report, Slide 3] |
| PRJ01-ISS-0002 | 2026-05-28 | Liu Fang | Electrical | Grid E5 / L02 | 600×100 electrical cable tray route crosses chilled water return pipe, 350mm overlap. Tray can be repositioned but needs CHW pipe rerouting confirmation. | CL-002 | High | In Progress | Electrical Eng. | 2026-06-08 | — | — | [Link to Clash Screenshot 0002] |
| PRJ01-ISS-0003 | 2026-05-20 | Park Min | Structural | Grid B2 / L04 | Structural beam depth revised from 500mm to 650mm in revised structural drawings Rev B. All MEP runs in this zone need to be re-checked. | N/A (design change) | Critical | Resolved | All MEP Leads | 2026-05-27 | 2026-05-26 | All MEP leads completed re-clash check against revised structural model Rev B. 14 new clashes identified — logged as ISS-0015 through ISS-0028. | [Link to Structural Rev B drawings, email confirmation from All] |

---

## Status Glossary

| Status | Meaning |
|--------|---------|
| Open | Issue logged, no action taken |
| In Progress | Responsible party is working on resolution |
| Awaiting Input | Blocked — waiting for information or decision from another party |
| Awaiting Approval | Proposed solution submitted; pending sign-off |
| Resolved | Issue resolved; confirmed in updated model |
| Accepted | Issue acknowledged and formally accepted as-is (documented decision) |
| Cancelled | Issue no longer exists (e.g., due to design change that removes the problem) |

---

# TEMPLATE 4: CLASH GROUP NAMING CONVENTION GUIDE

**File Name:** CM-T04_Clash_Group_Naming_Convention_Guide
**Format:** PDF / Word document
**Purpose:** To establish consistent, self-describing clash group names that any team member can understand without needing to open the clash — and that can be sorted, filtered, and reported on systematically.

---

## Why Naming Convention Matters

If you've ever opened a clash detection file and seen clash groups named "Clash Group 1," "Clash Group 2," "MEP clashes," or the subcontractor's initials, you already know the problem: these names tell you nothing about what the clashes are, where they are, or who owns them.

Poor naming creates three concrete problems:

**1. Time wasted in meetings.** When the agenda says "review Group 3," you have to open the software and look. A well-named group tells you everything before you even open it.

**2. Lost clashes.** Without a systematic naming system, groups get created by different people in different formats, making it impossible to search, filter, or track trends over time.

**3. No accountability.** If the clash group doesn't clearly identify which disciplines are involved, responsibility is unclear. "HVAC vs. Electrical" is unambiguous. "MEP clashes" is not.

A consistent naming convention solves all three problems. It takes 10 minutes to set up and saves hours over the life of a project.

---

## Recommended Naming Format

```
[PROJECT]-[CG]-[DISCIPLINE PAIR]-[LOCATION]-[NUMBER]
```

**Example:** `PRJ-CG-HVAC-ELEC-L03-001`

---

## What Each Field Means

**[PROJECT]** — Project code. Use the official project abbreviation from the BEP or project directory. Keep it short (3–6 characters). Consistent across all project documents.
- Examples: `PRJ`, `HSP1`, `TWR2`, `DC05`
- Do not use: full project names, spaces, special characters

**[CG]** — This is always "CG" and stands for Clash Group. It's a fixed delimiter that makes it immediately clear this is a clash group name, not a drawing number or document reference.

**[DISCIPLINE PAIR]** — The two disciplines involved in the clash, separated by a hyphen. Use standard discipline abbreviations (see table below). Always write them in the same order: use the list below to determine which discipline comes first.

Discipline priority order (first listed = appears first in the name):
1. HVAC (heating, ventilation, air conditioning)
2. MECH (mechanical — used when not specifically HVAC)
3. PLMB (plumbing)
4. FP (fire protection)
5. ELEC (electrical — power, lighting, data, comms)
6. STRUC (structural — beams, columns, slabs, foundations)
7. ARCH (architectural — walls, ceilings, floors, finishes)
8. CIVIL (civil works)

So: HVAC vs. Electrical = `HVAC-ELEC` (not ELEC-HVAC)
Structural vs. HVAC = `HVAC-STRUC` (not STRUC-HVAC)

**[LOCATION]** — The location identifier. This is usually a level (floor) reference, a grid zone, or a combination of both. Use the project's official level and grid naming.

Location formats:
- By level: `L01`, `L02`, `L03`, `RF` (roof), `B1` (basement 1)
- By zone: `ZA`, `ZB`, `ZC` (if the project uses zone designations)
- By grid area: `G-C3D4` (for a specific grid bay — keep it short)
- Combined: `L03-ZA` (level 3, Zone A)

If a clash group spans multiple levels, use the lowest level: `L02` for a group that crosses L02 to L04.

**[NUMBER]** — A 3-digit sequential number (001, 002, 003...) that distinguishes multiple groups with the same discipline pair and location. Reset per project, not per clash detection run.

---

## How to Group Clashes Before Naming

Before you name a clash group, you need to create the group. Here is the grouping logic:

**Step 1 — Filter by discipline pair.** Run your clash detection with disciplines separated. Do not run "all MEP vs. all MEP" in one test. Run HVAC vs. Structural, HVAC vs. Electrical, Electrical vs. Structural, etc. separately.

**Step 2 — Filter by location.** For each discipline pair result, filter by level or zone. Clashes on L03 go into one group. Clashes on L04 go into another. This is critical: combining all levels into one group makes it impossible to delegate resolution to the right team.

**Step 3 — Separate by type (Hard vs. Soft), if needed.** If a discipline pair and location has a large number of both hard and soft clashes, create two groups: one for hard clashes (`-H`), one for soft (`-S`). Only do this if there are more than 20 clashes of each type in the same group, or if the resolution process is different.

**Step 4 — Name the group.** Apply the naming format.

**Step 5 — Log the group.** Enter the group name, discipline pair, location, and number of clashes into the Issue Log Master.

---

## Good vs. Bad Naming Examples

| Bad Name | Problem | Good Name |
|----------|---------|-----------|
| Clash Group 1 | Tells you nothing | PRJ-CG-HVAC-STRUC-L03-001 |
| MEP clashes | Which MEP? Which location? | PRJ-CG-HVAC-ELEC-L02-001 |
| Electrical issue | Which issue? Against what? | PRJ-CG-ELEC-STRUC-B1-001 |
| L3 HVAC | No discipline pair, no number | PRJ-CG-HVAC-ARCH-L03-001 |
| John's clashes | Named by person — changes over time | PRJ-CG-PLMB-STRUC-L05-001 |
| 2024-05-28 | Date is not a group identifier | PRJ-CG-FP-HVAC-RF-001 |
| New | Meaningless as soon as it's no longer new | PRJ-CG-HVAC-ELEC-L01-003 |

---

## Quick Reference: When to Create a New Group vs. Add to Existing

**Create a new group when:**
- The discipline pair changes (HVAC-ELEC vs. HVAC-STRUC = two groups)
- The location changes (L02 vs. L03 = two groups)
- A new clash detection run reveals additional clashes after the original group is already being tracked in meetings

**Add to an existing group when:**
- A subcontractor resubmits a model and there are new clashes of the same discipline pair and location
- You split a group and realize the split was wrong — merge them back under the same name

---

## Applying the Naming Convention in Navisworks

In Navisworks Manage:
1. In the Clash Detective panel, select "Add Test" for each discipline pair.
2. After running the test, select clashes on the same level.
3. Right-click → Group → apply the name.
4. Export to HTML or Excel after naming — the group names will carry through to the report.

**Important:** Name your groups before you export or share the clash report. Do not share unnamed or auto-numbered groups outside your team.

---

# TEMPLATE 5: WEEKLY CLASH STATUS REPORT

**File Name:** CM-T05_Weekly_Clash_Status_Report
**Format:** Word / Google Docs
**Purpose:** A concise, consistent report distributed to the project team (or client) every week summarizing the status of clash resolution. This is not the same as meeting minutes — it is a standalone data document that shows progress and accountability.

---

## REPORT HEADER

```
─────────────────────────────────────────────────
WEEKLY CLASH STATUS REPORT
─────────────────────────────────────────────────
Project: ___________________________________________
Report Week: Week [N] | [DD MMM] – [DD MMM YYYY]
Prepared By: _______________________________________
Date Issued: _______________________________________
Distribution: ______________________________________
─────────────────────────────────────────────────
```

---

## SECTION 1: EXECUTIVE SUMMARY

```
Total Clashes This Week: ___
New This Week: ___ | Resolved This Week: ___ | Net Change: ___
Critical Clashes (Score 20–25) Outstanding: ___

Overall Status: □ On Track   □ At Risk   □ Behind Schedule

Key Message (1–2 sentences — what does the project team most need to know this week?):
___________________________________________________________________
___________________________________________________________________
```

---

## SECTION 2: CLASH SUMMARY BY DISCIPLINE PAIR

| Discipline Pair | New This Week | Resolved This Week | Pending (Open + In Progress) | Total in Log |
|----------------|--------------|-------------------|------------------------------|-------------|
| HVAC vs. Structural | | | | |
| HVAC vs. Electrical | | | | |
| HVAC vs. Plumbing | | | | |
| HVAC vs. Fire Protection | | | | |
| Electrical vs. Structural | | | | |
| Plumbing vs. Structural | | | | |
| Fire Protection vs. Structural | | | | |
| Other / Multi-Discipline | | | | |
| **TOTAL** | | | | |

---

## SECTION 3: TOP 5 PRIORITY CLASHES

*Clashes with the highest Priority Score (Impact × Urgency) that are currently unresolved.*

| Rank | Clash ID | Discipline Pair | Location | Description | Priority Score | Responsible | Target Date | Status |
|------|----------|----------------|----------|-------------|---------------|-------------|-------------|--------|
| 1 | | | | | | | | |
| 2 | | | | | | | | |
| 3 | | | | | | | | |
| 4 | | | | | | | | |
| 5 | | | | | | | | |

**Note on Top Priority Clashes:**
```
___________________________________________________________________
___________________________________________________________________
```

---

## SECTION 4: ACTION ITEMS FROM LAST WEEK

| # | Action Item | Owner | Due Date | Status | Comments |
|---|-------------|-------|----------|--------|----------|
| 1 | | | | □ Complete □ Pending □ Overdue | |
| 2 | | | | □ Complete □ Pending □ Overdue | |
| 3 | | | | □ Complete □ Pending □ Overdue | |
| 4 | | | | □ Complete □ Pending □ Overdue | |
| 5 | | | | □ Complete □ Pending □ Overdue | |

**Overdue items (explain if any):**
```
___________________________________________________________________
```

---

## SECTION 5: ACTION ITEMS FOR NEXT WEEK

| # | Action Item | Owner | Discipline | Target Date |
|---|-------------|-------|------------|-------------|
| 1 | | | | |
| 2 | | | | |
| 3 | | | | |
| 4 | | | | |
| 5 | | | | |

---

## SECTION 6: RISKS AND ISSUES

*Flag any coordination risks that the project team or project manager needs to be aware of.*

```
Risk 1: ____________________________________________
Impact: _____________ Mitigation: _________________

Risk 2: ____________________________________________
Impact: _____________ Mitigation: _________________
```

If no risks: *"No coordination risks to report this week."*

---

## SIGN-OFF

```
Prepared By: _______________________ Date: _______
BIM Coordinator: ___________________ Date: _______
Reviewed By (if applicable): _______ Date: _______

Next Report Due: [date]
Next Coordination Meeting: [date and time]
─────────────────────────────────────────────────
```

---

## Formatting and Distribution Notes

- This report is sent every Friday by close of business (or Monday morning if Friday is not possible).
- Distribute by email to: [project lead, all discipline leads, client representative — adjust per project].
- Keep it concise. If a section has nothing to report, write "None this week" — do not leave it blank.
- Attach the updated Clash Priority Matrix as an appendix (exported from Excel as PDF) if the project manager requests it.
- Archive all issued reports in the CDE under: [Project] / Coordination / Reports / Weekly Clash Status Reports / [Year] / [Week Number].

---

*LUA BIM LABS Template Pack v1.0 — For use by Coordinator Mentor subscribers only. Do not redistribute.*
