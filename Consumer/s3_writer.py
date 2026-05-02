import boto3
import json

def write_results(bucket_name, key, enriched_records):
    s3 = boto3.client("s3")
    out_data = "\n".join([json.dumps(r) for r in enriched_records])
    s3.put_object(Bucket=bucket_name, Key=key, Body=out_data.encode("utf-8"))
    print(f"✅ Results written to {bucket_name}/{key}")
