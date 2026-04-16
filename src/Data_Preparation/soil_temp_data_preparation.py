from pathlib import Path

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import FunctionTransformer


def identity_function(X):
    return X

def create_soil_temp_pipeline():
    return Pipeline(steps=[
        ("identity", FunctionTransformer(identity_function))
    ])


def prepare_soil_temp_data():
    """
    Loads train/test CSV files, renames columns to readable names,
    splits train into train/dev, and returns:
    X_train, X_dev, X_test, y_train, y_dev, y_test
    """
    base_dir = Path(__file__).resolve().parents[2]
    data_dir = base_dir / "Data"

    train_df = pd.read_csv(data_dir / "train.csv")
    test_df = pd.read_csv(data_dir / "test.csv")

    rename_map = {
        "num__latitude": "latitude",
        "num__longitude": "longitude",
        "num__soil_temperature_level_1": "soil_temperature",
        "num__total_precipitation": "total_precipitation",
        "num__runoff": "runoff",
        "num__total_evaporation": "total_evaporation",
        "num__potential_evaporation": "potential_evaporation",
        "num__2m_dewpoint_temperature": "dewpoint_temperature",
        "num__2m_temperature": "air_temperature",
        "num__snow_cover": "snow_cover",
        "num__snow_depth": "snow_depth",
        "num__snowfall": "snowfall",
        "num__snowmelt": "snowmelt",
        "num__year": "year",
        "num__month": "month",
        "num__day": "day",
        "cat__DistrictNa_Central": "district_central",
        "cat__DistrictNa_East Central": "district_east_central",
        "cat__DistrictNa_North Central": "district_north_central",
        "cat__DistrictNa_Northeast": "district_northeast",
        "cat__DistrictNa_Northwest": "district_northwest",
        "cat__DistrictNa_South Central": "district_south_central",
        "cat__DistrictNa_Southeast": "district_southeast",
        "cat__DistrictNa_Southwest": "district_southwest",
        "cat__DistrictNa_West Central": "district_west_central",
        "Soil_Moisture": "soil_moisture",
    }

    train_df = train_df.rename(columns=rename_map)
    test_df = test_df.rename(columns=rename_map)

    features = [
        "latitude",
        "longitude",
        "air_temperature",
        "dewpoint_temperature",
        "total_precipitation",
        "month",
        "day",
    ]

    target = "soil_temperature"

    X_full = train_df[features]
    y_full = train_df[target]

    X_train, X_dev, y_train, y_dev = train_test_split(
        X_full,
        y_full,
        test_size=0.2,
        random_state=42
    )

    X_test = test_df[features]
    y_test = test_df[target]

    return X_train, X_dev, X_test, y_train, y_dev, y_test