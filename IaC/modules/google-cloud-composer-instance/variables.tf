
variable "project" { }

variable "region" {
  default = "us-east1"
}

variable "zone" {
  default = "us-east1-b"
}

variable  dbt_run_job_id { }

variable  dataproc_cluster_name { }

variable  data_warehouse_bucket_name { }

variable  cloud_fuction_link { }