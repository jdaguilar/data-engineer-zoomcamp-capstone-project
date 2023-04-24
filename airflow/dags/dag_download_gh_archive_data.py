from datetime import timedelta, datetime

from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.operators.dummy_operator import DummyOperator

from utils.download_gh_data import download_data


# initializing the default arguments
default_args = {
		'start_date': datetime(2023, 1, 1),
		'retries': 5,
		'retry_delay': timedelta(hours=2)
}

with DAG(
    dag_id='download_gh_archive_data',
    default_args=default_args,
    schedule_interval='@hourly',
) as dag:
    
    start_task = DummyOperator(task_id='start_task')

    download_data_task = PythonOperator(
        task_id='download_data',
        python_callable=download_data,
        op_kwargs={'date': '{{ ds }}', 'hour': '{{ execution_date.hour}}'},
    )

    end_task = DummyOperator(task_id='end_task')


    start_task >> download_data_task >> end_task