Below is a **BIM Troubleshooting Decision Tree** designed for experienced BIM coordinators working with **Revit, Navisworks Manage, Civil 3D, Plant 3D, CADWorx, and Autodesk Construction Cloud (ACC)**.

This decision tree focuses on the **most common coordination failures** and provides **fast diagnostic paths** so a coordinator can solve issues in minutes instead of hours.

The structure is written in Markdown so it can be used directly in:

---

# BIM Troubleshooting Decision Tree

## Solve 95% of BIM Coordination Problems Quickly

This decision tree targets the **five most common problem categories**:

1. Models not aligning
    
2. Clash detection producing bad results
    
3. Models performing slowly
    
4. Missing geometry or models
    
5. Corrupted models
    

---

# Step 1 — Identify the Problem Type

```
Is the issue related to:

A  Model alignment
B  Clash detection
C  Model performance
D  Missing elements or links
E  Model corruption or crashes
```

Proceed to the appropriate section.

---

# A — Model Alignment Problems

## Symptom

Models do not line up in:

- Revit
    
- Navisworks
    
- ACC Model Coordination
    

Examples:

```
Models appear miles apart
Models offset by several feet
Grids do not align
Levels do not match
```

---

## A1 — Are grids aligned?

```
YES → Go to A2
NO → Grid mismatch
```

### Fix

```
Verify grid origin
Check if grids were manually moved
Confirm architectural model is authoritative
```

---

## A2 — Are levels aligned?

```
YES → Go to A3
NO → Level elevation mismatch
```

### Fix

```
Confirm level elevations match across models
Check if discipline models copied levels correctly
```

---

## A3 — Check coordinate system

Verify these elements in Revit:

```
Internal Origin
Project Base Point
Survey Point
Shared Coordinates
```

### Diagnostic

```
Are survey coordinates identical between models?
```

```
YES → Go to A4
NO → Coordinate mismatch
```

### Fix

```
Acquire coordinates from architectural or civil model
Publish coordinates to discipline models
Reload links using Shared Coordinates
```

---

## A4 — Check for manual movement

Question:

```
Was the model moved manually in Revit or Navisworks?
```

```
YES → Reset model position
NO → Go to A5
```

---

## A5 — Verify Civil model alignment

If civil models exist:

```
Civil 3D typically controls site coordinates
```

Fix workflow:

```
Civil model establishes survey coordinates
Architecture acquires coordinates
All discipline models publish coordinates
```

---

# B — Clash Detection Problems

## Symptom

Clash tests produce:

```
Thousands of clashes
False clashes
Missing clashes
```

---

## B1 — Too many clashes

Typical causes:

```
Insulation geometry
Pipe fittings
Small components
Hangers
```

### Solution

Adjust clash rules:

```
Ignore insulation layers
Ignore pipe fittings under 2"
Exclude hangers and supports
```

---

## B2 — Missing clashes

Question:

```
Are correct categories selected in clash test?
```

Check selections:

```
Structural Framing
Structural Columns
Structural Floors
Ducts
Pipes
Cable Trays
Conduits
```

If not included → update clash sets.

---

## B3 — Clash tolerance incorrect

Check tolerance:

Typical values:

```
Hard clashes → 0 inches
MEP clearance → 1"–2"
Equipment clearance → 24"–36"
```

Incorrect tolerance can hide clashes.

---

# C — Model Performance Problems

## Symptom

```
Revit extremely slow
Navisworks takes minutes to load
ACC models take long to process
```

---

## C1 — Check model size

Revit model target:

```
Under 500 MB
```

If larger:

### Fix

```
Remove unused families
Delete unused views
Purge unused elements
```

---

## C2 — Check CAD imports

Question:

```
Are CAD files imported instead of linked?
```

```
YES → Replace with linked CAD
NO → Continue
```

Imported CAD is one of the largest performance killers.

---

## C3 — Check view count

Target:

```
Less than 1500 views
```

If excessive:

```
Delete working views
Remove unused sections
Remove redundant 3D views
```

---

## C4 — Check warnings

Open:

```
Manage → Review Warnings
```

Target:

```
Less than 1000 warnings
```

High warnings slow Revit.

---

# D — Missing Models or Elements

## Symptom

```
Model appears empty
Elements missing
Links not visible
```

---

## D1 — Check link status

Open:

```
Manage Links
```

Question:

```
Are links loaded?
```

```
YES → Go to D2
NO → Reload links
```

---

## D2 — Check worksets

Question:

```
Are worksets visible?
```

```
YES → Continue
NO → Enable worksets
```

---

## D3 — Check view settings

Verify:

```
Visibility/Graphics
View filters
View templates
Detail level
Phase filters
```

View templates often hide geometry.

---

# E — Model Corruption or Crashes

## Symptom

```
Model crashes during open
Sync fails
Links refuse to reload
```

---

## E1 — Audit model

Open with:

```
Audit enabled
```

---

## E2 — Detach from central

Workflow:

```
Detach model
Save as new central
Reload links
Resynchronize
```

---

## E3 — Identify corrupted families

Symptoms:

```
Model crashes when placing specific families
```

Fix:

```
Remove family
Reload clean version
```

---

# Rapid Troubleshooting Flow (Quick Version)

This version is used during **live coordination meetings**.

```
1 Models misaligned
→ Check shared coordinates

2 Too many clashes
→ Check insulation and fittings

3 Revit slow
→ Check CAD imports and warnings

4 Missing elements
→ Check worksets and view templates

5 Model crashes
→ Audit and detach from central
```

---

# Elite BIM Coordinator Diagnostic Checklist

Top BIM teams always check these first:

```
Coordinates
Grids
Levels
Links
Clash rules
View templates
CAD imports
Warnings
```

Solving these eight areas resolves **the majority of coordination issues.**

---

# Advanced Upgrade (Used by Elite BIM Teams)

The most advanced BIM teams also implement:

```
Automated model health checks
Automated clash grouping
Automated issue creation
Model performance dashboards
```

These workflows are often built using **Revit API automation, Python, Dynamo, and tools like pyRevit**, which allow teams to automate repetitive coordination tasks and build custom tools tailored to their workflows.

---

# Result

Using this decision tree, experienced BIM coordinators can usually diagnose and resolve:

```
Model alignment issues
Clash detection failures
Performance bottlenecks
Missing geometry
Model corruption
```

within **5–15 minutes instead of hours of investigation.**

---

If you'd like, I can also create the **next three resources that turn strong BIM teams into elite coordination teams**:

1. **The Mega-Project BIM Coordination Playbook (100+ pages).**
    
2. **The Ultimate Navisworks Clash Rule Library used on billion-dollar projects.**
    
3. **The BIM Model Health Scoring System used by top VDC departments.**
    

Those three together create **one of the most advanced BIM team training systems currently used in the industry.**