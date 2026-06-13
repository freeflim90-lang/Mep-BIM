#!/usr/bin/env python3
"""Validate AI expert question profiles for 1-20 year knowledge QA coverage."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CONFIG = PROJECT_ROOT / "config" / "ai_expert_question_profiles.json"
REQUIRED_DIMENSIONS = {
    "concept",
    "application",
    "diagnosis",
    "tradeoff",
    "system",
    "governance",
    "strategy",
}
YEAR_BANDS = {
    "Entry": range(1, 4),
    "Working": range(4, 8),
    "Lead": range(8, 13),
    "Principal": range(13, 17),
    "Strategist": range(17, 21),
}


def error(message: str, fix: str) -> str:
    return f"{message} | fix: {fix}"


def load_config(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def expected_band(year: int) -> str:
    for band, years in YEAR_BANDS.items():
        if year in years:
            return band
    raise ValueError(f"unsupported career year: {year}")


def validate_profiles(config: dict[str, Any]) -> list[str]:
    errors: list[str] = []

    dimensions = set(config.get("required_dimensions", []))
    if dimensions != REQUIRED_DIMENSIONS:
        errors.append(error("required_dimensions must match the standard 7 dimensions", "restore concept/application/diagnosis/tradeoff/system/governance/strategy"))

    roles = config.get("ai_organization_role_lenses", [])
    if len(roles) < 5:
        errors.append(error("ai_organization_role_lenses must include multiple AI organization roles", "add CEO/COO/CFO/product/knowledge/domain role lenses"))
    for role in roles:
        if not role.get("role") or not role.get("expert_field"):
            errors.append(error(f"role lens is incomplete: {role}", "set both role and expert_field"))

    profiles = config.get("career_profiles", [])
    if len(profiles) != 20:
        errors.append(error("career_profiles must contain exactly 20 items", "define one profile for every career year from 1 through 20"))
        return errors

    years = [profile.get("career_year") for profile in profiles]
    if years != list(range(1, 21)):
        errors.append(error(f"career_year sequence is invalid: {years}", "sort and define years exactly as 1..20"))

    depth_levels = [profile.get("depth_level") for profile in profiles]
    if depth_levels != sorted(depth_levels) or depth_levels != list(range(1, 21)):
        errors.append(error(f"depth_level sequence is invalid: {depth_levels}", "make depth_level increase from 1 through 20"))

    band_counts: dict[str, int] = {band: 0 for band in YEAR_BANDS}
    dimension_counts: dict[str, int] = {dimension: 0 for dimension in REQUIRED_DIMENSIONS}

    required_fields = {
        "career_year",
        "band",
        "depth_level",
        "primary_dimensions",
        "question_focus",
        "expected_depth",
        "evidence_requirement",
        "failure_signal",
        "sample_question",
    }

    for profile in profiles:
        missing = sorted(field for field in required_fields if field not in profile)
        if missing:
            errors.append(error(f"profile year {profile.get('career_year')} missing fields: {missing}", "fill all required profile fields"))
            continue

        year = profile["career_year"]
        band = profile["band"]
        if band != expected_band(year):
            errors.append(error(f"career year {year} has band {band}, expected {expected_band(year)}", "align band with career year rubric"))
        band_counts[band] = band_counts.get(band, 0) + 1

        primary_dimensions = profile["primary_dimensions"]
        if not isinstance(primary_dimensions, list) or not primary_dimensions:
            errors.append(error(f"career year {year} primary_dimensions must be a non-empty list", "add at least one required dimension"))
            continue
        unknown = sorted(set(primary_dimensions) - REQUIRED_DIMENSIONS)
        if unknown:
            errors.append(error(f"career year {year} uses unknown dimensions: {unknown}", "use only standard dimensions"))
        for dimension in primary_dimensions:
            if dimension in dimension_counts:
                dimension_counts[dimension] += 1

        for text_field in ["question_focus", "expected_depth", "evidence_requirement", "failure_signal", "sample_question"]:
            if not isinstance(profile[text_field], str) or len(profile[text_field].strip()) < 12:
                errors.append(error(f"career year {year} field {text_field} is too weak", "write a concrete field value"))

        if year >= 8 and not {"diagnosis", "tradeoff", "system"} & set(primary_dimensions):
            errors.append(error(f"career year {year} must include diagnosis/tradeoff/system depth", "add at least one advanced operational dimension"))
        if year >= 13 and "governance" not in primary_dimensions:
            errors.append(error(f"career year {year} must include governance", "principal-level profiles require governance"))
        if year >= 17 and "strategy" not in primary_dimensions:
            errors.append(error(f"career year {year} must include strategy", "strategist-level profiles require strategy"))

    for band, years in YEAR_BANDS.items():
        expected = len(list(years))
        if band_counts.get(band, 0) != expected:
            errors.append(error(f"band {band} has {band_counts.get(band, 0)} profiles, expected {expected}", "restore career year band coverage"))

    missing_dimensions = sorted(dimension for dimension, count in dimension_counts.items() if count == 0)
    if missing_dimensions:
        errors.append(error(f"unused required dimensions: {missing_dimensions}", "cover every required dimension at least once"))

    return errors


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate AI expert career-year question profiles")
    parser.add_argument("--config", type=Path, default=DEFAULT_CONFIG)
    args = parser.parse_args()

    config = load_config(args.config)
    errors = validate_profiles(config)
    if errors:
        print("AI expert question profile validation: FAIL")
        for item in errors:
            print(f"- {item}")
        sys.exit(1)

    print("AI expert question profile validation: PASS")
    print("coverage: career_year=1..20, dimensions=7, bands=5, role_lenses>=5")


if __name__ == "__main__":
    main()
