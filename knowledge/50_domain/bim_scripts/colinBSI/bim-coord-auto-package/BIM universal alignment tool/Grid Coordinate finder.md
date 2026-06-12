 build the Grid Coordinate Finder as a pyRevit tool that allows a coordinator to click any point in the model and instantly see:

• Grid intersection or nearest grids

• Level

• Easting

• Northing

• Elevation

• Local model coordinates

  

This becomes extremely useful for:

• Clash reporting

• Field layout coordination

• RFI responses

• Construction issues

• Survey coordination

  

Below is the production-ready design.

  

⸻

  

Grid Coordinate Finder Tool

  

What the Tool Does

  

Workflow:

  

User runs tool

      ↓

User clicks point in model

      ↓

Tool calculates coordinates

      ↓

Nearest grid intersection found

      ↓

Report displayed

  

Example result:

  

POINT COORDINATES

  

Grid Location

Grid C / Grid 5

  

Level

Level 3

  

Survey Coordinates

Easting: 748350.12

Northing: 2134677.90

Elevation: 128'-0"

  

Local Model Coordinates

X: 130.12

Y: 245.44

Z: 28.00

  

  

⸻

  

Required Data from Model

  

The tool reads:

  

Grids

Levels

Survey Point

Project Base Point

True North Rotation

  

  

⸻

  

Core Steps

  

1. Pick Point

  

Use pyRevit point selection.

  

Pick point in model

  

  

⸻

  

2. Convert to Survey Coordinates

  

Revit stores internal coordinates relative to internal origin.

  

We convert to:

  

Easting

Northing

Elevation

  

  

⸻

  

3. Find Nearest Grids

  

The tool compares the picked point with all grid locations.

  

Example result:

  

Nearest Grid X = C

Nearest Grid Y = 5

  

  

⸻

  

Core Script

  

Below is the first working version.

  

from pyrevit import revit, DB

from Autodesk.Revit.UI.Selection import ObjectType

import math

  

uidoc = revit.uidoc

doc = revit.doc

  

# Grid Coordinate finder

point = uidoc.Selection.PickPoint("Select point in model")

  

x = point.X

y = point.Y

z = point.Z

  

# Collect grids

grids = DB.FilteredElementCollector(doc)\

    .OfClass(DB.Grid)\

    .ToElements()

  

closest_grid_x = None

closest_grid_y = None

min_dist_x = 999999

min_dist_y = 999999

  

for grid in grids:

  

    curve = grid.Curve

    grid_pt = curve.GetEndPoint(0)

  

    dx = abs(x - grid_pt.X)

    dy = abs(y - grid_pt.Y)

  

    if dx < min_dist_x:

        min_dist_x = dx

        closest_grid_x = grid.Name

  

    if dy < min_dist_y:

        min_dist_y = dy

        closest_grid_y = grid.Name

  

print("\nGRID LOCATION")

print("Grid:", closest_grid_x, "/", closest_grid_y)

  

print("\nMODEL COORDINATES")

print("X:", round(x,3))

print("Y:", round(y,3))

print("Z:", round(z,3))

  

  

⸻

  

Survey Coordinate Conversion

  

Add this conversion using the coordinate engine we created earlier.

  

Survey Easting

Survey Northing

Survey Elevation

  

Example function:

  

def to_survey(x,y,z,ref_e,ref_n,rotation):

  

    theta = math.radians(rotation)

  

    e = ref_e + x*math.cos(theta) + y*math.sin(theta)

    n = ref_n - x*math.sin(theta) + y*math.cos(theta)

  

    return e,n,z

  

Output example:

  

Easting: 748350.12

Northing: 2134677.90

Elevation: 128.00

  

  

⸻

  

Level Detection

  

The tool also determines the closest level.

  

levels = DB.FilteredElementCollector(doc)\

    .OfClass(DB.Level)\

    .ToElements()

  

closest_level = None

min_dist = 9999

  

for lvl in levels:

  

    dist = abs(z - lvl.Elevation)

  

    if dist < min_dist:

        min_dist = dist

        closest_level = lvl.Name

  

Result:

  

Level 3

  

  

⸻

  

Output Dialog

  

Display the results using a dialog.

  

Example:

  

GRID LOCATION

  

Grid C / Grid 5

  

LEVEL

Level 3

  

SURVEY COORDINATES

Easting: 748350.12

Northing: 2134677.90

Elevation: 128'-0"

  

MODEL COORDINATES

X: 130.12

Y: 245.44

Z: 28.00

  

  

⸻

  

Optional Feature: Copy to Clipboard

  

The tool can automatically copy coordinates for pasting into:

• RFIs

• clash reports

• issue trackers

  

Example output:

  

Grid C5

Level 3

E 748350.12

N 2134677.90

EL 128'-0"

  

  

⸻

  

Optional Feature: Clash Location Tool

  

This tool can also convert Navisworks clash coordinates.

  

Input:

  

Clash coordinate

X,Y,Z

  

Output:

  

Grid C5

Level 3

  

This is extremely valuable for coordination meetings.

  

⸻

  

Toolbar Layout

  

Your BIM automation tools now include:

  

BIM Coordinates

  

Coordinate Setup

Model Alignment

Grid Coordinate Finder

Coordinate Validator

Export CAD UCS

  

This is already a very powerful BIM coordination toolkit.

  

⸻