import boto3
import json
import joblib
from model import predict

s3 = boto3.client("s3")
RAW_BUCKET = "tfms-raw-data-bucket"
PROCESSED_BUCKET = "tfms-processed-data-bucket"

def run_batch():
    # List objects in raw bucket
    response = s3.list_objects_v2(Bucket=RAW_BUCKET, Prefix="raw/")
    for obj in response.get("Contents", []):
        key = obj["Key"]
        raw_obj = s3.get_object(Bucket=RAW_BUCKET, Key=key)
        record = json.loads(raw_obj["Body"].read())

        # Apply model
        fraud_status = predict(record)
        enriched = {**record, "fraud_prediction": int(fraud_status)}

        # Write to processed bucket
        processed_key = key.replace("raw/", "processed/")
        s3.put_object(
            Bucket=PROCESSED_BUCKET,
            Key=processed_key,
            Body=json.dumps(enriched)
        )
        print(f"Processed {key} → {processed_key}")

if __name__ == "__main__":
    run_batch()
