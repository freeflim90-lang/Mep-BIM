"""
clash_parser.py — Parse Navisworks XML clash report into heatmap CSV.

Input:
  data/input/clash_report.xml        — Navisworks XML export
  data/output/grid_lines.csv         — from ExportGrids pyRevit button
  data/output/level_elevations.csv   — from ExportGrids pyRevit button

Output:
  data/output/clash_heatmap_data.csv
  Columns: ClashID, Status, DisciplineA, DisciplineB, Level, GridZone, X, Y, Z

Called as Stage 0 in main.py. If clash_report.xml is absent, logs and
returns immediately — not an error (XML export is a manual Tuesday step).

Discipline pair is extracted from the clash test name (e.g. "Arch vs Structure").
Level is the highest level whose elevation <= clash Z. Below all levels = "Below Grade".
GridZone is "VertGrid1-VertGrid2/HorizGrid1-HorizGrid2". Outside grid = "Outside Grid".
"""
import bisect
import csv
import logging
import os
import xml.etree.ElementTree as ET

logger = logging.getLogger(__name__)

XML_FILENAME = "clash_report.xml"
HEATMAP_FILENAME = "clash_heatmap_data.csv"
GRID_FILENAME = "grid_lines.csv"
LEVEL_FILENAME = "level_elevations.csv"

HEADERS = [
    "ClashID", "Status", "DisciplineA", "DisciplineB",
    "Level", "GridZone", "X", "Y", "Z",
]


# ---------------------------------------------------------------------------
# Data loaders
# ---------------------------------------------------------------------------

def load_grid_lines(output_dir):
    """Return (vertical_grids, horizontal_grids) sorted by Position.
    Each list contains (position_float, name_str) tuples.
    Returns (None, None) if file is missing."""
    path = os.path.join(output_dir, GRID_FILENAME)
    if not os.path.exists(path):
        logger.warning("grid_lines.csv not found — GridZone will show 'No Grid Data'")
        return None, None
    vertical, horizontal = [], []
    with open(path, "r") as f:
        for row in csv.DictReader(f):
            pos = float(row["Position"])
            name = row["GridName"]
            if row["Orientation"] == "V":
                vertical.append((pos, name))
            else:
                horizontal.append((pos, name))
    vertical.sort()
    horizontal.sort()
    return vertical, horizontal


def load_levels(output_dir):
    """Return list of (elevation_float, level_name_str) sorted by elevation asc.
    Returns None if file is missing."""
    path = os.path.join(output_dir, LEVEL_FILENAME)
    if not os.path.exists(path):
        logger.warning("level_elevations.csv not found — Level will show raw Z")
        return None
    levels = []
    with open(path, "r") as f:
        for row in csv.DictReader(f):
            levels.append((float(row["Elevation"]), row["LevelName"]))
    levels.sort()
    return levels


# ---------------------------------------------------------------------------
# Coordinate mappers
# ---------------------------------------------------------------------------

def map_level(z, levels):
    """Return level name for given Z elevation.
    Finds the highest level whose elevation <= z."""
    if levels is None:
        return str(round(z, 2))
    elevations = [lv[0] for lv in levels]
    idx = bisect.bisect_right(elevations, z) - 1
    if idx < 0:
        return "Below Grade"
    return levels[idx][1]


def find_bracket(pos, grids):
    """Return 'Name1-Name2' for the bay pos falls in, or edge labels."""
    if not grids:
        return "?"
    positions = [g[0] for g in grids]
    names = [g[1] for g in grids]
    idx = bisect.bisect_right(positions, pos) - 1
    if idx < 0:
        return "<" + names[0]
    if idx >= len(grids) - 1:
        return ">" + names[-1]
    return names[idx] + "-" + names[idx + 1]


def map_grid_zone(x, y, vertical, horizontal):
    """Return GridZone string like 'A-B/1-2'."""
    if vertical is None or horizontal is None:
        return "No Grid Data"
    v_zone = find_bracket(x, vertical)
    h_zone = find_bracket(y, horizontal)
    return "{}/{}".format(v_zone, h_zone)


# ---------------------------------------------------------------------------
# XML parser
# ---------------------------------------------------------------------------

def parse_discipline_pair(test_name):
    """Extract DisciplineA, DisciplineB from test name like 'Arch vs Structure'."""
    if " vs " in test_name:
        parts = test_name.split(" vs ", 1)
        return parts[0].strip(), parts[1].strip()
    return test_name.strip(), "Unknown"


def parse_xml(xml_path, vertical, horizontal, levels):
    """Parse Navisworks XML and return list of rows matching HEADERS."""
    rows = []
    tree = ET.parse(xml_path)
    root = tree.getroot()

    for clashtest in root.iter("clashtest"):
        test_name = clashtest.get("name", "Unknown")
        disc_a, disc_b = parse_discipline_pair(test_name)

        for clash in clashtest.iter("clashresult"):
            clash_id = clash.get("name", "")
            status = clash.get("status", "active")

            pos = clash.find(".//clashpoint/pos3f")
            if pos is None:
                continue  # skip clashes with no position data

            x = float(pos.get("x", 0))
            y = float(pos.get("y", 0))
            z = float(pos.get("z", 0))

            level = map_level(z, levels)
            grid_zone = map_grid_zone(x, y, vertical, horizontal)

            rows.append([
                clash_id, status, disc_a, disc_b,
                level, grid_zone,
                round(x, 4), round(y, 4), round(z, 4),
            ])

    return rows


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def run(input_dir=None, output_dir=None):
    """Run the clash parser. Called from main.py as Stage 0.
    Accepts optional path overrides for testing."""
    from config import INPUT_DIR, OUTPUT_DIR
    input_dir = str(input_dir or INPUT_DIR)
    output_dir = str(output_dir or OUTPUT_DIR)

    xml_path = os.path.join(input_dir, XML_FILENAME)
    if not os.path.exists(xml_path):
        logger.info(
            "clash_report.xml not found in %s — skipping clash parser "
            "(place Navisworks XML export there on Tuesday)", input_dir
        )
        return 0

    vertical, horizontal = load_grid_lines(output_dir)
    levels = load_levels(output_dir)

    logger.info("Parsing %s", xml_path)
    rows = parse_xml(xml_path, vertical, horizontal, levels)

    out_path = os.path.join(output_dir, HEATMAP_FILENAME)
    os.makedirs(output_dir, exist_ok=True)
    with open(out_path, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(HEADERS)
        w.writerows(rows)

    logger.info("clash_heatmap_data.csv written — %d clashes", len(rows))
    return len(rows)


if __name__ == "__main__":
    import sys
    logging.basicConfig(level=logging.INFO)
    sys.path.insert(0, str(__import__("pathlib").Path(__file__).parent.parent))
    run()
