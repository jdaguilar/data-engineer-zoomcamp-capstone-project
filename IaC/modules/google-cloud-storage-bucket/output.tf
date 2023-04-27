
output "data_warehouse_bucket_name" {
  value = google_storage_bucket.data_warehouse_bucket.name
}

output "cloud_function_bucket_name" {
  value = google_storage_bucket.cloud_function_bucket.name
}

output "pyspark_repo_bucket_name" {
  value = google_storage_bucket.pyspark_repo_bucket.name
}
