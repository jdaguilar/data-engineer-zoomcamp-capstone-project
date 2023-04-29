output "cloud_fuction_link" {
  value = module.google_cloud_function_instance.cloud_fuction_link
}

output "dataproc_cluster_name" {
  value = module.google_cloud_dataproc_instance.dataproc_cluster_name
}

output "airflow_uri" {
  value = module.google_cloud_composer_instance.airflow_uri
}

output "airflow_dag_folder" {
  value = module.google_cloud_composer_instance.airflow_dag_folder
}
