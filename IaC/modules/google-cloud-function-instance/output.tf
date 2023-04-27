
output "cloud_fuction_link" {
  value = google_cloudfunctions_function.cloud_function_instance.https_trigger_url
}
