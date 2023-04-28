
output "airflow_uri" {
  value = google_composer_environment.airflow_service.config.0.airflow_uri
}

output "airflow_dag_folder" {
  value = google_composer_environment.airflow_service.config.0.dag_gcs_prefix
}
