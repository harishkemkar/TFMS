import pandas as pd
import numpy as np
import joblib
import json

EXPECTED_FEATURES = [
    "V1","V2","V3","V4","V5","V6","V7","V8","V9","V10",
    "V11","V12","V13","V14","V15","V16","V17","V18","V19","V20",
    "V21","V22","V23","V24","V25","V26","V27","V28",
    "Amount","_log_amount","Hour_from_start_mod24","is_night_proxy","is_business_hours_proxy"
]

def preprocess_row(row):
    hour = (int(row["Time"]) // 3600) % 24
    log_amount = np.log1p(float(row["Amount"]))
    return {
        **{f"V{i}": float(row[f"V{i}"]) for i in range(1,29)},
        "Amount": float(row["Amount"]),
        "_log_amount": log_amount,
        "Hour_from_start_mod24": hour,
        "is_night_proxy": int(hour >= 22 or hour < 6),
        "is_business_hours_proxy": int(9 <= hour < 18)
    }

def process_records(raw_data, model_path):
    model = joblib.load(model_path)
    records = raw_data.split("}{")
    records = [r if r.startswith("{") else "{" + r for r in records]
    records = [r if r.endswith("}") else r + "}" for r in records]

    enriched = []
    for i, rec in enumerate(records, start=1):
        row = json.loads(rec)
        features = preprocess_row(row)
        X_row = pd.DataFrame([features], columns=EXPECTED_FEATURES)

        pred = model.predict(X_row)[0]
        prob = model.predict_proba(X_row)[0][1]

        row["Predicted_Class"] = int(pred)
        row["Predicted_Label"] = "Fraud" if pred == 1 else "Non-Fraud"
        row["Fraud_Probability"] = float(prob)
        enriched.append(row)

        if i % 100 == 0:
            print(f"Processed {i} records...")

    return enriched
