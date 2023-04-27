
# Upload pyspark file to run pyspark Job
resource "google_storage_bucket_object" "pyspark_repo_archive" {
  name   = "process_gh_archive_dataproc.py"
  bucket = var.pyspark_repo_bucket_name
  source = "../dataproc/process_gh_archive_dataproc.py"
}

# Create DataProc Cluster
resource "google_dataproc_cluster" "pyspark_cluster" {
  name   = "pyspark-cluster"
  region = var.region
}
