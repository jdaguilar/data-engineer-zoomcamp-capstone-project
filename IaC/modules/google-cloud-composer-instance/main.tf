
# Create Airflow Environment
resource "google_composer_environment" "airflow_service" {
  name   = "capstone-project-airflow-service"
  region = var.region

  config {
    software_config {
      airflow_config_overrides = {
        core-dags_are_paused_at_creation = "True"
      }

      pypi_packages = {
        apache-airflow-providers-dbt-cloud = ""
      }

      env_variables = {
        DATAPROC_CLUSTER_NAME : var.dataproc_cluster_name,
        # DATAPROC_CLUSTER_NUM_WORKERS: 1,
        DATAPROC_CLUSTER_ZONE : var.zone,
        # DATAPROC_MASTER_DISK_SIZE: 300,
        # DATAPROC_MASTER_MACHINE_TYPE: "n2-standard-4",
        DATAPROC_PYTHON_SCRIPTS_PATH: "gs://${pyspark_repo_bucket_name}",
        DBT_RUN_JOB_ID : var.dbt_run_job_id,
        GOOGLE_CLOUD_PROJECT_ID : var.project,
        GOOGLE_CLOUD_STORAGE_BUCKET : var.data_warehouse_bucket_name,
        GOOGLE_CLOUD_STORAGE_DESTINATION_FILES: "gs://${var.dataproc_cluster_name}/gh-archives/processed/",
        GOOGLE_CLOUD_STORAGE_SOURCE_FILES: "gs://${var.dataproc_cluster_name}/gh-archives/raw/{0}/*",
        REGION : var.region,
        download_gh_data_cloud_function : var.cloud_fuction_link
      }
    }
  }
}
