# MEP Data & Schedule Reference
**LUA BIM LABS Starter — Track 6 Quick Reference**
*Track completion card — Day 47*

---

## Revit Schedule Types by Discipline

| Discipline | Schedule Type | Primary Purpose |
|---|---|---|
| HVAC | Mechanical Equipment Schedule | List AHUs, FCUs, VAV boxes with mark, level, system, flow |
| HVAC | Duct Schedule | Total duct length by size and system — quantity takeoff |
| Piping | Pipe Schedule | Total pipe length by size and material — procurement |
| Piping | Mechanical Equipment Schedule | Pumps, heat exchangers with capacity, flow, pressure |
| Electrical | Electrical Equipment Schedule | Panels, transformers with voltage, phase, load |
| Electrical | Cable Tray Schedule | Tray length by width and type |
| Plumbing | Plumbing Fixture Schedule | Fixtures with mark, type, water demand |
| Plumbing | Pipe Schedule | Domestic water and drainage pipe by size and material |
| Fire | Mechanical Equipment Schedule | Fire pumps, sprinkler heads — count and location |
| Fire | Pipe Schedule | Sprinkler main and branch pipe by size |
| All | Duct / Pipe Fitting Schedule | Fitting count by type — procurement and quantity check |

---

## Key Parameters by MEP Discipline

**HVAC**
- Mark (unique equipment ID), Family/Type, Level, System Classification, System Name, Design Flow Rate, Air Volume (CFM/L/s), Filter Type

**Piping (Mechanical)**
- Mark, Family/Type, Level, System Name, Pipe Size (DN/NPS), Material, Design Flow Rate, Operating Pressure, Insulation Specification

**Electrical**
- Mark, Family/Type, Level, Voltage, Phase, Load Classification, Circuit Number, Panel Name, Load (kW/VA)

**Plumbing**
- Mark, Family/Type, Level, System Type (Domestic Cold, Domestic Hot, Sanitary), Pipe Size, Slope (for drainage), Material

**Fire Protection**
- Mark, Family/Type, Level, System Name (Wet/Dry), Pipe Size, Sprinkler Head Type, K-Factor, Coverage Area

---

## COBie Required Fields

COBie (Construction Operations Building Information Exchange) is the standard data format for BIM-to-FM handover.

| COBie Sheet | Key Required Fields |
|---|---|
| Facility | Name, Description, ProjectName, SiteName, LinearUnits, AreaUnits |
| Floor | Name, Description, Elevation, Height |
| Space | Name, Description, FloorName, Area |
| Component | Name, Description, CreatedBy, TypeName, SpaceName |
| Type | Name, Description, Category, Manufacturer, ModelNumber, WarrantyDuration |
| Attribute | Name, Category, Value, Unit, CreatedBy |

---

## Data Export Checklist — FM Handover

- [ ] All equipment has unique Mark values — no blanks or duplicates
- [ ] Manufacturer and Model Number fields populated for all COBie-required equipment
- [ ] System names follow the project BEP convention — no "Default" systems
- [ ] Floor and space data linked to equipment in the schedule
- [ ] IFC export completed and validated — check in Solibri or BIM Collab
- [ ] COBie spreadsheet exported and reviewed for blank required fields
- [ ] Warranty and maintenance data fields populated per FM requirements
- [ ] Schedule CSV exported and cross-referenced against design specification quantities
- [ ] File version and issue date recorded in the export log

---
*LUA BIM LABS | Practical BIM Education for MEP*
*Educational reference only — not project specification or code compliance guidance.*
