# IFC Material QTO

IFC Material QTO is a Python CLI tool to extract material volumes from IFC files. It computes quantities per material, supports multiple IFC files at once, and can optionally calculate volumes from geometry when IFC quantities are missing.

## Features

- Extract material volumes from one or more IFC files
- Automatically handle layered materials
- Fallback to geometry-based volume calculation if IFC quantities are missing
- Write per-file CSVs to a custom output directory (default: `results/`)
- Supports verbose and quiet logging
- MIT licensed

## Calculation Assumptions

For elements with layered materials (`IfcMaterialLayerSetUsage`), total element volume is distributed across layers proportionally to their thickness.
The calculation used is:
```
ratio = layer.LayerThickness / total_thickness
layer_volume = element_volume * ratio
```
This means:
- The sum of all layer volumes equals the total element volume
- Layers are assumed to occupy equal area and vary only by thickness
- No voids, overlaps, or material inefficiencies are considered
> $\color{Yellow}{\textbf{IMPORTANT!}}$ This is a simplification and may not reflect real-world construction details in all cases. For highly accurate takeoffs, verify results against project-specific modeling practices.

## Installation

### Using uv (recommended)
```bash
git clone https://github.com/your-username/ifc-material-qto.git
cd ifc-material-qto
uv sync
```

### Using pip
```bash
git clone https://github.com/your-username/ifc-material-qto.git
cd ifc-material-qto
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
# .\.venv\Scripts\activate  # Windows
pip install .
```

## Requirements

- Python 3.10+
- ifcopenshell

## Usage

```bash
uv run ifc-material-qto <file1.ifc> [file2.ifc ...] [--use-geometry] [--output-dir OUTPUT_DIR] [--verbose|--quiet]
```

## Examples
- Process a single IFC file with default settings:
```bash
uv run ifc-material-qto building.ifc
```

- Process multiple IFC files and write CSVs to a custom folder:
```bash
uv run ifc-material-qto building1.ifc building2.ifc --output-dir exports
```
- Disable geometry fallback:
```bash
uv run ifc-material-qto building.ifc --no-use-geometry
```

- Enable verbose output:
```bash
uv run ifc-material-qto building.ifc --verbose
```

## Output
By default, CSVs are written into a folder named `results/`.
Each CSV contains `material`, `volume(m3)`, `element_count`

## License
This project is licensed under the MIT License.
