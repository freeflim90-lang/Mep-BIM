# Model Quality Self-Review Checklist
**LUA BIM LABS Starter — Track 4 Quick Reference**
*Track completion card — Day 28*

---

## 4-Area Quality Framework

Model quality is verified across four areas. Complete all 20 checks before submitting any MEP model.

---

### Area 1: Geometry

- [ ] All elements are placed at correct elevations using numeric offsets — not visually estimated
- [ ] No elements floating in space, buried in a slab, or placed off-grid
- [ ] All ducts and pipes have valid, confirmed sizes (not default or approximate)
- [ ] Equipment is placed at correct position relative to structural grids
- [ ] No duplicate elements at the same location (check with Manage > Review Warnings)

### Area 2: Data / Parameters

- [ ] All elements have a unique Mark value — no blanks, no duplicates
- [ ] All elements are assigned to a named system (no "Default" or unnamed systems)
- [ ] Required parameters are populated: Size, Level, System Name, Material/Specification
- [ ] Equipment tags match the design drawing or equipment schedule
- [ ] File name follows the project BEP naming convention

### Area 3: System Connections

- [ ] All duct and pipe ends are connected — no open connectors
- [ ] The Systems Browser shows no unassigned or "unnamed" systems
- [ ] Equipment (AHU, pump, panel) is connected to its associated ductwork or pipework
- [ ] Gravity drainage is modeled with required slope (not flat) — typically 1:50 for drainage
- [ ] System Inspector shows zero errors for each active system

### Area 4: Coordination Readiness

- [ ] All linked models are loaded and up to date (not broken links)
- [ ] Shared coordinates confirmed — model aligns with architectural base
- [ ] Model purged of unused families and types (File > Purge Unused)
- [ ] Revit warnings reviewed — critical warnings resolved or documented
- [ ] File synchronized to the central model before handover

---

## LOD Self-Check Table

| LOD | Geometry Confirmed | Parameters Populated | Hangers / Supports Included | Clash-Checked |
|---|---|---|---|---|
| LOD 200 | Approximate | Minimal | No | No |
| LOD 300 | Accurate | Core fields filled | No | Optional |
| LOD 350 | Accurate | Full set required | Yes | Yes — required |
| LOD 400 | Fabrication detail | All fields including manufacturer | Yes (detailed) | Yes |
| LOD 500 | As-installed | All fields + field verification | As installed | N/A — record |

---

## Quick Reference: Common Errors to Check

| Error | Where to Check |
|---|---|
| Open connectors | Systems Browser — unhosted elements |
| Wrong system type | Properties panel → System Classification |
| Blank Mark | Schedule view, sort by Mark field |
| Warnings count | Manage tab → Review Warnings |
| File size (large) | File > Purge Unused; check RVT file size |

---
*LUA BIM LABS | Practical BIM Education for MEP*
*Educational reference only — not project specification or code compliance guidance.*
