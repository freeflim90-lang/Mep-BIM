import pandas as pd


def preprocess_energy_data(df: pd.DataFrame, freq: str = "h") -> pd.DataFrame:
    """
    Clean and regularize time-series data.
    """
    if "Datetime" not in df.columns or "Energy" not in df.columns:
        raise ValueError("Input dataframe must include 'Datetime' and 'Energy' columns.")

    clean = df.copy()
    clean["Datetime"] = pd.to_datetime(clean["Datetime"], errors="coerce")
    clean["Energy"] = pd.to_numeric(clean["Energy"], errors="coerce")
    clean = clean.dropna(subset=["Datetime", "Energy"])

    clean = clean.sort_values("Datetime").drop_duplicates(subset=["Datetime"], keep="last")
    clean = clean.set_index("Datetime")

    clean = clean.resample(freq).mean(numeric_only=True)
    clean["Energy"] = clean["Energy"].interpolate(method="time").ffill().bfill()

    q1 = clean["Energy"].quantile(0.25)
    q3 = clean["Energy"].quantile(0.75)
    iqr = q3 - q1
    lower = q1 - 3 * iqr
    upper = q3 + 3 * iqr
    clean["Energy"] = clean["Energy"].clip(lower=lower, upper=upper)

    return clean[["Energy"]]

