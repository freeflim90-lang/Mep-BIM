import json
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score


def split_time_series(
    X: pd.DataFrame,
    y: pd.Series,
    test_fraction: float = 0.2,
) -> tuple[pd.DataFrame, pd.DataFrame, pd.Series, pd.Series]:
    """Chronological train/test split (no shuffling for time series)."""
    if not (0 < test_fraction < 1):
        raise ValueError("test_fraction must be between 0 and 1.")
    if len(X) < 50:
        raise ValueError("Dataset is too small after feature engineering.")

    split_index = int(len(X) * (1 - test_fraction))
    X_train, X_test = X.iloc[:split_index], X.iloc[split_index:]
    y_train, y_test = y.iloc[:split_index], y.iloc[split_index:]
    return X_train, X_test, y_train, y_test


def train_model(
    X_train: pd.DataFrame,
    y_train: pd.Series,
    model_name: str = "random_forest",
):
    """Train and return selected regression model."""
    normalized = model_name.strip().lower()

    if normalized == "linear_regression":
        model = LinearRegression()
    elif normalized == "random_forest":
        model = RandomForestRegressor(
            n_estimators=350,
            random_state=42,
            n_jobs=-1,
            max_depth=18,
            min_samples_leaf=2,
        )
    else:
        raise ValueError(
            f"Unsupported model_name '{model_name}'. Use 'random_forest' or 'linear_regression'."
        )

    model.fit(X_train, y_train)
    return model


def evaluate_predictions(y_true: pd.Series, y_pred) -> dict[str, float]:
    """Compute core regression metrics."""
    rmse = float(np.sqrt(mean_squared_error(y_true, y_pred)))
    mae = mean_absolute_error(y_true, y_pred)
    r2 = r2_score(y_true, y_pred)
    return {
        "rmse": rmse,
        "mae": float(mae),
        "r2": float(r2),
    }


def save_model_artifact(
    path: Path,
    model,
    feature_columns: list[str],
    feature_defaults: dict[str, float],
) -> None:
    artifact = {
        "model": model,
        "feature_columns": feature_columns,
        "feature_defaults": feature_defaults,
    }
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(artifact, path)


def load_model_artifact(path: Path):
    return joblib.load(path)


def save_metrics(path: Path, metrics: dict[str, float]) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as file:
        json.dump(metrics, file, indent=2)
