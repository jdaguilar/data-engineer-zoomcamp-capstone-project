terraform {
  required_providers {
    google = {
      source = "hashicorp/google"
      version = "4.51.0"
    }
  }
}

provider "google" {
  credentials = file(var.credentials_file)

  project = var.project
  region  = var.region
  zone = var.zone
}

# create ZIP file for Cloud Function
data "archive_file" "cloud_function_source_code" {
 type        = "zip"
 source_dir  = "../cloud_functions/function/"
 output_path = "../cloud_functions/index.zip"
}

# Create Cloud Storage Bucket for Data WareHouse
resource "google_storage_bucket" "data_warehouse_bucket" {
  name     = "${var.project}-data-warehouse"
  location = "us-east1"

  public_access_prevention = "enforced"
}

# Create bucket to store source code for Cloud Function
resource "google_storage_bucket" "cloud_function_bucket" {
  name     = "${var.project}-${var.region}-gcf-source"
  location = "us-east1"

  public_access_prevention = "enforced"
}

# Upload ZIP file
resource "google_storage_bucket_object" "cloud_function_archive" {
  name   = "index.zip"
  bucket = google_storage_bucket.cloud_function_bucket.name
  source = "../cloud_functions/index.zip"
}

# Create Cloud Function Instance
resource "google_cloudfunctions_function" "cloud_function_instance" {
  name        = "download_gh_archive_data_v2"
  description = "Cloud Function to download GH archive data"
  runtime = "python39"

  available_memory_mb   = 1024
  source_archive_bucket = google_storage_bucket.cloud_function_bucket.name
  source_archive_object = google_storage_bucket_object.cloud_function_archive.name
  trigger_http          = true
  entry_point           = "download_gh_archive_hourly_data"

  environment_variables = {
    BUCKET_NAME = google_storage_bucket.data_warehouse_bucket.name
  }

}

# Create DataProc Cluster
resource "google_dataproc_cluster" "pyspark_cluster" {
  name   = "pyspark-cluster"
  region = var.region
}

# Create Airflow Environment
resource "google_composer_environment" "airflow_service" {
  name   = "capstone-project-airflow-service"
  region = var.region
}