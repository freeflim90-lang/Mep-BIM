# Revit MEP Setup Checklist
**LUA BIM LABS Starter — Track 2 Quick Reference**
*Track completion card — Day 14*

---

## Project Setup Checklist

**Levels and Grids**
- [ ] Levels are copied or monitored from the architectural/structural model — not created independently
- [ ] Floor-to-floor heights verified against the architectural model
- [ ] Level names match the project naming convention (e.g., L01, B1, RF)
- [ ] Structural grids are visible in MEP plan views for spatial reference

**Shared Coordinates**
- [ ] Architectural model is linked into the MEP model
- [ ] Shared coordinates acquired from the architectural model
- [ ] Survey point and project base point confirmed — not moved by the MEP team
- [ ] All discipline models (HVAC, piping, electrical) align to the same shared coordinate base

**Worksets**
- [ ] Worksets created per discipline or system (e.g., HVAC, Plumbing, Electrical, Linked Models)
- [ ] Each workset assigned to a responsible team member or role
- [ ] Central file saved to the project CDE — not a local desktop folder
- [ ] All modelers working from local copies, not the central file directly

**Linked Models**
- [ ] Architectural model linked and pinned
- [ ] Structural model linked and pinned
- [ ] Other MEP discipline models linked for coordination reference
- [ ] All link paths verified (not broken) before modeling starts

**Discipline-Specific Settings**
- [ ] Correct Revit MEP template selected (Mechanical, Electrical, or Plumbing)
- [ ] View discipline filter set to the correct MEP system per view
- [ ] View range set to capture the ceiling MEP zone (cut height and bottom offset confirmed)
- [ ] Linked model visibility set to Halftone so MEP elements are visually distinct

---

## System Naming Conventions

| Element | Example Format | Notes |
|---|---|---|
| File name | `[Project]-[Disc]-[Level]-[Author]-[Date].rvt` | e.g., `PRJ-MECH-ALL-LUA-20260529.rvt` |
| System name | `HVAC-SA-L03` | HVAC, Supply Air, Level 3 |
| Equipment tag | `AHU-01-L03` | Air Handling Unit 01, Level 3 |
| Plan view | `MEP-MECH-L03-PLAN` | MEP, Mechanical, Level 3, Plan |
| Coordination view | `3D-COORD-ZONE-A` | Zone A coordination 3D view |

---

## Template Verification Items

Before modeling begins, verify:
- [ ] Correct MEP template is active (check File > Project Information)
- [ ] System types exist for all required systems (Supply Air, Return Air, Chilled Water Supply, etc.)
- [ ] Family library path is accessible and project-specific families are loaded
- [ ] Revision table and title block are set up on sheet templates
- [ ] View templates for each discipline are created and applied

---
*LUA BIM LABS | Practical BIM Education for MEP*
*Educational reference only — not project specification or code compliance guidance.*
