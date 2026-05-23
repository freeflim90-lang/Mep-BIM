from pathlib import Path

import pandas as pd

from src.features import build_feature_row_for_timestamp


def iterative_forecast(
    model,
    history_series: pd.Series,
    feature_columns: list[str],
    horizon: int = 48,
    freq: str = "h",
    feature_defaults: dict[str, float] | None = None,
) -> pd.DataFrame:
    """
    Forecast future energy values iteratively.
    Each predicted step becomes part of history for the next step.
    """
    if horizon <= 0:
        raise ValueError("horizon must be greater than 0.")
    if len(history_series) < 168:
        raise ValueError("Need at least 168 historical rows for stable lag features.")

    history = history_series.copy().astype(float)
    if not isinstance(history.index, pd.DatetimeIndex):
        raise ValueError("history_series index must be DatetimeIndex.")

    start = history.index[-1] + pd.tseries.frequencies.to_offset(freq)
    future_index = pd.date_range(start=start, periods=horizon, freq=freq)

    predictions: list[float] = []
    for timestamp in future_index:
        row = build_feature_row_for_timestamp(
            timestamp=timestamp,
            history=history,
            feature_defaults=feature_defaults,
        )
        row_df = pd.DataFrame([row])

        for column in feature_columns:
            if column not in row_df.columns:
                default_value = 0.0 if feature_defaults is None else float(feature_defaults.get(column, 0.0))
                row_df[column] = default_value

        row_df = row_df[feature_columns]
        prediction = float(model.predict(row_df)[0])
        predictions.append(prediction)
        history.loc[timestamp] = prediction

    return pd.DataFrame(
        {
            "Datetime": future_index,
            "Forecast_Energy": predictions,
        }
    )


def save_forecast(path: Path, forecast_df: pd.DataFrame) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    forecast_df.to_csv(path, index=False)

