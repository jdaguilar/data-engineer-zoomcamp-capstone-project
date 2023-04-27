
# Create Cloud Storage Bucket for Data WareHouse
resource "google_storage_bucket" "data_warehouse_bucket" {
  name     = "${var.project}-data-warehouse"
  location = var.region

  public_access_prevention = "enforced"
}

# Create bucket to store source code for Cloud Function
resource "google_storage_bucket" "cloud_function_bucket" {
  name     = "${var.project}-${var.region}-gcf-source"
  location = var.region

  public_access_prevention = "enforced"
}

# Create bucket to store source code for Dataproc
resource "google_storage_bucket" "pyspark_repo_bucket" {
  name     = "${var.project}-dataproc-source-code"
  location = var.region
  public_access_prevention = "enforced"
}
