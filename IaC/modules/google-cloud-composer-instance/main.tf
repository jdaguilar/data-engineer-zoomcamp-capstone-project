
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
        DATAPROC_CLUSTER_ZONE : var.zone,
        DBT_RUN_JOB_ID : var.dbt_run_job_id,
        GOOGLE_CLOUD_PROJECT_ID : var.project,
        GOOGLE_CLOUD_STORAGE_BUCKET : var.data_warehouse_bucket_name,
        REGION : var.region,
        download_gh_data_cloud_function : var.cloud_fuction_link
      }
    }
  }
}
