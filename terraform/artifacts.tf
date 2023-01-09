resource "aws_s3_bucket" "artifacts-bucket" {
  bucket = "tvm-jenkins-artifacts-${var.environment}"
  acl    = "private"

  tags = {
    Name = "tvm-jenkins-artifacts-${var.environment}"
  }

  lifecycle_rule {
    id      = "weekly_retention"
    enabled = true

    expiration {
      days = 7
    }
  }
  logging {
    target_bucket = var.access_logs_target_bucket
    target_prefix = "log/"
  }
}
