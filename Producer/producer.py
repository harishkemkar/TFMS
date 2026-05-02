import boto3
import csv
import json
import time
import os

# AWS Firehose client
firehose = boto3.client("firehose", region_name="ap-southeast-1")

DELIVERY_STREAM_NAME = "TFMS_transaction_firehose"

# Define file path and file name separately
FILE_PATH = r"C:\HarishKemkar\local_repo\projects\Transactional Fraud Management Syetem"   # adjust to your folder

FILE_NAME = "creditcard.csv"

def send_to_firehose(file_path, file_name):
    full_path = os.path.join(file_path, file_name)
    print(f"Reading from: {full_path}")

    with open(full_path, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Convert row to JSON string
            data = json.dumps(row)

            # Publish record to Firehose
            response = firehose.put_record(
                DeliveryStreamName=DELIVERY_STREAM_NAME,
                Record={"Data": data.encode("utf-8")}
            )
            print(f"Sent record Time={row['Time']} ID={response['RecordId']}")

            # Sleep to simulate real-time flow
            # time.sleep(0.1)

if __name__ == "__main__":
    send_to_firehose(FILE_PATH, FILE_NAME)
