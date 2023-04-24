
from airflow.models import Variable
import google.auth.transport.requests
import google.oauth2.id_token
import requests


def download_data(date: str, hour: int) -> str:
    # Call your cloud function here to download the data for the hour before it was called
    # ...
    # Generate the ID token
    url = Variable.get("download_gh_data_cloud_function")
    auth_req = google.auth.transport.requests.Request()
    id_token = google.oauth2.id_token.fetch_id_token(auth_req, url)

    payload = {"date": date, "hour": hour}
    headers = {'content-type': 'application/json', "Authorization": f"Bearer {id_token}"}

    response = requests.post(url, json=payload, headers=headers, timeout=60)

    if response.status_code == 200:
        output = "Data downloaded"
    else:
        output = 'Error:', response.content

    return output