# BIM Coordination Automation Package — Master Index

This index defines the reading order, implementation phases, and purpose of each document in this package. **Start here.**

---

## Implementation Phases

### Phase 1 — Standards and Templates
Establish standards before any automation. No scripting required.

| Action | Reference |
|---|---|
| Define coordination workflow and weekly schedule | `BIM Coordination 101.md` |
| Establish clash matrix and Navisworks rule templates | `BIM Coordination 101.md` |
| Build Revit project template (.RTE) with worksets, views, view templates | `BIM Revit model setup automation.md` (Steps 1–2) |
| Set up ACC folder structure and permissions | `BIM Autpmatic Coordination System.md` (Part 10) |
| Define BIM Standards Manual | `BIM Autpmatic Coordination System.md` (Part 12) |

---

### Phase 2 — pyRevit Toolbar and Project Setup Automation
Deploy the coordinator toolbar and automate new project initialization.

| Action | Reference |
|---|---|
| Build pyRevit BIM Coordinator Toolbar (40 tools) | `BIM Coordination Toolbar design doc.md` |
| Script: Initialize Project (worksets, views, sheets, links, coordinates) | `BIM Revit model setup automation.md` (Steps 3–14) |
| Train team on BIM coordination fundamentals | `BIM Coordination 101.md` |
| Train senior coordinators on advanced workflows | `BIM Coordination Advanced.md` |
| Troubleshooting reference | `BIM Troubleshooting Mega-Guide.md` |

---

### Phase 3 — Model Health Scoring and Clash Automation
Automate quality checks and clash processing.

| Action | Reference |
|---|---|
| Deploy pyRevit 150-point model health scorer | `BIM Score implementation Plan.md` |
| Scoring rubric reference | `BIM scoring system.md` |
| Script: Navisworks clash grouping (Python) | `BIM Coordination Automation Toolkit.md` (Tool 1) |
| Script: Clash prioritization engine | `BIM Coordination Automation Toolkit.md` (Tool 4) |
| Script: Model health checker (simpler version) | `BIM automation plan.md` (Section 1) |

---

### Phase 4 — ACC Issue Automation and Command Center Dashboard
Close the loop from clash to issue to dashboard.

| Action | Reference |
|---|---|
| Script: Automatic ACC issue creation | `BIM Coordination Automation Toolkit.md` (Tool 2) |
| Script: Weekly coordination report generator | `BIM Coordination Automation Toolkit.md` (Tool 3) |
| Build Power BI Command Center dashboard | `BIM Command Center.md` |
| Build clash heat map visualization | `BIM clash heat map.md` |
| Full system architecture overview | `BIM Autpmatic Coordination System.md` |

---

### Phase 5 — Portfolio Governance and Predictive Intelligence *(Advanced Tier)*
Enterprise-scale BIM governance across multiple projects. Supersedes the simpler CSV approach from Phases 3–4.

| Action | Reference |
|---|---|
| Deploy pyRevit CPython portfolio exporter (all fact tables) | `BIM compliance dashboard Requirements.md` |
| Migrate shared parameters to `Portfolio_` convention | `BIM compliance dashboard Requirements.md` (Shared Parameters section) |
| Build governance scoring engine in Power BI | `BIM compliance dashboard Requirements.md` (Governance Engine section) |
| Build predictive velocity measures | `BIM compliance dashboard Requirements.md` (Predictive Engine section) |

> **Note:** Phase 5 supersedes the simple CSV exports from Phases 3–4 and introduces the `Portfolio_` shared parameter convention. See the migration note in each earlier file for the transition path.

---

## Canonical Standards (Quick Reference)

### Weekly Workflow

| Day | Activity |
|---|---|
| Monday | Model uploads (deadline for all disciplines) |
| Tuesday | Clash tests run in Navisworks |
| Wednesday | Automation scripts process clashes; clash groups generated; heat map updated |
| Thursday | ACC issues created automatically; Power BI dashboard refreshed |
| Friday | Coordination meeting using dashboards and heat maps |

---

### Model Health Score Thresholds (150-point scale)

| Score | Status | Action |
|---|---|---|
| 130–150 | Elite | No action needed |
| 115–129 | Excellent | Monitor |
| 100–114 | Healthy | Minimum for coordination entry |
| 85–99 | Needs Cleanup | Notify team; remediate before next cycle |
| Below 85 | Critical | Reject from coordination |

---

### Warning Count Target

| Warnings | Assessment |
|---|---|
| < 300 | Ideal |
| 300–1,000 | Acceptable |
| > 1,000 | Flag for cleanup |

---

### Clash Tolerance Standards

| Test Type | Tolerance |
|---|---|
| Hard clash (structural vs MEP) | 0 inches |
| MEP internal clearance | 1–2 inches |
| Equipment maintenance clearance | 24–36 inches |

---

### Point Cloud / LiDAR Standards

| Format | Use |
|---|---|
| RCP / RCS (ReCap) | Linked into Revit (Scan workset); appended in Navisworks for visual reference |
| RCMR (Revit Scan Mesh) | Linked into Revit (Scan workset) as mesh visual reference |

**Key rules:**
- Point clouds are **visual reference overlays only** — not used for formal clash detection
- All RCP/RCMR files must be placed on the **Scan workset** in Revit
- AutoCAD and CADWorx users may reference RCP files directly in their authoring environment
- Standard view: **3D - Scan Reference** (created during project initialization)

---

### Model File Size Target

| Size | Assessment |
|---|---|
| < 300 MB | Ideal |
| < 500 MB | Acceptable |
| > 500 MB | Flag for cleanup |

---

## File Map

| File | Type | Phase |
|---|---|---|
| `BIM Coordination Package - Index.md` | Master index | All |
| `BIM Coordination 101.md` | Training | 1–2 |
| `BIM Coordination Advanced.md` | Training | 2 |
| `BIM Troubleshooting Mega-Guide.md` | Reference | 2+ |
| `BIM Autpmatic Coordination System.md` | System overview | 1–4 |
| `BIM Revit model setup automation.md` | Implementation | 2 |
| `BIM Coordination Toolbar design doc.md` | Implementation | 2 |
| `BIM scoring system.md` | Standard / rubric | 3 |
| `BIM Score implementation Plan.md` | Implementation | 3 |
| `BIM automation plan.md` | Implementation | 3 |
| `BIM Coordination Automation Toolkit.md` | Implementation | 3–4 |
| `BIM clash heat map.md` | Implementation | 4 |
| `BIM Command Center.md` | Implementation | 4 |
| `BIM compliance dashboard Requirements.md` | Implementation | 5 |
