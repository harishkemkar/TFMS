import pandas as pd
import numpy as np
import joblib

# Define the expected feature order
EXPECTED_FEATURES = [
    "V1","V2","V3","V4","V5","V6","V7","V8","V9","V10",
    "V11","V12","V13","V14","V15","V16","V17","V18","V19","V20",
    "V21","V22","V23","V24","V25","V26","V27","V28",
    "Amount","_log_amount","Hour_from_start_mod24","is_night_proxy","is_business_hours_proxy"
]

def preprocess_row(row):
    """Preprocess a single transaction row into engineered features."""
    hour = (row["Time"] // 3600) % 24
    log_amount = np.log1p(row["Amount"])
    is_business_hours = int(9 <= hour < 18)
    is_night = int(hour >= 22 or hour < 6)

    # Build dictionary with feature names
    return {
        "V1": row["V1"], "V2": row["V2"], "V3": row["V3"], "V4": row["V4"], "V5": row["V5"],
        "V6": row["V6"], "V7": row["V7"], "V8": row["V8"], "V9": row["V9"], "V10": row["V10"],
        "V11": row["V11"], "V12": row["V12"], "V13": row["V13"], "V14": row["V14"], "V15": row["V15"],
        "V16": row["V16"], "V17": row["V17"], "V18": row["V18"], "V19": row["V19"], "V20": row["V20"],
        "V21": row["V21"], "V22": row["V22"], "V23": row["V23"], "V24": row["V24"], "V25": row["V25"],
        "V26": row["V26"], "V27": row["V27"], "V28": row["V28"],
        "Amount": row["Amount"], "_log_amount": log_amount,
        "Hour_from_start_mod24": hour, "is_night_proxy": is_night,
        "is_business_hours_proxy": is_business_hours
    }

def main():
    # Load dataset
    df = pd.read_csv("training_data.csv")

    # Load Random Forest model
    rf_cal = joblib.load("Model/model_rf_cal.joblib")

    predictions, labels, probs = [], [], []

    # Process each record one by one
    for i, row in df.iterrows():
        features = preprocess_row(row)

        # Convert dict to DataFrame with correct column order
        X_row = pd.DataFrame([features], columns=EXPECTED_FEATURES)

        pred = rf_cal.predict(X_row)[0]
        prob = rf_cal.predict_proba(X_row)[0][1]

        predictions.append(pred)
        labels.append("Fraud" if pred == 1 else "Non-Fraud")
        probs.append(prob)

        # Progress logging every 10,000 records
        if i % 10 == 0:
            print(f"Processed {i} records...")

    # Add predictions back to DataFrame
    df["Predicted_Class"] = predictions
    df["Predicted_Label"] = labels
    df["Fraud_Probability"] = probs

    # Save enriched dataset to CSV
    df.to_csv("results_full.csv", index=False)
    print("✅ Finished processing all records. Results saved to results_full.csv")

if __name__ == "__main__":
    main()
