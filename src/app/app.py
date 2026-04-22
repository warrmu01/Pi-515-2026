"""
Minimal Flask UI: lat/lon + date -> Open-Meteo weather -> chained model predictions.

Run from the `src` folder:
    python -m app.app
Then open http://127.0.0.1:5000
"""

from __future__ import annotations

import datetime as dt
import re

from flask import Flask, render_template, request

from app.open_meteo import fetch_daily_weather
from app.predict import (
    irrigation_band,
    load_models,
    predict_soil_moisture,
    predict_soil_temp,
)

app = Flask(__name__)

_soil_temp_model = None
_soil_moisture_model = None


def get_models():
    global _soil_temp_model, _soil_moisture_model
    if _soil_temp_model is None or _soil_moisture_model is None:
        _soil_temp_model, _soil_moisture_model = load_models()
    return _soil_temp_model, _soil_moisture_model


@app.route("/", methods=["GET"])
def landing():
    return render_template("landing.html")


@app.route("/predict", methods=["GET", "POST"])
def predict_page():
    result = None
    daily_results = []
    error = None
    show_result = False
    min_date = (dt.date.today() + dt.timedelta(days=1)).isoformat()
    if request.method == "POST":
        try:
            lat = float(request.form.get("latitude", "").strip())
            lon = float(request.form.get("longitude", "").strip())
            start_date_s = request.form.get("start_date", "").strip()
            end_date_s = request.form.get("end_date", "").strip()
            date_range_s = request.form.get("date_range", "").strip()
            st_model, sm_model = get_models()

            # Support a single date-range field from the UI.
            if (not start_date_s or not end_date_s) and date_range_s:
                parts = re.split(r"\s+to\s+", date_range_s)
                if len(parts) == 2:
                    start_date_s, end_date_s = parts[0].strip(), parts[1].strip()

            if not start_date_s or not end_date_s:
                raise ValueError("Please select both a start and end date in the range picker.")

            start_day = dt.date.fromisoformat(start_date_s)
            end_day = dt.date.fromisoformat(end_date_s)
            today = dt.date.today()
            if start_day <= today or end_day <= today:
                raise ValueError("Please select future dates for both start and end.")
            if end_day < start_day:
                raise ValueError("End date must be on or after start date.")

            total_days = (end_day - start_day).days + 1
            for offset in range(total_days):
                day = start_day + dt.timedelta(days=offset)
                weather = fetch_daily_weather(lat, lon, day)
                soil_temp_pred, X_row = predict_soil_temp(st_model, weather, lat, lon, day)
                soil_moist_pred = predict_soil_moisture(sm_model, X_row, soil_temp_pred)
                daily_results.append(
                    {
                        "date": day.isoformat(),
                        "soil_temperature": round(soil_temp_pred, 4),
                        "soil_moisture": round(soil_moist_pred, 4),
                        "irrigation_recommendation": irrigation_band(soil_moist_pred),
                    }
                )

            # Keep first day as summary if needed by template.
            result = daily_results[0]
            show_result = True
        except Exception as exc:  # noqa: BLE001 — surface any failure to the user
            error = str(exc)
    return render_template(
        "index.html",
        result=result,
        daily_results=daily_results,
        error=error,
        show_result=show_result,
        min_date=min_date,
    )


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
