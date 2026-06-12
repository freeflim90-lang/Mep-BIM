This includes **clash tolerances, model limits, clearances, and performance benchmarks** typically used by high-performing BIM teams.

The structure remains the same but with **imperial measurements, US industry practices, and construction tolerances.**

---

# Advanced BIM Coordination

## Master-Level Training for Elite BIM Teams (Imperial Standards)

Target audience:

- Senior BIM Coordinators
- BIM Specialists
- Digital Delivery Leads
- BIM leads

Software stack:

- Autodesk Construction Cloud (ACC)
    
- Revit
    
- Navisworks Manage
    
- Civil 3D
    
- Plant 3D
    
- CADWorx Plant
    
- AutoCAD
    

---

# Course Structure

|Module|Topic|
|---|---|
|1|Advanced Model Troubleshooting|
|2|Coordinate System Mastery|
|3|Federated Model Strategy|
|4|Advanced Clash Detection|
|5|False Clash Elimination|
|6|Model Performance Optimization|
|7|Mega-Project Coordination|
|8|Cross-Platform Coordination|
|9|BIM Automation|
|10|BIM Data Intelligence|

---

# Module 1 — Advanced Model Troubleshooting

Most coordination failures are **model issues disguised as clash problems.**

Elite BIM teams identify and correct model problems **before running clash detection.**

---

## Critical Model Failure Types

### Model Origin Errors

Symptoms:

```
Models appear miles apart
Elements extremely far from origin
Navisworks camera navigation becomes unstable
```

Typical cause:

```
Civil model coordinates not followed
Incorrect survey point placement
Model drawn thousands of feet from origin
```

Diagnosis workflow:

```
Check Survey Point coordinates
Check Project Base Point
Verify Internal Origin
Verify Shared Coordinates
```

Acceptable coordinate distance:

```
Geometry should be within approximately 10 miles of internal origin
Best practice is within 1 mile
```

---

### Linked Model Drift

Symptoms:

```
Links slightly offset
Links move after reload
Grids misalign by several inches
```

Typical causes:

```
Multiple coordinate systems used
Incorrect Acquire/Publish workflow
Manual movement of linked models
```

Solution workflow:

```
Reload links using Shared Coordinates
Acquire coordinates from civil or architectural model
Publish coordinates back to discipline models
```

---

### Corrupt Revit Links

Symptoms:

```
Models slow dramatically
Reloading links takes several minutes
Frequent crashes during synchronization
```

Troubleshooting process:

```
Audit model on open
Detach from central
Reload links individually
Replace corrupted links
```

---

# Module 2 — Coordinate System Mastery

Coordinate mistakes are the **most expensive BIM coordination errors.**

---

## Revit Coordinate References

Revit includes four coordinate systems:

```
Internal Origin
Project Base Point
Survey Point
Shared Coordinates
```

---

## Professional Coordinate Strategy

Industry best practice:

```
Civil model establishes site coordinates
Architectural model acquires coordinates
All discipline models publish coordinates
```

---

## Coordinate Validation Checklist

Before coordination begins:

```
Verify grid alignment within 1/8"
Verify level elevations
Verify building orientation
Verify project north vs true north
Verify survey coordinate values
```

---

# Module 3 — Federated Model Strategy

Large projects require structured **federation management.**

---

## Federation Structure

Recommended discipline order:

```
Civil
Site Utilities
Architecture
Structure
Mechanical
Electrical
Plumbing
Process
Equipment
Temporary Works
```

---

## Federation File Types

|File|Purpose|
|---|---|
|NWC|Cached export for Navisworks|
|NWF|Coordination working file|
|NWD|Published coordination model|

---

## Federation Best Practice

Never clash directly against live Revit files.

Use the structure:

```
Revit Models → NWC Exports → NWF Coordination File → Published NWD
```

---

# Module 4 — Advanced Clash Detection

Professional BIM teams focus on **high-value clash detection.**

---

## Clash Rule Example

```
Test Name: STRUCTURE_vs_MEP
```

Selection A:

```
Structural Columns
Structural Framing
Structural Floors
Structural Walls
```

Selection B:

```
Ducts
Pipes
Cable Trays
Conduits
```

Tolerance:

```
0 inches
```

---

## Clearance Clash Example

```
Test Name: EQUIPMENT_CLEARANCE
```

Selection A:

```
Mechanical Equipment
Electrical Equipment
```

Selection B:

```
Structure
Ductwork
Piping
```

Clearance requirement:

```
2 ft – 3 ft typical maintenance clearance
```

---

# Module 5 — False Clash Elimination

Poor teams review **10,000 clashes.**

Elite teams reduce this to **200 meaningful clashes.**

---

## Major False Clash Sources

### Duct Insulation

Insulation often causes thousands of clashes.

Solution:

```
Ignore insulation layer
Clash using duct center geometry
```

---

### Pipe Fittings

Small fittings create large volumes of low-value clashes.

Solution:

```
Ignore pipe fittings smaller than 2 inches
```

---

### Hangers and Supports

Supports may intentionally intersect structural elements.

Solution:

```
Exclude hanger families from clash tests
```

---

# Module 6 — Model Performance Optimization

Large models reduce coordination efficiency.

---

## Revit Performance Targets

|Metric|Target|
|---|---|
|Model size|< 500 MB|
|Warnings|< 1,000|
|Views|< 1,500|
|Links|< 15|
|CAD imports|0 preferred|

---

## Model Cleanup Techniques

```
Purge unused families
Remove imported CAD files
Delete redundant views
Consolidate worksets
Replace groups with assemblies
```

---

# Module 7 — Mega-Project Coordination

Large projects require structured coordination teams.

---

## Coordination Structure

```
Discipline BIM Coordinators
Zone Coordinators
Lead BIM Coordinator
Digital Delivery Manager
```

---

## Zone-Based Coordination

Divide the project into areas:

```
Building A
Building B
Podium
Central Plant
Parking Structure
Site Utilities
```

Each zone runs its own clash detection cycle.

---

# Module 8 — Cross-Platform Coordination

Projects using **Plant 3D, CADWorx, Civil 3D, and Revit** require strict export workflows.

---

## Standard Coordination Exports

|Platform|Export Format|
|---|---|
|Revit|NWC|
|Plant 3D|NWC|
|Civil 3D|NWC|
|CADWorx|NWC or IFC|
|AutoCAD|NWC|
|ReCap (LiDAR Point Cloud)|RCP / RCS (visual reference overlay)|
|Revit Scan Mesh|RCMR (visual reference overlay)|

> **Point Cloud Coordination Note:** LiDAR point cloud scans (RCP/RCS) and Revit Scan Meshes (RCMR) are used as visual reference overlays only — not for formal clash detection. Link RCP files into Revit on the **Scan workset**. Append into Navisworks for visual reference. AutoCAD and CADWorx users may reference RCP files directly.

---

## Export Guidelines

Before exporting:

```
Freeze unnecessary layers
Remove construction lines
Clean unused blocks
Verify model units (feet/inches)
```

---

# Module 9 — BIM Automation

Elite BIM teams automate repetitive coordination tasks.

---

## Automation Opportunities

Examples:

```
Automated model health reports
Automatic clash grouping
Automated naming validation
Automatic issue creation
```

---

## Automation Tools

```
Dynamo
pyRevit
Python scripts
Revit API
PowerShell scripts
```

Automating coordination tasks through scripting and API tools allows teams to eliminate repetitive tasks and build custom workflows for their organization.

---

# Module 10 — BIM Data Intelligence

Advanced BIM teams use model data for **construction intelligence.**

---

## Data Extraction Examples

```
Clash trend analysis
Coordination progress metrics
Model maturity tracking
Discipline performance metrics
```

---

## Reporting Tools

```
Power BI dashboards
ACC analytics
Excel coordination reports
Navisworks clash reports
```

---

# Capstone Exercise — Advanced Coordination Scenario

Participants coordinate a complex project using:

```
Civil model
Architectural model
Structural model
MEP models
Process piping model
Equipment model
```

---

## Tasks

```
Validate model coordinates
Build federated model
Create advanced clash tests
Eliminate false clashes
Generate clash reports
Run coordination meeting
Publish coordination dashboard
```

---

# Final Outcome

After completing this course, your team should be capable of:

```
Managing mega-project coordination
Diagnosing complex model failures
Running high-efficiency clash detection
Building automated BIM workflows
Producing data-driven coordination reports
```

---

If you'd like, I can also build the **three most powerful upgrades that truly create elite BIM teams**:

1. **The Elite BIM Coordinator Playbook (80–100 pages)** used by top US contractors.
    
2. **A complete Navisworks clash rule library used on billion-dollar projects.**
    
3. **A BIM troubleshooting decision tree that lets coordinators solve 95% of model issues in minutes.**
    

Those three resources are what typically separate **average BIM teams from the top BIM teams in the US.**
