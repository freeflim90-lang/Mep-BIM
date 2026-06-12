from dataclasses import asdict

import pandas as pd

from src.config import ProjectConfig
from src.data_loader import ensure_directories, load_or_create_dataset
from src.features import build_training_features
from src.forecasting import iterative_forecast, save_forecast
from src.modeling import (
    evaluate_predictions,
    save_metrics,
    save_model_artifact,
    split_time_series,
    train_model,
)
from src.preprocessing import preprocess_energy_data
from src.visualization import plot_actual_vs_predicted, plot_energy_trend, plot_future_forecast


def run_pipeline(
    model_name: str = "random_forest",
    forecast_horizon: int = 48,
    test_fraction: float = 0.2,
) -> dict:
    config = ProjectConfig()
    ensure_directories(config.root_dir)

    raw_df = load_or_create_dataset(config.data_path)
    clean_df = preprocess_energy_data(raw_df, freq="h")
    plot_energy_trend(clean_df, config.trend_plot_path)

    X, y, _ = build_training_features(clean_df, target_col="Energy")
    X_train, X_test, y_train, y_test = split_time_series(X, y, test_fraction=test_fraction)

    model = train_model(X_train, y_train, model_name=model_name)
    y_pred = model.predict(X_test)
    metrics = evaluate_predictions(y_test, y_pred)

    feature_columns = list(X.columns)
    feature_defaults = X_train.median(numeric_only=True).to_dict()
    save_model_artifact(
        path=config.model_path,
        model=model,
        feature_columns=feature_columns,
        feature_defaults=feature_defaults,
    )
    save_metrics(config.metrics_path, metrics)

    prediction_df = pd.DataFrame(
        {
            "Datetime": X_test.index,
            "Actual_Energy": y_test.values,
            "Predicted_Energy": y_pred,
        }
    )
    prediction_df.to_csv(config.predictions_path, index=False)

    future_df = iterative_forecast(
        model=model,
        history_series=clean_df["Energy"],
        feature_columns=feature_columns,
        horizon=forecast_horizon,
        freq="h",
        feature_defaults=feature_defaults,
    )
    save_forecast(config.forecast_path, future_df)

    plot_actual_vs_predicted(X_test.index, y_test, y_pred, config.actual_vs_pred_plot_path)
    plot_future_forecast(clean_df, future_df, config.forecast_plot_path)

    return {
        "model_name": model_name,
        "forecast_horizon": forecast_horizon,
        "metrics": metrics,
        "rows_in_raw_data": int(len(raw_df)),
        "rows_in_clean_data": int(len(clean_df)),
        "train_rows": int(len(X_train)),
        "test_rows": int(len(X_test)),
        "artifacts": {
            "model_path": str(config.model_path),
            "metrics_path": str(config.metrics_path),
            "predictions_path": str(config.predictions_path),
            "forecast_path": str(config.forecast_path),
            "trend_plot_path": str(config.trend_plot_path),
            "actual_vs_pred_plot_path": str(config.actual_vs_pred_plot_path),
            "forecast_plot_path": str(config.forecast_plot_path),
        },
        "config": {k: str(v) for k, v in asdict(config).items()},
    }

