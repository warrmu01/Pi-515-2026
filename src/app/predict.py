"""
Load saved training pipelines and run inference with the same feature columns
as Data_Preparation/soil_temp_data_preparation.py and soil_moisture_data_preparation.py.
"""

from __future__ import annotations

import datetime as dt
from pathlib import Path

import joblib
import pandas as pd

# Same order as training DataFrames (moisture adds predicted_soil_temp last).
SOIL_TEMP_FEATURES = [
    "latitude",
    "longitude",
    "air_temperature",
    "dewpoint_temperature",
    "total_precipitation",
    "month",
    "day",
]

SOIL_MOISTURE_FEATURES = SOIL_TEMP_FEATURES + ["predicted_soil_temp"]


def _src_dir() -> Path:
    return Path(__file__).resolve().parents[1]


def load_models():
    model_dir = _src_dir() / "models"
    temp_path = model_dir / "soil_temperature_model.joblib"
    moist_path = model_dir / "soil_moisture_model.joblib"
    if not temp_path.is_file():
        raise FileNotFoundError(
            f"Missing {temp_path}. Train and save the model from src/notebooks/soil_temp_model.ipynb first."
        )
    if not moist_path.is_file():
        raise FileNotFoundError(
            f"Missing {moist_path}. Train and save the model from src/notebooks/soil_moisture_model.ipynb first."
        )
    soil_temp = joblib.load(temp_path)
    soil_moisture = joblib.load(moist_path)
    return soil_temp, soil_moisture


def predict_soil_temp(soil_temp_model, weather: dict[str, float], latitude: float, longitude: float, day: dt.date):
    row = {
        "latitude": latitude,
        "longitude": longitude,
        "air_temperature": weather["air_temperature"],
        "dewpoint_temperature": weather["dewpoint_temperature"],
        "total_precipitation": weather["total_precipitation"],
        "month": day.month,
        "day": day.day,
    }
    X = pd.DataFrame([row], columns=SOIL_TEMP_FEATURES)
    pred = float(soil_temp_model.predict(X)[0])
    return pred, X


def predict_soil_moisture(soil_moisture_model, X_temp_row: pd.DataFrame, predicted_soil_temp: float):
    X = X_temp_row.copy()
    X["predicted_soil_temp"] = predicted_soil_temp
    X = X[SOIL_MOISTURE_FEATURES]
    pred = float(soil_moisture_model.predict(X)[0])
    return pred


def irrigation_band(soil_moisture_pred: float) -> str:
    """
    Map predicted soil moisture to irrigation need labels (tunable thresholds).

    Lower moisture -> higher irrigation need (matches README intent).
    Adjust IR_* if your training target uses a different scale.
    """
    high_need_threshold = 0.20
    if soil_moisture_pred < high_need_threshold:
        return "HIGH"
    return "MEDIUM"
