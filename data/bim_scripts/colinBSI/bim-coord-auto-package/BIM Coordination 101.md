Below is a **professional BIM Coordinator 101 training package** expanded into:

- A **structured training manual outline**
- A **5-day intensive course schedule**
    
- A **clash matrix template**
    
- A **BIM coordinator project checklist**
    
- A **Navisworks clash rule template**
    

---

# BIM Coordinator 101

## Complete Training Package

Designed for teams using:

- Autodesk Construction Cloud (ACC)
    
- Revit
    
- Navisworks Manage
    
- AutoCAD
    
- Civil 3D
    
- Plant 3D
    
- CADWorx Plant
    

---

# 1. BIM Coordinator Training Manual Structure

## Chapter 1 — BIM Coordination Fundamentals

### Role of a BIM Coordinator

A BIM Coordinator manages **model integration, coordination, and issue tracking across disciplines.**

Primary responsibilities:

- Collect discipline models
    
- Validate models
    
- Combine models
    
- Run clash detection
    
- Track coordination issues
    
- Lead coordination meetings
    
- Maintain BIM standards
    

### BIM Roles Comparison

|Role|Responsibility|
|---|---|
|BIM Manager|Strategy, standards, execution plans|
|BIM Coordinator|Model coordination and clash detection|
|BIM Modeler|Model creation|
|Discipline Lead|Engineering decisions|

---

# Chapter 2 — BIM Execution Plan (BEP)

The BIM Execution Plan defines **how BIM will be implemented on a project.**

Typical BEP sections:

```
Project Overview
Software Platforms
Model Naming Standards
Model Responsibilities
Level of Development
Model Exchange Schedule
Clash Detection Process
Issue Tracking Process
```

### Example Model Naming Standard

```
<Project>-<Discipline>-<Zone>-<Type>-<Version>

Example:
ABC-HOSP-MECH-Z1-MOD-V03
```

---

# Chapter 3 — Model Coordination Workflow

## Weekly Coordination Cycle

```
1 Model upload deadline
2 Model validation
3 Federated model creation
4 Clash detection
5 Issue assignment
6 Coordination meeting
7 Issue resolution
```

### Typical Coordination Timeline

|Day|Task|
|---|---|
|Monday|Model uploads (deadline for all disciplines)|
|Tuesday|Clash tests run in Navisworks|
|Wednesday|Automation scripts process clashes; clash groups generated|
|Thursday|ACC issues created automatically from clash groups|
|Friday|Coordination meeting using dashboards and heat maps|

---

# Chapter 4 — Autodesk Construction Cloud (ACC)

### Core ACC Modules

|Module|Use|
|---|---|
|Docs|File storage|
|Design Collaboration|Package sharing|
|Model Coordination|Clash detection|
|Issues|Issue tracking|

---

## Recommended ACC Folder Structure

```
Project Files

01_WIP
02_SHARED
03_PUBLISHED
04_ARCHIVE
```

### Rules

- WIP models are **never used for coordination**
    
- Coordination uses **Shared or Published models**
    

---

# Chapter 5 — Revit Model Coordination

### Key Coordination Concepts

#### Shared Coordinates

Required to align models.

Workflow:

```
Link models
Acquire coordinates
Publish coordinates
```

#### Revit Model Health

Key metrics:

|Metric|Target|
|---|---|
|Warnings|< 500|
|File size|< 500MB|
|Links|< 10|
|Groups|Minimal|

---

# Chapter 6 — Multi-Platform Coordination

Projects using **Plant 3D, Civil 3D, CADWorx, and AutoCAD** require export workflows.

### Typical Coordination File Types

|Software|Coordination Export|
|---|---|
|Revit|NWC|
|Plant 3D|NWC|
|Civil 3D|NWC|
|AutoCAD|NWC|
|CADWorx|NWC or IFC|
|ReCap (LiDAR Point Cloud)|RCP / RCS (visual reference overlay)|
|Revit Scan Mesh|RCMR (visual reference overlay)|

> **Point Cloud Coordination Note:** LiDAR point cloud scans (RCP/RCS) and Revit Scan Meshes (RCMR) are used as visual reference overlays only — they are not used for formal clash detection. Link RCP files into Revit on the **Scan workset**. Append RCP files into Navisworks for visual reference during coordination reviews. AutoCAD and CADWorx users may reference RCP files directly in their authoring environment.

---

# Chapter 7 — Navisworks Manage

## Federated Model Creation

Append models in this order:

```
Civil
Architecture
Structure
Mechanical
Electrical
Plumbing
Process
```

Save as:

```
<Project>_FEDERATION.nwd
```

---

# Chapter 8 — Clash Detection

### Clash Detection Types

|Type|Description|
|---|---|
|Hard Clash|Physical intersection|
|Clearance Clash|Required spacing violated|
|Workflow Clash|Construction sequence conflict|

---

# 2. 5-Day Intensive Training Program

# Day 1 — BIM Fundamentals

## Topics

- BIM roles
    
- Model coordination workflow
    
- BIM execution plans
    
- Model naming conventions
    
- File structures
    

## Exercise

Students review a sample **BEP** and identify:

- model responsibilities
    
- coordination schedule
    
- clash rules
    

---

# Day 2 — ACC Project Setup

## Topics

- ACC Docs
    
- Design Collaboration
    
- Model Coordination
    
- Issue workflows
    

## Exercise

Students:

```
Create project folder structure
Upload discipline models
Review version history
```

---

# Day 3 — Revit Model Validation

## Topics

- Shared coordinates
    
- Model linking
    
- Model health checks
    
- Workset management
    

## Exercise

Students audit a Revit model and report:

```
Warnings
File size
Unused views
Unused families
```

---

# Day 4 — Navisworks Clash Detection

## Topics

- Federated model creation
    
- Clash detection rules
    
- Clash grouping
    
- Clash reporting
    

## Exercise

Students:

```
Append discipline models
Create clash tests
Run clashes
Group clashes
Create reports
```

---

# Day 5 — Issue Tracking and Coordination

## Topics

- ACC Issues
    
- Clash assignment
    
- Coordination meetings
    
- Reporting
    

## Exercise

Students run a **mock coordination meeting.**

---

# 3. Clash Matrix Template

This defines **which disciplines clash against which.**

```
DISCIPLINE CLASH MATRIX
```

|Discipline|Clash Against|
|---|---|
|Structure|Mechanical|
|Structure|Plumbing|
|Structure|Electrical|
|Structure|Process|
|Mechanical|Structure|
|Mechanical|Electrical|
|Mechanical|Plumbing|
|Plumbing|Structure|
|Plumbing|Electrical|
|Electrical|Structure|
|Electrical|Mechanical|
|Civil|Structure|
|Civil|Mechanical|
|Process|Structure|

---

# 4. BIM Coordinator Daily Checklist

## Model Management

```
Verify models uploaded
Check file versions
Confirm naming standards
Confirm shared coordinates
```

---

## Model QA

```
Check Revit warnings
Check file sizes
Verify links
Verify levels and grids
```

---

## Clash Detection

```
Update federated model
Run clash tests
Review clash groups
Assign issues
```

---

## Issue Tracking

```
Review open issues
Assign responsibility
Update issue status
Prepare meeting notes
```

---

# 5. Navisworks Clash Rule Template

## Structure vs MEP

```
Test Name: STR_vs_MEP

Selection A:
Structure

Selection B:
Mechanical
Electrical
Plumbing

Tolerance: 0 mm
```

---

## Structure vs Process

```
Test Name: STR_vs_PROCESS

Selection A:
Structure

Selection B:
Process Piping

Tolerance: 0 mm
```

---

## MEP Internal Clash

```
Test Name: MEP_Internal

Selection A:
Mechanical

Selection B:
Electrical
Plumbing

Tolerance: 25 mm
```

---

# 6. Coordination Meeting Template

## Weekly Coordination Meeting

```
Project:
Date:
Coordinator:
Attendees:
```

### Agenda

```
1 Model updates
2 Major clashes
3 Open issues
4 Design changes
5 Next deadlines
```

---

### Action Items

|Issue|Discipline|Due Date|
|---|---|---|
|Pipe clash at Grid C5|Mechanical|May 12|
|Cable tray conflict|Electrical|May 14|

---

# 7. BIM Coordinator Skills Roadmap

## Core Skills

```
Revit
Navisworks Manage
ACC
Clash detection
Model QA
Communication
```

---

## Advanced Skills

```
Dynamo automation
Revit API
Python
PowerBI dashboards
Model health automation
```

The BIM Pure training material also strongly encourages automation through **Python and the Revit API** to eliminate repetitive BIM tasks and build custom tools for teams.

---

# 8. Capstone Coordination Exercise

Students complete a full coordination workflow.

## Inputs

```
Architecture model
Structure model
Mechanical model
Electrical model
Process model
Civil model
```

---

## Tasks

```
1 Upload models to ACC
2 Create federated model
3 Run clash detection
4 Create clash groups
5 Assign issues
6 Conduct coordination meeting
7 Publish coordination report
```

---

# If you want, I can also produce

1. A **50-page BIM Coordinator Handbook**
    
2. A **full Navisworks clash rule library (used on mega projects)**
    
3. A **Revit model QA checklist used by large BIM teams**
    
4. An **ACC coordination workflow standard**
    
5. A **BIM coordinator onboarding playbook for new hires**
    