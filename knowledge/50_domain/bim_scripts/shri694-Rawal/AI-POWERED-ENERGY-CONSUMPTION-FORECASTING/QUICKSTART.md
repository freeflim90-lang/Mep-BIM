# Quick Start

Use this guide to install dependencies and run the forecasting pipeline quickly.

## 1. Create a virtual environment

Windows PowerShell:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install --upgrade pip
pip install -r requirements.txt
```

Mac/Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

## 2. Run the forecasting pipeline

```bash
python main.py --model random_forest --forecast-horizon 72 --test-fraction 0.2
```

This generates:

- `models/energy_forecast_model.joblib`
- `outputs/metrics.json`
- `outputs/test_predictions.csv`
- `outputs/future_forecast.csv`
- `images/energy_trend.png`
- `images/actual_vs_predicted.png`
- `images/future_forecast.png`

## 3. Start the optional Flask API

```bash
python app.py
```

Then send a request to `POST /predict` with a JSON body:

```json
{
  "timestamp": "2026-04-15 14:00:00"
}
```

or

```json
{
  "hour": 14,
  "day_of_week": 2
}
```

## 4. Explore the docs

- `docs/architecture.md`
- `docs/github-proof-plan.md`
- `docs/implementation-phases.md`
- `docs/proof-checklist.md`
