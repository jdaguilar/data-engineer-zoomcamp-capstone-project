import tempfile
import os
import requests
from google.cloud.storage import Client


def download_gh_archive_hourly_data(request):
    request_json = request.get_json(silent=True)
    request_args = request.args

    if request_json and 'date' in request_json:
        date = request_json['date']
    elif request_args and 'date' in request_args:
        date = request_args['date']
    else:
        return 'Invalid request. Please provide date.', 400
    
    if request_json and 'hour' in request_json:
        hour = request_json['hour']
    elif request_args and 'hour' in request_args:
        hour = request_args['hour']
    else:
        return 'Invalid request. Please provide hour.', 400

    bucket_name = os.environ.get('BUCKET_NAME')

    with tempfile.TemporaryDirectory() as output_dir:
        url = f"https://data.gharchive.org/{date}-{hour}.json.gz"
        file_name = f"{date}-{hour}.json.gz"
        file_path = os.path.join(output_dir, file_name)
        response = requests.get(url)
        
        with open(file_path, 'wb') as f:
            f.write(response.content)

        storage_client = Client()
        bucket = storage_client.bucket(bucket_name)
        blob_name = f"gh-archives/raw/{date}/{file_name}"
        blob = bucket.blob(blob_name)
        blob.upload_from_filename(file_path)

    return 'Data downloaded and uploaded to GCS successfully!', 200
