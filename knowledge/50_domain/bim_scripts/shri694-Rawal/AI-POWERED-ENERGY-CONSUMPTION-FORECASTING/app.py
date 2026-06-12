from pathlib import Path

import pandas as pd
from flask import Flask, jsonify, request

from src.features import build_feature_row_for_timestamp
from src.modeling import load_model_artifact

app = Flask(__name__)
MODEL_ARTIFACT_PATH = Path("models") / "energy_forecast_model.joblib"


def _load_artifact():
    if not MODEL_ARTIFACT_PATH.exists():
        raise FileNotFoundError(
            "Model artifact not found. Run `python main.py` first to train and save the model."
        )
    return load_model_artifact(MODEL_ARTIFACT_PATH)


@app.get("/health")
def health():
    return jsonify({"status": "ok"})


@app.post("/predict")
def predict():
    payload = request.get_json(silent=True) or {}

    try:
        artifact = _load_artifact()
    except FileNotFoundError as error:
        return jsonify({"error": str(error)}), 400

    model = artifact["model"]
    feature_columns = artifact["feature_columns"]
    feature_defaults = artifact["feature_defaults"]

    if "timestamp" in payload:
        timestamp = pd.to_datetime(payload["timestamp"], errors="coerce")
    else:
        hour = payload.get("hour")
        day_of_week = payload.get("day_of_week")
        if hour is None or day_of_week is None:
            return (
                jsonify(
                    {
                        "error": "Provide either `timestamp` OR (`hour` and `day_of_week`) in request body."
                    }
                ),
                400,
            )

        now = pd.Timestamp.now().normalize()
        day_gap = (int(day_of_week) - now.dayofweek) % 7
        timestamp = now + pd.Timedelta(days=day_gap, hours=int(hour))

    if pd.isna(timestamp):
        return jsonify({"error": "Invalid timestamp format."}), 400

    history_level = float(feature_defaults.get("lag_1", 100.0))
    history_index = pd.date_range(end=timestamp - pd.Timedelta(hours=1), periods=200, freq="h")
    synthetic_history = pd.Series([history_level] * len(history_index), index=history_index)

    feature_row = build_feature_row_for_timestamp(
        timestamp=timestamp,
        history=synthetic_history,
        feature_defaults=feature_defaults,
    )

    for key, value in payload.items():
        if key in feature_row:
            feature_row[key] = float(value)

    row_df = pd.DataFrame([feature_row])
    for column in feature_columns:
        if column not in row_df.columns:
            row_df[column] = float(feature_defaults.get(column, 0.0))
    row_df = row_df[feature_columns]

    prediction = float(model.predict(row_df)[0])
    return jsonify(
        {
            "timestamp": timestamp.isoformat(),
            "predicted_energy_kwh": round(prediction, 3),
        }
    )


if __name__ == "__main__":
    app.run(debug=True)

