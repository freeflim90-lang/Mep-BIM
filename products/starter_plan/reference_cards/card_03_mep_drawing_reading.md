# MEP Drawing Reading Guide
**LUA BIM LABS Starter — Track 3 Quick Reference**
*Track completion card — Day 21*

---

## Drawing Types Reference

| Drawing Type | Definition | Created By | Primary Use |
|---|---|---|---|
| Design Drawing | Shows the engineer's design intent — system layout, sizes, and specification | Design Engineer | Basis for BIM modeling and procurement |
| Coordination Drawing | Shows clash-resolved MEP routing confirmed for construction — includes elevations and grid references | BIM Coordinator | Site installation and setting-out |
| Shop Drawing | Shows fabrication-level detail for manufacture — includes cut lengths, flanges, bolt patterns | Contractor / Fabricator | Off-site manufacturing (spools, panels) |
| As-Built Drawing | Records the actual installed condition — deviations from design captured | Contractor (BIM-assisted) | Facility management and handover |

---

## MEP Plan Reading Tips

**HVAC Plans — what to check:**
- Supply air routes from AHU to diffusers (confirm system assignment on each duct)
- Return air routes from grilles back to AHU (do not confuse with supply)
- VAV box locations and connected branch ducts
- Equipment tags (AHU, FCU, EF) matching the equipment schedule
- Duct size annotations at key routing changes

**Piping Plans — what to check:**
- Flow direction arrows on supply and return lines
- Pipe size annotations — confirm they match the design specification
- Valve symbols — isolation valves, check valves, pressure regulators
- Equipment connection points (pumps, coils, heat exchangers)
- Drain and vent pipe routes for sanitary systems (look for slope notation)

**Electrical Plans — what to check:**
- Cable tray routing from main switchboard to distribution boards
- Panel board locations matching the single-line diagram
- Circuit homerun lines from panels to major equipment
- Conduit routes and junction box positions
- Load labels on distribution equipment

---

## Schematic Symbols Reference

| System | Common Symbols |
|---|---|
| HVAC Supply Air | Solid rectangle duct in plan; arrow showing flow direction |
| HVAC Return Air | Dashed rectangle duct in plan; arrow reversed toward AHU |
| Chilled Water | CWS (supply) and CWR (return) with flow arrows |
| Hot Water | HWS and HWR labeled, with isolating valve symbols |
| Drainage (gravity) | Dashed line with slope notation (e.g., 1:50) |
| Sprinkler | Solid pipe line with "X" or dot symbols for heads |
| Cable Tray | Double-line rectangle in plan; size labeled (e.g., 600×100) |
| Conduit | Single line with size callout; homerun arrows to panel |

---

## Coordination vs. Design Drawing Differences

| | Design Drawing | Coordination Drawing |
|---|---|---|
| **Purpose** | Show design intent | Show clash-resolved routing for installation |
| **LOD** | LOD 200–300 | LOD 350 |
| **Elevation data** | Approximate or not shown | Confirmed pipe inverts and duct soffit levels |
| **Structural reference** | May not include beams | Structural grid and key beams shown |
| **Clash status** | Not applicable | All Major clashes resolved before issue |
| **Issued by** | Design Engineer | BIM Coordinator |
| **Used by** | Modeling team, QA | Site installation teams |

---
*LUA BIM LABS | Practical BIM Education for MEP*
*Educational reference only — not project specification or code compliance guidance.*
