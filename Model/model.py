import joblib
import numpy as np
import pandas as pd

MODEL_PATH = "Model/model_rf_cal.joblib"
model = joblib.load(MODEL_PATH)

def preprocess_row(row: pd.Series) -> pd.DataFrame:
    features = row.drop(labels=["Class"]).copy()
    hour = int(row["Time"] % 24)
    features["Hour_from_start_mod24"] = hour
    features["_log_amount"] = np.log1p(row["Amount"])
    features["is_business_hours_proxy"] = 1 if 9 <= hour <= 17 else 0
    features["is_night_proxy"] = 1 if 0 <= hour <= 6 else 0
    return features.to_frame().T

def predict_from_row(row: pd.Series) -> int:
    features = preprocess_row(row)
    return int(model.predict(features)[0])

def predict_proba_from_row(row: pd.Series) -> float:
    features = preprocess_row(row)
    return float(model.predict_proba(features)[0][1])
