"""
coord_utils.py — Shared coordinate math and Extensible Storage I/O.

Import in any script with: from coord_utils import load_coords, to_survey, ...
"""
import math

import clr
clr.AddReference("RevitAPI")
from Autodesk.Revit.DB import (
    FilteredElementCollector,
    DataStorage,
    Transaction,
)
from Autodesk.Revit.DB.ExtensibleStorage import (
    SchemaBuilder,
    AccessLevel,
    Entity,
    Schema,
)
import System

# ---------------------------------------------------------------------------
# Extensible Storage schema
# ---------------------------------------------------------------------------
_SCHEMA_GUID = System.Guid("4b7c9a2e-1f3d-4e8b-a5c6-d2e0f1b3a7c9")
_SCHEMA_NAME = "BIMCoordinates"


def _get_or_create_schema():
    existing = Schema.Lookup(_SCHEMA_GUID)
    if existing:
        return existing
    b = SchemaBuilder(_SCHEMA_GUID)
    b.SetSchemaName(_SCHEMA_NAME)
    b.SetReadAccessLevel(AccessLevel.Public)
    b.SetWriteAccessLevel(AccessLevel.Public)
    b.AddSimpleField("easting",      System.Double)
    b.AddSimpleField("northing",     System.Double)
    b.AddSimpleField("elevation",    System.Double)
    b.AddSimpleField("rotation_deg", System.Double)
    b.AddSimpleField("ref_grid",     System.String)
    return b.Finish()


def save_coords(doc, easting, northing, elevation, rotation_deg, ref_grid):
    """Store project coordinate values in Revit Extensible Storage."""
    schema = _get_or_create_schema()
    # Find existing DataStorage for this schema, or create one
    storage = None
    for ds in FilteredElementCollector(doc).OfClass(DataStorage).ToElements():
        if ds.GetEntity(schema).IsValid():
            storage = ds
            break
    t = Transaction(doc, "BIMTools: Save Coordinates")
    t.Start()
    if storage is None:
        storage = DataStorage.Create(doc)
    entity = Entity(schema)
    entity.Set("easting",      float(easting))
    entity.Set("northing",     float(northing))
    entity.Set("elevation",    float(elevation))
    entity.Set("rotation_deg", float(rotation_deg))
    entity.Set("ref_grid",     str(ref_grid))
    storage.SetEntity(entity)
    t.Commit()


def load_coords(doc):
    """
    Read project coordinate values from Extensible Storage.
    Returns dict with keys: easting, northing, elevation, rotation_deg, ref_grid
    Returns None if not set.
    """
    schema = Schema.Lookup(_SCHEMA_GUID)
    if schema is None:
        return None
    for ds in FilteredElementCollector(doc).OfClass(DataStorage).ToElements():
        entity = ds.GetEntity(schema)
        if entity.IsValid():
            return {
                "easting":      entity.Get[System.Double]("easting"),
                "northing":     entity.Get[System.Double]("northing"),
                "elevation":    entity.Get[System.Double]("elevation"),
                "rotation_deg": entity.Get[System.Double]("rotation_deg"),
                "ref_grid":     entity.Get[System.String]("ref_grid"),
            }
    return None


# ---------------------------------------------------------------------------
# Coordinate math
# ---------------------------------------------------------------------------

def to_model(easting, northing, elevation, ref_e, ref_n, base_z, rot_deg):
    """Convert survey coordinates to model (Revit internal) coordinates."""
    theta = math.radians(rot_deg)
    dx = easting  - ref_e
    dy = northing - ref_n
    x = dx * math.cos(theta) - dy * math.sin(theta)
    y = dx * math.sin(theta) + dy * math.cos(theta)
    z = elevation - base_z
    return round(x, 4), round(y, 4), round(z, 4)


def to_survey(x, y, z, ref_e, ref_n, base_z, rot_deg):
    """Convert model coordinates back to survey coordinates (reverse transform)."""
    theta = math.radians(rot_deg)
    e = ref_e + x * math.cos(theta) + y * math.sin(theta)
    n = ref_n - x * math.sin(theta) + y * math.cos(theta)
    elev = z + base_z
    return round(e, 4), round(n, 4), round(elev, 4)


def check_large_coords(easting, northing):
    """
    Return a warning string if survey coordinates are dangerously far from origin.
    Revit geometry becomes unstable beyond ~105,600 ft (20 miles).
    Returns None if coords are safe.
    """
    distance = math.sqrt(easting ** 2 + northing ** 2)
    if distance > 105600:
        shift_e = -(int(easting / 1000) * 1000)
        shift_n = -(int(northing / 1000) * 1000)
        return (
            "WARNING: Survey coordinates are {:.0f} ft from origin (limit ~105,600 ft).\n"
            "Recommended Revit origin shift: X={}, Y={}\n"
            "This keeps geometry stable while preserving survey values."
        ).format(distance, shift_e, shift_n)
    return None


def calc_rotation(e1, n1, e2, n2):
    """
    Calculate project north rotation (degrees) from two known grid points.
    Point 1 should be the reference (e.g. Grid A1), Point 2 a second known point.
    """
    return math.degrees(math.atan2(e2 - e1, n2 - n1))
