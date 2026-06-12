# Universal Coordinate Engine
A Shared Coordinate System Generator that outputs values for:

  

- Revit  
    

- Project Base Point (PBP)
- Survey Point (SP)
- True North rotation
- Levels

-   
    
- AutoCAD / Plant3D / CADWorx  
    

- World coordinates
- UCS origin
- UCS rotation

-   
    
- Civil alignment with Northing / Easting

  

  

If done correctly, this eliminates 95% of coordination problems caused by bad coordinates.

  

Below is a complete architecture + math model + tool design so you can build it as a Python tool in a pyRevit toolbar.

  

  

  

  

BIM Universal Coordinate Setup Tool

  

  

  

Goal

  

  

Input a small set of survey control values and automatically compute coordinates for:

|   |   |
|---|---|
|Platform|Outputs|
|Revit|Survey Point, Project Base Point, Levels|
|AutoCAD|X,Y,Z coordinates|
|Plant3D|Model origin|
|CADWorx|Plant origin|
|Civil3D|Alignment reference|
|All|True North / UCS rotation|

  

  

  

  

Required Inputs

  

  

The tool should only ask for five inputs.

First Floor Elevation

Project North Rotation

Northing

Easting

Known Grid Intersection Coordinates

Example input:

First Floor Elevation = 100'-0"

Northing = 2,134,556.20

Easting = 748,221.40

Project North Rotation = 12.5°

  

Grid Intersection = A / 1

Grid Intersection X,Y in model = 0,0

  

  

  

  

Coordinate Systems

  

  

Your tool will calculate three coordinate systems.

  

  

1. Survey Coordinate System

  

  

Real-world coordinates.

Northing

Easting

Elevation

Example:

N = 2,134,556.20

E = 748,221.40

Z = 100'

  

  

  

  

2. Revit Internal Coordinates

  

  

Revit stores coordinates as:

X

Y

Z

But they are offset from Survey Point.

  

  

  

  

3. CAD World Coordinates

  

  

CAD uses:

X → Easting

Y → Northing

Z → Elevation

  

  

  

  

Key Conversion

  

  

The most important conversion:

CAD X = Easting

CAD Y = Northing

Revit X = Easting Offset

Revit Y = Northing Offset

  

  

  

  

Rotation Calculation

  

  

Project North vs True North must be converted.

  

Formula:

RotationRadians = Degrees × π / 180

Example:

12.5° × π / 180

= 0.218 radians

  

  

  

  

Grid Intersection Offset

  

  

Example:

Grid A1 coordinates = (0,0)

Survey coordinates = (748221.4 , 2134556.2)

Offset:

X offset = 748221.4

Y offset = 2134556.2

  

  

  

  

Revit Setup Logic

  

  

The tool should perform these steps automatically.

  

  

Step 1

  

  

Place Survey Point:

Survey Point X = Easting

Survey Point Y = Northing

Survey Point Z = First Floor Elevation

  

  

  

  

Step 2

  

  

Set Project Base Point

  

Typically:

PBP = 0,0,0

or optionally:

PBP = grid intersection

  

  

  

  

Step 3

  

  

Rotate True North

  

Set:

True North Rotation = Project North Rotation

  

  

  

  

Step 4

  

  

Create Levels

  

Example auto-generation:

|   |   |
|---|---|
|Level|Elevation|
|Level 1|100’|
|Level 2|114’|
|Level 3|128’|
|Roof|150’|

  

  

  

  

CAD / Plant3D Coordinate Output

  

  

The tool should generate coordinates like:

Model Origin

X = 748221.40

Y = 2134556.20

Z = 100

  

  

  

  

UCS Definition

  

  

Your tool should also calculate UCS.

  

Example output:

UCS Origin = Grid A1

UCS X Axis = Project East

UCS Y Axis = Project North

Rotation = 12.5°

AutoCAD command equivalent:

UCS

Origin

748221.4,2134556.2,100

Rotate

12.5

  

  

  

  

Python Calculation Engine

  

  

This script performs the coordinate math.

import math

  

northing = 2134556.2

easting = 748221.4

elevation = 100

rotation_deg = 12.5

  

rotation_rad = math.radians(rotation_deg)

  

rev_x = easting

rev_y = northing

rev_z = elevation

  

cad_x = easting

cad_y = northing

cad_z = elevation

  

print("Revit Survey Point")

print(rev_x, rev_y, rev_z)

  

print("CAD Coordinates")

print(cad_x, cad_y, cad_z)

  

print("Rotation (radians)")

print(rotation_rad)

  

  

  

  

Tool Output Report

  

  

Your tool should automatically generate a Coordinate Setup Sheet.

  

Example:

PROJECT COORDINATE REPORT

  

Survey Point

Northing: 2,134,556.20

Easting: 748,221.40

Elevation: 100'-0"

  

Project Base Point

X: 0

Y: 0

Z: 0

  

True North Rotation

12.5°

  

UCS Definition

Origin: Grid A1

Rotation: 12.5°

  

CAD Origin

X: 748221.40

Y: 2134556.20

Z: 100

This becomes project documentation.

  

  

  

  

pyRevit Toolbar Tool

  

  

You should package this as a pyRevit button.

  

Folder structure:

BIMTools.extension

   BIM.tab

      Coordination.panel

         CoordinateSetup.pushbutton

             script.py

             icon.png

This is exactly how custom tools are organized in pyRevit extensions. 

  

  

  

  

Future Version (Extremely Powerful)

  

  

Your tool can later add:

  

  

Automatic model alignment

  

  

For linked models:

Align to Shared Coordinates

  

  

  

  

Multi-software export

  

  

Generate:

Revit Setup

AutoCAD Script (.scr)

Civil3D Setup

Plant3D Setup

  

  

  

  

Automatic coordinate checker

  

  

Detect if models are:

500 miles away

rotated incorrectly

elevation mismatched

  

  

  

  

This Tool Would Be Very Valuable

  

  

A tool like this can:

  

- eliminate shared coordinate errors
- standardize project setup
- save hours per project
- prevent catastrophic model misalignment

  

  

Large VDC teams build tools like this internally.

  

  

  

If you’d like, I can also help you design the next-level version of this tool that most companies do not have:

  

  

The Universal BIM Coordinate Engine

  

  

It automatically:

  

- reads coordinates from Civil3D
- aligns Revit models
- generates CAD UCS scripts
- validates coordinates across all disciplines


  

Below are the major components you should add.

  

  

  

  

1. Large Coordinate Protection (Critical for Revit)

  

  

One of the biggest problems with survey coordinates is floating point precision errors in Revit when coordinates are very large.

  

Typical survey coordinates:

Easting: 748221.40

Northing: 2134556.20

Revit geometry becomes unstable beyond roughly:

20 miles from origin

≈ 105,600 ft

Your tool should automatically calculate:

Distance from internal origin

Then warn the user if the building is too far away.

  

  

Add this feature

  

  

The tool should automatically recommend a coordinate shift:

Survey = real world

Revit = local working coordinates

Example output:

Recommended Revit Origin Shift

X = -748000

Y = -2134000

This keeps geometry close to the origin while preserving survey coordinates.

  

  

  

  

2. Unit Conversion Engine

  

  

Your system must support all major BIM units.

  

Inputs may arrive as:

US survey feet

International feet

meters

millimeters

Many surveyors still use US Survey Foot, which differs from International Foot.

  

Conversion difference:

1 US survey foot = 1200/3937 m

1 international foot = 0.3048 m

Your tool should include:

Survey Foot → Revit Foot conversion

Meters → Feet conversion

  

  

  

  

3. Grid Intersection Solver

  

  

Right now you allow a grid intersection input.

  

But you should also allow two grid intersections.

  

Why this matters:

  

Two points define project orientation.

  

Example:

Grid A1 = known coordinate

Grid B1 = known coordinate

From this the tool can calculate:

True project rotation

Formula:

rotation = atan2(ΔEasting , ΔNorthing)

This removes human error in rotation entry.

  

  

  

  

4. Model Alignment Validator

  

  

After setup, the tool should scan the model and verify:

Are linked models aligned?

Are coordinates consistent?

Is project north correct?

Checks include:

Revit internal origin

Survey point

PBP position

True north rotation

Output:

COORDINATE VALIDATION

  

Revit Model: OK

Linked Structural Model: ROTATION MISMATCH

Civil Model: OFFSET ERROR

This becomes extremely valuable in large projects.

  

  

  

  

5. CAD Export Script Generator

  

  

Instead of just showing CAD coordinates, your tool should generate AutoCAD scripts.

  

Output file:

setup_ucs.scr

Example contents:

UCS

W

UCS

Origin

748221.4,2134556.2,100

UCS

Z

12.5

PLAN

C

Users simply run:

SCRIPT

setup_ucs.scr

This automatically sets coordinates in:

  

- AutoCAD
- Plant3D
- CADWorx

  

  

  

  

  

6. Civil 3D Integration

  

  

Civil files typically define:

State Plane Coordinate System

Your tool should store:

Coordinate system name

Datum

Zone

Example:

NAD83 Indiana West

EPSG:2965

This becomes part of the project coordinate report.

  

  

  

  

7. BIM Execution Plan Generator

  

  

Your tool should automatically generate the project coordinate specification.

  

Example output:

PROJECT COORDINATE STANDARD

  

Survey Datum: NAD83

Units: US Survey Feet

  

Revit Setup

Survey Point = 748221.40 , 2134556.20 , 100

  

AutoCAD Setup

UCS Origin = 748221.40 , 2134556.20 , 100

  

Rotation

True North = 12.5°

This becomes the coordination standard document.

  

  

  

  

8. Linked Model Coordinate Push

  

  

The tool should optionally push coordinates into linked models.

  

For example:

Mechanical model

Structural model

Electrical model

Function:

Publish Shared Coordinates

This ensures all teams share the same coordinate system.

  

  

  

  

9. Grid Coordinate Calculator

  

  

Another extremely useful feature:

  

Select any grid intersection and the tool reports:

Northing

Easting

Elevation

This helps during field coordination.

  

Example output:

Grid C4

  

Easting: 748350.12

Northing: 2134677.90

Elevation: 100'

  

  

  

  

10. Model Origin Diagnostic

  

  

Many BIM models already contain bad coordinate setups.

  

Your tool should detect:

Survey point clipped/unclipped

PBP moved incorrectly

model 10 miles from origin

rotation mismatches

Output example:

COORDINATE DIAGNOSTIC

  

Survey Point: Unclipped

PBP Offset: 120000 ft

Rotation Error: 1.5°

  

  

  

  

11. Multi-Software Output Package

  

  

Your tool should produce a coordination package:

/Coordinates

  

Revit_setup.txt

Autocad_ucs.scr

Plant3D_origin.txt

Civil3D_reference.txt

Coordinate_Report.pdf

This becomes the official coordinate setup package for the project.

  

  

  

  

12. Visualization Tool (Very Helpful)

  

  

Your tool could also generate a coordinate diagram.

  

Example:

Internal Origin

Project Base Point

Survey Point

Grid A1

True North

Project North

This helps coordinators visually understand the setup.

  

  

  

  

The Final Tool Architecture

  

  

Your tool would consist of five engines.

Input Engine

Coordinate Math Engine

Software Output Engine

Validation Engine

Documentation Engine

  

  

  

  

If you build all of this…

  

  

You will essentially have created a Universal BIM Coordinate System Engine.

  

Very few companies have something like this internally.

  

It would solve problems across:

  

- Revit
- AutoCAD
- Plant3D
- CADWorx
- Civil3D
- ACC coordination

  

  

  

  

If you’d like, I can also help you design something extremely valuable for this tool:

  

A full mathematical model for coordinate transformations used in survey engineering (translation + rotation matrices).

  

That is the core math behind professional survey software, and implementing it will make your tool extremely accurate.
