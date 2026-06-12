from pathlib import Path
from typing import Iterable

import pandas as pd

from src.simulation import generate_virtual_energy_data


def ensure_directories(root_dir: Path) -> None:
    """Create required project directories if they do not exist."""
    folders: Iterable[str] = (
        "data",
        "notebooks",
        "src",
        "models",
        "outputs",
        "images",
        "docs",
    )
    for folder in folders:
        (root_dir / folder).mkdir(parents=True, exist_ok=True)


def _pick_first_available_column(df: pd.DataFrame, candidates: list[str]) -> str | None:
    lowered = {col.lower(): col for col in df.columns}
    for candidate in candidates:
        if candidate in lowered:
            return lowered[candidate]
    return None


def standardize_energy_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Normalize different input schemas to a standard:
    - Datetime
    - Energy
    """
    normalized = df.copy()

    datetime_col = _pick_first_available_column(
        normalized,
        ["datetime", "timestamp", "date", "time"],
    )
    energy_col = _pick_first_available_column(
        normalized,
        ["energy", "energy_kwh", "consumption", "load", "usage", "target"],
    )

    if datetime_col is None and isinstance(normalized.index, pd.DatetimeIndex):
        normalized = normalized.reset_index().rename(columns={"index": "Datetime"})
        datetime_col = "Datetime"

    if datetime_col is None:
        raise ValueError(
            "Datetime column not found. Expected one of: datetime, timestamp, date, time."
        )
    if energy_col is None:
        raise ValueError(
            "Energy column not found. Expected one of: energy, energy_kwh, consumption, load."
        )

    normalized = normalized.rename(columns={datetime_col: "Datetime", energy_col: "Energy"})
    normalized["Datetime"] = pd.to_datetime(normalized["Datetime"], errors="coerce")
    normalized["Energy"] = pd.to_numeric(normalized["Energy"], errors="coerce")
    normalized = normalized.dropna(subset=["Datetime", "Energy"])

    keep_cols = ["Datetime", "Energy"]
    if "Temperature" in normalized.columns:
        keep_cols.append("Temperature")
    return normalized[keep_cols]


def load_or_create_dataset(
    data_path: Path,
    start_date: str = "2024-01-01",
    periods: int = 24 * 365 * 2,
) -> pd.DataFrame:
    """
    Load dataset from disk; if missing, generate a virtual simulated dataset.
    """
    data_path = Path(data_path)
    if data_path.exists():
        dataset = pd.read_csv(data_path)
    else:
        dataset = generate_virtual_energy_data(start_date=start_date, periods=periods)
        data_path.parent.mkdir(parents=True, exist_ok=True)
        dataset.to_csv(data_path, index=False)

    return standardize_energy_columns(dataset)

