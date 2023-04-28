# output "cloud_fuction_link" {
#   value = google_cloudfunctions_function.cloud_function_instance.https_trigger_url
# }

# output "dataproc_cluster_name" {
#   value = google_dataproc_cluster.pyspark_cluster.name
# }

output "airflow_uri" {
  value = module.google_cloud_composer_instance.airflow_uri
}

output "airflow_dag_folder" {
  value = module.google_cloud_composer_instance.airflow_dag_folder
}
