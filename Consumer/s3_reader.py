import boto3

def list_raw_files(bucket_name):
    s3 = boto3.client("s3")
    response = s3.list_objects_v2(Bucket=bucket_name)
    return [obj["Key"] for obj in response.get("Contents", [])]

def read_raw_file(bucket_name, key):
    s3 = boto3.client("s3")
    obj = s3.get_object(Bucket=bucket_name, Key=key)
    return obj["Body"].read().decode("utf-8")
