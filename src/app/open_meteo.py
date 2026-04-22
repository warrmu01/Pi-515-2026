"""
Fetch daily weather for one calendar day from Open-Meteo (no API key).

- Last ~93 days + near future: Forecast API (past_days cap is 93).
- Older past dates: Historical Archive API (ERA5).
"""

from __future__ import annotations

import datetime as dt
from typing import Any
from urllib.parse import urlencode
from urllib.request import urlopen
import json


FORECAST_URL = "https://api.open-meteo.com/v1/forecast"
ARCHIVE_URL = "https://archive-api.open-meteo.com/v1/archive"


def _read_json(url: str) -> dict[str, Any]:
    with urlopen(url, timeout=30) as resp:
        return json.loads(resp.read().decode())


def _mean_or_none(a: float | None, b: float | None) -> float | None:
    if a is None and b is None:
        return None
    if a is None:
        return float(b)
    if b is None:
        return float(a)
    return (float(a) + float(b)) / 2.0


def _row_from_forecast_daily(daily: dict[str, Any], idx: int) -> dict[str, float]:
    tmax = daily.get("temperature_2m_max", [None])[idx]
    tmin = daily.get("temperature_2m_min", [None])[idx]
    dmax = daily.get("dew_point_2m_max", [None])[idx]
    dmin = daily.get("dew_point_2m_min", [None])[idx]
    air = _mean_or_none(tmax, tmin)
    dew = _mean_or_none(dmax, dmin)
    precip = daily.get("precipitation_sum", [None])[idx]
    if air is None or dew is None:
        raise RuntimeError("Open-Meteo response missing temperature or dew point for that day.")
    precip_val = 0.0 if precip is None else float(precip)
    return {
        "air_temperature": float(air),
        "dewpoint_temperature": float(dew),
        "total_precipitation": precip_val,
    }


def _fetch_forecast_window(latitude: float, longitude: float, past_days: int, forecast_days: int) -> dict[str, Any]:
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "timezone": "UTC",
        "past_days": past_days,
        "forecast_days": forecast_days,
        "daily": "temperature_2m_max,temperature_2m_min,dew_point_2m_max,dew_point_2m_min,precipitation_sum",
    }
    data = _read_json(f"{FORECAST_URL}?{urlencode(params)}")
    err = data.get("reason") or data.get("error")
    if err:
        raise RuntimeError(f"Open-Meteo error: {err}")
    return data


def _fetch_archive_day(latitude: float, longitude: float, day: dt.date) -> dict[str, float]:
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "start_date": day.isoformat(),
        "end_date": day.isoformat(),
        "timezone": "UTC",
        "daily": "temperature_2m_mean,dew_point_2m_mean,precipitation_sum",
    }
    data = _read_json(f"{ARCHIVE_URL}?{urlencode(params)}")
    err = data.get("reason") or data.get("error")
    if err:
        raise RuntimeError(f"Open-Meteo archive error: {err}")
    daily = data.get("daily") or {}
    times: list[str] = daily.get("time") or []
    if not times:
        raise RuntimeError("Open-Meteo archive returned no daily rows for that date.")
    idx = 0
    air = daily.get("temperature_2m_mean", [None])[idx]
    dew = daily.get("dew_point_2m_mean", [None])[idx]
    precip = daily.get("precipitation_sum", [None])[idx]
    if air is None or dew is None:
        raise RuntimeError("Open-Meteo archive response missing temperature or dew point.")
    precip_val = 0.0 if precip is None else float(precip)
    return {
        "air_temperature": float(air),
        "dewpoint_temperature": float(dew),
        "total_precipitation": precip_val,
    }


def fetch_daily_weather(latitude: float, longitude: float, day: dt.date) -> dict[str, float]:
    """
    Return air_temperature (°C), dewpoint_temperature (°C), total_precipitation (mm)
    for the given calendar day at lat/lon.
    """
    today = dt.date.today()
    if day > today + dt.timedelta(days=15):
        raise RuntimeError("Date too far in the future (Open-Meteo forecast is limited to about 16 days).")

    days_ago = (today - day).days

    if days_ago > 93:
        return _fetch_archive_day(latitude, longitude, day)

    data = _fetch_forecast_window(latitude, longitude, past_days=93, forecast_days=16)
    daily = data.get("daily") or {}
    times: list[str] = daily.get("time") or []
    target = day.isoformat()
    try:
        idx = times.index(target)
    except ValueError:
        raise RuntimeError(
            f"No weather row for {target}. Try an older date (archive) or check lat/lon."
        ) from None
    return _row_from_forecast_daily(daily, idx)
