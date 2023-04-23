from datetime import timedelta, datetime

from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.operators.dummy_operator import DummyOperator
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


with DAG(
    dag_id='download_gh_archive_data',
    start_date=datetime(2023, 1, 1),
    schedule_interval='@hourly',
) as dag:
    
    start_task = DummyOperator(task_id='start_task')

    download_data_task = PythonOperator(
        task_id='download_data',
        python_callable=download_data,
        op_kwargs={'date': '{{ ds }}', 'hour': '{{ execution_date.hour - 1}}'},
    )

    end_task = DummyOperator(task_id='end_task')


    start_task >> download_data_task >> end_task