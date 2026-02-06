resource "google_service_account" "gsa" {
  account_id = "svc@proj.iam.gserviceaccount.com"
}

resource "aws_iam_access_key" "user_key" {
  id = "AKIAEXAMPLE"
}

resource "aws_instance" "web" {
  service_account = "web-sa"

  lifecycle {
    prevent_destroy = true
  }
}

resource "google_compute_instance" "vm" {
  deletion_protection = true
  service_account      = "vm-sa"
}

resource "aws_cloudtrail" "audit" {
  enable_log_file_validation = true
}

resource "aws_autoscaling_group" "asg" {
  min_size = 1
}
