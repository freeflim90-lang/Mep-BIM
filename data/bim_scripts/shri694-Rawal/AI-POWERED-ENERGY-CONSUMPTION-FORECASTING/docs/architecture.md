# System Architecture

## Text Block Diagram

```text
Historical Energy Data (CSV / Virtual Simulation)
                |
                v
        Data Loading & Validation
                |
                v
      Preprocessing (resample, fill NA, clean)
                |
                v
  Feature Engineering (time, lag, rolling stats)
                |
                v
      Model Training (Random Forest / Linear)
                |
                +-------------------------+
                |                         |
                v                         v
    Evaluation (RMSE, MAE, R2)      Save Model Artifact
                |                         |
                v                         |
         Result Visualizations            |
                |                         |
                +------------+------------+
                             |
                             v
            Iterative Future Forecast Generation
                             |
                             v
        CSV + Plots + API Inference (optional Flask)
```

## Data Flow Summary

1. Raw data is loaded from `data/energy.csv`.
2. Missing file fallback triggers synthetic dataset generation.
3. Data is normalized to standard columns (`Datetime`, `Energy`).
4. Time-series is cleaned and regularized to hourly granularity.
5. Features are built using temporal and historical lag behavior.
6. Model is trained and evaluated with chronological train/test split.
7. Artifacts and visuals are saved for reporting and GitHub proof.

