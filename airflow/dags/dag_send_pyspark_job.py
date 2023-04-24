from datetime import timedelta, datetime 

from airflow import DAG
from airflow.models import Variable
from airflow.operators.empty import EmptyOperator
from airflow.providers.google.cloud.operators.dataproc import DataprocSubmitJobOperator


# # initializing the default arguments
default_args = {
	'start_date': datetime(2023, 1, 1),
	'retries': 3,
	'retry_delay': timedelta(minutes=5)
}

GOOGLE_CLOUD_PROJECT_ID = Variable.get("GOOGLE_CLOUD_PROJECT_ID")
GOOGLE_CLOUD_STORAGE_BUCKET = Variable.get("GOOGLE_CLOUD_STORAGE_BUCKET")
REGION = Variable.get("REGION")
DATAPROC_CLUSTER_NAME = Variable.get("DATAPROC_CLUSTER_NAME")
GOOGLE_CLOUD_STORAGE_SOURCE_FILES = Variable.get("GOOGLE_CLOUD_STORAGE_SOURCE_FILES")
GOOGLE_CLOUD_STORAGE_DESTINATION_FILES = Variable.get("GOOGLE_CLOUD_STORAGE_DESTINATION_FILES")
DATAPROC_PYTHON_SCRIPTS_PATH = Variable.get("DATAPROC_PYTHON_SCRIPTS_PATH")

PYSPARK_JOB = {
    "reference": {"project_id": GOOGLE_CLOUD_PROJECT_ID},
    "placement": {"cluster_name": DATAPROC_CLUSTER_NAME},
    "pyspark_job": {
        "main_python_file_uri": f"{DATAPROC_PYTHON_SCRIPTS_PATH}/process_gh_archive_dataproc.py",
        "args": [
            "--date", "{{ ds }}",
            "--source_files_pattern", GOOGLE_CLOUD_STORAGE_SOURCE_FILES,
            "--destination_files_pattern", GOOGLE_CLOUD_STORAGE_DESTINATION_FILES,
        ]
    }
}


with DAG(
    dag_id='process_raw_gh_archive_data',
    default_args=default_args,
    schedule_interval='0 1 * * *',
) as dag:

    start_task = EmptyOperator(task_id='start_task')

    pyspark_task = DataprocSubmitJobOperator(
        task_id="process_raw_gh_data", 
        job=PYSPARK_JOB, 
        region=REGION, 
        project_id=GOOGLE_CLOUD_PROJECT_ID
    )

    end_task = EmptyOperator(task_id='end_task')

    start_task >> pyspark_task >> end_task
