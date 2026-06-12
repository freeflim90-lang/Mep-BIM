import argparse
import logging
import os

from ifc_material_qto.processing import process_ifc, write_csv

def main():
    parser = argparse.ArgumentParser(
        description="Extract material quantities from IFC files"
    )
    parser.add_argument(
        "ifc_paths",
        nargs="+",
        help="Path to one or more IFC files"
    )
    parser.add_argument(
        "--use-geometry",
        action=argparse.BooleanOptionalAction,
        default=True,
        help="Compute quantities from geometry if no IFC quantities exist"
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Enable verbose (debug) output"
    )
    parser.add_argument(
        "--quiet",
        action="store_true",
        help="Output only errors"
    )
    parser.add_argument(
        "--output-dir",
        default="results",
        help="Directory where CSV files will be written (default: results)"
    )
    args = parser.parse_args()

    if args.verbose and args.quiet:
        parser.error("Cannot use --verbose and --quiet together")

    if args.verbose:
        level = logging.DEBUG
    elif args.quiet:
        level = logging.ERROR
    else:
        level = logging.INFO

    logging.basicConfig(
        level=level,
        format="%(levelname)s: %(message)s"
    )

    for p in args.ifc_paths:
        if not os.path.isfile(p):
            parser.error(f"File not found: {p}")

    os.makedirs(args.output_dir, exist_ok=True)
    for ifc_path in args.ifc_paths:
        material_data = process_ifc(ifc_path, args.use_geometry)
        base = os.path.basename(ifc_path)
        output_csv = os.path.join(args.output_dir, f"{base}_materials.csv")
        write_csv(material_data, output_csv)

if __name__ == "__main__":
    main()