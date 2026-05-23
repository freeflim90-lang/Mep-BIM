from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


sns.set_theme(style="whitegrid")


def _safe_savefig(path: Path) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(path, dpi=150, bbox_inches="tight")
    plt.close()


def plot_energy_trend(energy_df: pd.DataFrame, save_path: Path) -> None:
    plt.figure(figsize=(14, 5))
    plt.plot(energy_df.index, energy_df["Energy"], color="#2A9D8F", linewidth=1.2)
    plt.title("Energy Consumption Trend")
    plt.xlabel("Datetime")
    plt.ylabel("Energy (kWh)")
    _safe_savefig(save_path)


def plot_actual_vs_predicted(
    index: pd.DatetimeIndex,
    y_true: pd.Series,
    y_pred,
    save_path: Path,
) -> None:
    plt.figure(figsize=(14, 5))
    plt.plot(index, y_true, label="Actual", color="#264653", linewidth=1.4)
    plt.plot(index, y_pred, label="Predicted", color="#E76F51", linewidth=1.2, alpha=0.85)
    plt.title("Actual vs Predicted Energy Consumption (Test Set)")
    plt.xlabel("Datetime")
    plt.ylabel("Energy (kWh)")
    plt.legend()
    _safe_savefig(save_path)


def plot_future_forecast(
    history_df: pd.DataFrame,
    forecast_df: pd.DataFrame,
    save_path: Path,
    history_hours: int = 24 * 7,
) -> None:
    plt.figure(figsize=(14, 5))
    history_slice = history_df.tail(history_hours)

    plt.plot(
        history_slice.index,
        history_slice["Energy"],
        label="Recent History",
        color="#1D3557",
        linewidth=1.4,
    )
    plt.plot(
        pd.to_datetime(forecast_df["Datetime"]),
        forecast_df["Forecast_Energy"],
        label="Forecast",
        color="#F4A261",
        linewidth=1.8,
    )
    plt.title("Future Energy Forecast")
    plt.xlabel("Datetime")
    plt.ylabel("Energy (kWh)")
    plt.legend()
    _safe_savefig(save_path)

