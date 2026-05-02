import os
import boto3
import json
from model_integration import process_records
from s3_writer import write_results

RAW_BUCKET = "tfms-raw-data-bucket"
PROCESSED_BUCKET = "tfms-processed-data-bucket"
MODEL_PATH = "Model/model_rf_cal.joblib"

s3 = boto3.client("s3")

def rename_to_processing(bucket, key):
    new_key = f"Processing_{key}"
    # Copy then delete original
    s3.copy_object(Bucket=bucket, CopySource={"Bucket": bucket, "Key": key}, Key=new_key)
    s3.delete_object(Bucket=bucket, Key=key)
    return new_key

def main():
    # File name passed via environment variable (from SQS event → ECS task)
    raw_key = os.environ.get("RAW_FILE_KEY")
    if not raw_key:
        raise ValueError("RAW_FILE_KEY not provided")

    print(f"Starting processing for {raw_key}...")

    # Rename to Processing_<file>
    processing_key = rename_to_processing(RAW_BUCKET, raw_key)

    # Check if already processed
    out_key = raw_key.replace("TFMS_transaction_firehose", "TFMS_processed") + ".jsonl"
    try:
        s3.head_object(Bucket=PROCESSED_BUCKET, Key=out_key)
        print(f"⚠️ Skipping {raw_key}, already processed.")
        return
    except s3.exceptions.ClientError:
        pass  # Not found, safe to process

    # Read file
    obj = s3.get_object(Bucket=RAW_BUCKET, Key=processing_key)
    raw_data = obj["Body"].read().decode("utf-8")

    # Process records
    enriched = process_records(raw_data, MODEL_PATH)

    # Write results
    write_results(PROCESSED_BUCKET, out_key, enriched)

    # Cleanup
    s3.delete_object(Bucket=RAW_BUCKET, Key=processing_key)
    print(f"✅ Finished {raw_key}, results saved to {PROCESSED_BUCKET}/{out_key}")

if __name__ == "__main__":
    main()
