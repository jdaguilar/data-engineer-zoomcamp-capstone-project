import argparse
import os
import threading

import requests
from google.cloud import storage


def download_hourly_data(date, hour, output_dir):
    url = f"https://data.gharchive.org/{date}-{hour}.json.gz"
    file_name = os.path.join(output_dir, f"{date}-{hour}.json.gz")
    response = requests.get(url)
    
    with open(file_name, 'wb') as f:
        f.write(response.content)

    return file_name


def upload_to_gcs(bucket_name, source_file_name, destination_blob_name):
    """Uploads a file to the specified GCS bucket."""
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_filename(source_file_name)

    print(f"File {source_file_name} uploaded to {destination_blob_name}.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--date", 
        help="Date in the format 'YYYY-MM-DD' (e.g. 2023-04-01)"
    )
    parser.add_argument(
        "--output_dir", 
        help="Directory to store output files"
    )
    parser.add_argument(
        "--bucket_name",
        help="Name of the GCS bucket to upload files to"
    )
    args = parser.parse_args()

    date = args.date
    output_dir = args.output_dir
    hours = range(0, 24)

    if not os.path.exists(args.output_dir):
        os.makedirs(args.output_dir)

    threads = []
    for hour in hours:
        timestamp = (date, hour, output_dir)
        t = threading.Thread(target=download_hourly_data, args=timestamp)
        threads.append(t)
        t.start()
    
    for thread in threads:
        thread.join()

    # Upload downloaded files to GCS bucket
    bucket_name = args.bucket_name
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)

    for hour in hours:
        file_name = f"{date}-{hour}.json.gz"
        blob_name = f"raw/{date}/{file_name}"
        source_file_name = os.path.join(output_dir, file_name)
        upload_to_gcs(bucket_name, source_file_name, blob_name)
