import numpy as np
import pandas as pd


def add_time_features(index: pd.DatetimeIndex) -> pd.DataFrame:
    """Create calendar and cyclical time features from datetime index."""
    frame = pd.DataFrame(index=index)
    frame["hour"] = index.hour
    frame["day_of_week"] = index.dayofweek
    frame["month"] = index.month
    frame["day_of_year"] = index.dayofyear
    frame["is_weekend"] = (frame["day_of_week"] >= 5).astype(int)

    frame["hour_sin"] = np.sin(2 * np.pi * frame["hour"] / 24)
    frame["hour_cos"] = np.cos(2 * np.pi * frame["hour"] / 24)
    frame["dow_sin"] = np.sin(2 * np.pi * frame["day_of_week"] / 7)
    frame["dow_cos"] = np.cos(2 * np.pi * frame["day_of_week"] / 7)
    return frame


def build_training_features(
    energy_df: pd.DataFrame,
    target_col: str = "Energy",
) -> tuple[pd.DataFrame, pd.Series, pd.DataFrame]:
    """
    Create ML-ready features for model training.
    """
    if target_col not in energy_df.columns:
        raise ValueError(f"Target column '{target_col}' not found in dataframe.")

    dataset = pd.DataFrame(index=energy_df.index)
    dataset[target_col] = energy_df[target_col].astype(float)
    dataset = dataset.join(add_time_features(dataset.index))

    dataset["lag_1"] = dataset[target_col].shift(1)
    dataset["lag_24"] = dataset[target_col].shift(24)
    dataset["lag_168"] = dataset[target_col].shift(168)

    dataset["rolling_mean_24"] = dataset[target_col].rolling(24).mean()
    dataset["rolling_std_24"] = dataset[target_col].rolling(24).std()

    dataset = dataset.dropna()

    X = dataset.drop(columns=[target_col])
    y = dataset[target_col]
    return X, y, dataset


def build_feature_row_for_timestamp(
    timestamp: pd.Timestamp,
    history: pd.Series,
    feature_defaults: dict[str, float] | None = None,
) -> dict[str, float]:
    """
    Build one feature row for a single future timestamp using historical energy series.
    """
    timestamp = pd.Timestamp(timestamp)
    time_features = add_time_features(pd.DatetimeIndex([timestamp])).iloc[0].to_dict()

    row: dict[str, float] = {k: float(v) for k, v in time_features.items()}
    row["lag_1"] = float(history.iloc[-1]) if len(history) >= 1 else 0.0
    row["lag_24"] = float(history.iloc[-24]) if len(history) >= 24 else row["lag_1"]
    row["lag_168"] = float(history.iloc[-168]) if len(history) >= 168 else row["lag_24"]

    recent_24 = history.iloc[-24:] if len(history) >= 24 else history
    row["rolling_mean_24"] = float(recent_24.mean()) if len(recent_24) else row["lag_1"]
    row["rolling_std_24"] = float(recent_24.std(ddof=0)) if len(recent_24) > 1 else 0.0

    if feature_defaults:
        for key, value in feature_defaults.items():
            row.setdefault(key, float(value))

    return row

