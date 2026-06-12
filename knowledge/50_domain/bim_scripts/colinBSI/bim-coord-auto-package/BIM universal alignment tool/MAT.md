# MAT
Model Alignment Tool
design the Model Alignment Tool so a coordinator can press one button and immediately know:

  

- If linked models are misaligned
- How much they are offset
- How much they are rotated
- Optionally auto-correct the alignment

  

  

This is one of the highest value BIM automation tools for coordination.

  

  

  

  

Model Alignment Tool

  

  

  

Purpose

  

  

Detect and correct misalignment between:

  

- Architectural model
- Structural model
- MEP models
- Plant3D / CAD imports

  

  

The tool analyzes:

Origin

Rotation

Elevation

Shared Coordinates

  

  

  

  

What the Tool Detects

  

  

The tool compares the host model against all links.

  

It checks:

|   |   |
|---|---|
|Check|Description|
|Origin Offset|Distance between model origins|
|Rotation Difference|True north mismatch|
|Elevation Difference|Level offset|
|Shared Coordinate Status|Published vs not published|

Example output:

STRUCTURAL MODEL

  

Offset X: 2.3 ft

Offset Y: -1.2 ft

Rotation Error: 0.35°

Elevation Offset: 0.00 ft

  

  

  

  

Alignment Strategy

  

  

The tool uses three coordinate references.

Internal Origin

Project Base Point

Survey Point

Preferred workflow:

Architectural Model = master

All others align to it

  

  

  

  

Alignment Math

  

  

To detect alignment differences, compare transforms:

Host Transform

Link Transform

Compute:

Translation difference

Rotation difference

  

  

  

  

Alignment Calculation

  

  

Translation difference:

ΔX = link.X − host.X

ΔY = link.Y − host.Y

ΔZ = link.Z − host.Z

Rotation difference:

Δθ = link_rotation − host_rotation

Distance from origin:

distance = √(ΔX² + ΔY²)

  

  

  

  

pyRevit Alignment Tool

  

  

Below is the core script.

  

This scans all linked models and reports alignment differences.

from pyrevit import revit, DB

import math

  

doc = revit.doc

  

links = DB.FilteredElementCollector(doc)\

    .OfClass(DB.RevitLinkInstance)\

    .ToElements()

  

host_transform = DB.Transform.Identity

  

print("MODEL ALIGNMENT REPORT\n")

  

for link in links:

  

    transform = link.GetTransform()

  

    x = transform.Origin.X

    y = transform.Origin.Y

    z = transform.Origin.Z

  

    rotation = math.degrees(math.atan2(

        transform.BasisX.Y,

        transform.BasisX.X

    ))

  

    print("Link Model:", link.Name)

    print("Offset X:", round(x,3))

    print("Offset Y:", round(y,3))

    print("Offset Z:", round(z,3))

    print("Rotation:", round(rotation,4))

    print("-----------------------")

Output example:

MODEL ALIGNMENT REPORT

  

Structural_Model.rvt

Offset X: 2.301

Offset Y: -1.200

Offset Z: 0.000

Rotation: 0.35°

  

Mechanical_Model.rvt

Offset X: 0.005

Offset Y: 0.002

Offset Z: 0.000

Rotation: 0.00°

  

  

  

  

Alignment Thresholds

  

  

Your tool should define tolerances.

Translation tolerance = 0.05 ft

Rotation tolerance = 0.05°

Elevation tolerance = 0.02 ft

If exceeded:

FLAG MISALIGNED

  

  

  

  

Visual Warning

  

  

The tool should display:

✓ Aligned

⚠ Minor offset

✗ Major misalignment

  

  

  

  

Auto-Align Feature

  

  

If enabled, the tool will:

Move link to shared coordinates

Rotate link to project north

Example code:

with revit.Transaction("Align Link"):

  

    new_transform = DB.Transform.CreateTranslation(

        DB.XYZ(-x,-y,-z)

    )

  

    link.SetTransform(new_transform)

  

  

  

  

Coordinate Comparison

  

  

The tool should also compare:

Survey point location

Project base point location

True north rotation

This catches incorrect coordinate setups.

  

  

  

  

Advanced Alignment Mode

  

  

A powerful feature is grid alignment.

  

Instead of origin alignment, the tool can align models using:

Grid intersection

Level elevation

Example workflow:

Select Grid A1 in host

Select Grid A1 in link

Tool computes offset

Moves model automatically

  

  

  

  

Alignment Report

  

  

The tool should generate a report:

MODEL ALIGNMENT REPORT

  

Host Model: Architectural

  

Structural Model

Offset: 2.3 ft

Rotation: 0.35°

Status: MISALIGNED

  

Mechanical Model

Offset: 0.01 ft

Rotation: 0.00°

Status: OK

Saved as:

/BIMReports/model_alignment_report.txt

  

  

  

  

Next-Level Version

  

  

Later versions can include:

  

  

Clash-to-grid reporting

  

  

Convert clash coordinates to:

Grid location

Level

Example:

Clash #452

  

Grid: C5

Level: 3

  

  

  

  

Visual alignment viewer

  

  

The tool displays:

Origin

Survey point

Project base point

Link origin

in a coordination view.

  

  

  

  

Recommended Toolbar Layout

  

  

Your coordinate toolkit could look like this:

BIM Coordinates

  

Coordinate Setup

Model Alignment

Coordinate Validator

Grid Coordinate Finder

Export CAD UCS

These five tools together become a complete BIM coordinate management system.

  

  

  

If you’d like, the next tool I strongly recommend building is:

  

Grid Coordinate Finder

  

It lets a coordinator click any point in the model and instantly see:

Grid location

Northing

Easting

Elevation

That tool becomes incredibly useful for clash reports, field layout, and coordination meetings.