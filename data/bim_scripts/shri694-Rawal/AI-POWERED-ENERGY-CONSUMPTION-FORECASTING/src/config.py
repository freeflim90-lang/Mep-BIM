from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class ProjectConfig:
    """Centralized project paths used across the pipeline."""

    root_dir: Path = Path(__file__).resolve().parents[1]

    data_path: Path = root_dir / "data" / "energy.csv"
    model_path: Path = root_dir / "models" / "energy_forecast_model.joblib"

    metrics_path: Path = root_dir / "outputs" / "metrics.json"
    predictions_path: Path = root_dir / "outputs" / "test_predictions.csv"
    forecast_path: Path = root_dir / "outputs" / "future_forecast.csv"

    trend_plot_path: Path = root_dir / "images" / "energy_trend.png"
    actual_vs_pred_plot_path: Path = root_dir / "images" / "actual_vs_predicted.png"
    forecast_plot_path: Path = root_dir / "images" / "future_forecast.png"

