# Site-Readiness Check Guide
**LUA BIM LABS Starter — Track 7 Quick Reference**
*Track completion card — Day 54*

---

## What Site Teams Need from BIM

| Output | Format | Purpose |
|---|---|---|
| Coordination Drawings | A1/A3 prints, PDF | Shows MEP routing with confirmed elevations and grid references for each zone |
| Setting-Out Data | Dimension tables, grid-referenced drawings | Marks hole positions, hanger spacings, and equipment base locations on slab or wall |
| Model Access (Viewer) | NWD file, Autodesk Viewer link, BIM 360 Docs | Site supervisors navigate 3D model to understand spatial relationships |
| Clash Clearance Sign-off | Written memo or tracker export | Confirms all Critical and Major clashes in the zone are resolved before work starts |
| Spool Drawings | ISO drawings (isometric), spool delivery schedule | Pre-fabricated assemblies matched to site by unique spool ID tag |
| RFI Response | Written RFI response (within 24 hours) | Formal resolution when site conditions differ from model or drawings |

---

## RFI Process Flow

```
Site condition differs from model or drawing
        ↓
Site supervisor raises formal RFI
(Assigned RFI number, description, photo)
        ↓
RFI submitted to BIM Coordinator / Engineer
        ↓
BIM Coordinator / Engineer reviews model + site info
        ↓
Response issued within agreed timeframe (typically 24–48 hours)
        ↓
If model change required:
  → Model updated, drawings reissued at new revision
        ↓
RFI closed with reference to resolution in issue tracker
        ↓
Deviation captured in as-built record if site differs from revised model
```

---

## As-Built Update Checklist

When installation deviates from the BIM model:
- [ ] Deviation identified and described (element, location, nature of change)
- [ ] RFI raised and formally responded to
- [ ] BIM modeler updates the model to reflect actual installed position
- [ ] Updated model version saved with "AS-BUILT" in the file name
- [ ] Revised coordination drawing issued at a new revision
- [ ] Site team notified of updated drawing and old revision superseded
- [ ] Deviation logged in the project change register

---

## Spool Drawing Basics

| Term | Meaning |
|---|---|
| Spool | Pre-built section of pipework or ductwork (with fittings, flanges, supports) — manufactured off-site |
| ISO Drawing | Isometric view spool drawing showing 3D routing, all connections, and dimensions |
| Cut Length | Exact length of each straight pipe segment, accounting for fitting allowances |
| Spool ID | Unique tag on each spool matching the spool drawing — site installs by matching tag to drawing |
| End Preparation | Type of joint at each spool end (flanged, grooved, butt-welded) |
| BIM-to-Fabrication | Model must be at LOD 350, clash-resolved, before spool drawings are generated |

---

## Common Site-to-BIM Feedback Types

| Feedback Type | Typical Cause | BIM Response |
|---|---|---|
| Slab deviation | Floor poured out of level — not as modeled | Survey actual level, adjust model elevation, reissue coordination drawing |
| Structure out of position | Column or beam installed offset from design | RFI to structural engineer, update model if accepted, recheck clashes |
| Service omitted from model | Design change issued to site but not captured in BIM | Model update required, all affected coordination drawings reissued |
| Insufficient clearance on site | Void tighter than modeled due to finishes thickness | Check finish build-up, adjust model with confirmed data, re-coordinate |
| Fitting not available (procurement) | Specified fitting type unavailable or substituted | Engineer approval for substitution, model updated with alternate family |

---
*LUA BIM LABS | Practical BIM Education for MEP*
*Educational reference only — not project specification or code compliance guidance.*
