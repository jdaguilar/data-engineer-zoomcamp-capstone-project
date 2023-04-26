
from datetime import datetime

from airflow.models import DAG, Variable
from airflow.operators.dummy import DummyOperator
from airflow.providers.dbt.cloud.operators.dbt import (
    DbtCloudRunJobOperator,
)


DBT_RUN_JOB_ID = Variable.get("DBT_RUN_JOB_ID")

with DAG(
    dag_id="dbt_cloud_provider_eltml",
    start_date=datetime(2023, 1, 1),
    schedule_interval=None,
    catchup=False,
) as dag:
    start_dbt = DummyOperator(task_id="start_dbt")
    end_dbt = DummyOperator(task_id="end_dbt")

    trigger_dbt_cloud_job_run = DbtCloudRunJobOperator(
        task_id="trigger_dbt_cloud_job_run",
        job_id=DBT_RUN_JOB_ID,
        check_interval=10,
        timeout=300,
    )

    start_dbt >> trigger_dbt_cloud_job_run >> end_dbt