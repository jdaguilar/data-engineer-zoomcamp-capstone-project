terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "4.51.0"
    }
  }
}

provider "google" {
  credentials = file(var.credentials_file)

  project = var.project
  region  = var.region
  zone    = var.zone
}

module "google_cloud_storage_bucket" {
  source  = "./modules/google-cloud-storage-bucket"
  project = var.project
  region  = var.region
}

module "google_cloud_function_instance" {
  source                     = "./modules/google-cloud-function-instance"
  cloud_function_bucket_name = module.google_cloud_storage_bucket.cloud_function_bucket_name
  data_warehouse_bucket_name = module.google_cloud_storage_bucket.data_warehouse_bucket_name
}

module "google_cloud_dataproc_instance" {
  source                   = "./modules/google-cloud-dataproc-instance"
  pyspark_repo_bucket_name = module.google_cloud_storage_bucket.pyspark_repo_bucket_name
}

module "google_cloud_composer_instance" {
  source                     = "./modules/google-cloud-composer-instance"
  project                    = var.project
  region                     = var.region
  zone                       = var.zone
  dbt_run_job_id             = var.dbt_run_job_id
  dataproc_cluster_name      = module.google_cloud_dataproc_instance.dataproc_cluster_name
  data_warehouse_bucket_name = module.google_cloud_storage_bucket.data_warehouse_bucket_name
  cloud_fuction_link         = module.google_cloud_function_instance.cloud_fuction_link
}
