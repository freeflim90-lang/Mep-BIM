# AI-Powered Energy Consumption Forecasting

Forecast hourly electricity consumption using a production-inspired Python pipeline with modeling, evaluation, forecasting, and visualization.

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

## Why it matters

Energy providers, smart buildings, and grid operators depend on accurate demand forecasts to:
- avoid outages and grid instability
- minimize overgeneration and energy waste
- reduce peak-time costs
- support cleaner, more reliable operations

This project produces actionable demand forecasts from historical usage data and saves the results as reports, plots, and reusable artifacts.

## What it includes

- automatic dataset loading or synthetic hourly dataset generation
- preprocessing, resampling, and anomaly-safe cleaning
- time-based feature engineering, lag features, and rolling statistics
- model training with `RandomForestRegressor` or `LinearRegression`
- evaluation with `RMSE`, `MAE`, and `R²`
- future forecast export and plot generation
- optional Flask API for inference

## Dataset details

The repository supports:
- a source CSV file: `data/energy.csv`
- or an automatically generated synthetic dataset when the file is missing

The synthetic dataset includes realistic patterns for:
- daily morning and evening peaks
- weekend demand changes
- seasonal temperature-driven HVAC load
- long-term trend and random noise

Standard pipeline columns:
- `Datetime`
- `Energy`
- `Temperature` (optional)

## Models

Available models:
- `random_forest` — ensemble regression with 350 trees and controlled depth
- `linear_regression` — baseline linear model for quick comparison

The pipeline maintains a chronological time-series split and avoids shuffling to preserve temporal integrity.

## Latest results

Metrics from the most recent run:

- **RMSE:** 5.52
- **MAE:** 4.38
- **R²:** 0.856

### Visual outputs

![Energy Consumption Trend](images/energy_trend.png)

![Actual vs Predicted Energy](images/actual_vs_predicted.png)

![Future Energy Forecast](images/future_forecast.png)

## Quick start

Initialize the project environment and install dependencies:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install --upgrade pip
pip install -r requirements.txt
```

Run the forecasting pipeline:

```powershell
python main.py --model random_forest --forecast-horizon 72 --test-fraction 0.2
```

Optional Flask API:

```powershell
python app.py
```

Then send a prediction request to `POST /predict` with:

```json
{ "timestamp": "2026-04-15 14:00:00" }
```

or

```json
{ "hour": 14, "day_of_week": 2 }
```

See `QUICKSTART.md` for a condensed setup guide.

## Project structure

```text
AI-Powered Energy Consumption Forecasting/
├── app.py
├── CHANGELOG.md
├── CONTRIBUTING.md
├── LICENSE
├── QUICKSTART.md
├── README.md
├── data/
├── docs/
├── images/
├── models/
├── notebooks/
├── outputs/
├── requirements.txt
└── src/
```

## Generated artifacts

After a successful run, the repository writes:
- `models/energy_forecast_model.joblib`
- `outputs/metrics.json`
- `outputs/test_predictions.csv`
- `outputs/future_forecast.csv`
- `images/energy_trend.png`
- `images/actual_vs_predicted.png`
- `images/future_forecast.png`

## Documentation

- `docs/README.md` — docs folder index
- `docs/architecture.md` — architectural design and data flow
- `docs/github-proof-plan.md` — project proofing plan for GitHub
- `docs/implementation-phases.md` — development milestones
- `docs/proof-checklist.md` — release readiness checklist

## License

This project is available under the MIT License. See `LICENSE` for details.

