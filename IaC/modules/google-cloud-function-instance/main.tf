
# create ZIP file for Cloud Function
data "archive_file" "cloud_function_source_code" {
  type        = "zip"
  source_dir  = "../cloud_functions/function/"
  output_path = "../cloud_functions/index.zip"
}

# Upload ZIP file
resource "google_storage_bucket_object" "cloud_function_archive" {
  name   = "index.zip"
  bucket = var.cloud_function_bucket_name
  source = "../cloud_functions/index.zip"
}

# Create Cloud Function Instance
resource "google_cloudfunctions_function" "cloud_function_instance" {
  name        = "download_gh_archive_data_v2"
  description = "Cloud Function to download GH archive data"
  runtime     = "python39"

  available_memory_mb   = 1024
  source_archive_bucket = var.cloud_function_bucket_name
  source_archive_object = google_storage_bucket_object.cloud_function_archive.name
  trigger_http          = true
  entry_point           = "download_gh_archive_hourly_data"

  environment_variables = {
    BUCKET_NAME = var.data_warehouse_bucket_name
  }

}