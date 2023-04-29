from datetime import timedelta, datetime

from airflow import DAG
from airflow.models import Variable
from airflow.operators.empty import EmptyOperator
from airflow.providers.google.cloud.operators.dataproc import (
    DataprocSubmitJobOperator
)


# initializing the default arguments
default_args = {
	'start_date': datetime(2023, 1, 2),
	'retries': 3,
	'retry_delay': timedelta(hours=1)
}

GOOGLE_CLOUD_PROJECT_ID = Variable.get("GOOGLE_CLOUD_PROJECT_ID")
GOOGLE_CLOUD_STORAGE_BUCKET = Variable.get("GOOGLE_CLOUD_STORAGE_BUCKET")
REGION = Variable.get("REGION")
GOOGLE_CLOUD_STORAGE_SOURCE_FILES = Variable.get("GOOGLE_CLOUD_STORAGE_SOURCE_FILES")
GOOGLE_CLOUD_STORAGE_DESTINATION_FILES = Variable.get("GOOGLE_CLOUD_STORAGE_DESTINATION_FILES")

DATAPROC_CLUSTER_NAME = Variable.get("DATAPROC_CLUSTER_NAME")
DATAPROC_CLUSTER_ZONE = Variable.get("DATAPROC_CLUSTER_ZONE")
DATAPROC_MASTER_MACHINE_TYPE = Variable.get("DATAPROC_MASTER_MACHINE_TYPE")
DATAPROC_MASTER_DISK_SIZE = int(Variable.get("DATAPROC_MASTER_DISK_SIZE"))
DATAPROC_CLUSTER_NUM_WORKERS = int(Variable.get("DATAPROC_CLUSTER_NUM_WORKERS"))

DATAPROC_PYTHON_SCRIPTS_PATH = Variable.get("DATAPROC_PYTHON_SCRIPTS_PATH")


# Define pyspark job parameters
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
    schedule='0 1 * * *',
) as dag:

    start_pipeline = EmptyOperator(task_id='start_pipeline')

    pyspark_task = DataprocSubmitJobOperator(
        task_id="process_raw_gh_data",
        job=PYSPARK_JOB,
        region=REGION,
        project_id=GOOGLE_CLOUD_PROJECT_ID,
    )

    end_pipeline = EmptyOperator(task_id='end_task')

start_pipeline >> pyspark_task >> end_pipeline
